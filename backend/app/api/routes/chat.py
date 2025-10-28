"""Chat API routes"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
import json
from datetime import datetime, timedelta

from app.models.schemas import ChatRequest, ChatResponse, ChatMessageResponse
from app.services.llm_service import get_llm_service
from app.services.data_service import get_data_service
from app.core.llm.prompts import SYSTEM_PROMPT
from app.core.llm.tools import TOOLS
from app.utils.time_utils import parse_relative_time

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    llm_service = Depends(get_llm_service),
    data_service = Depends(get_data_service)
):
    """
    Main chat endpoint with function calling support
    """
    
    # For MVP, using a mock user_id
    # TODO: Get from authentication
    from uuid import UUID
    mock_user_id = UUID('12345678-1234-5678-1234-567812345678')
    
    try:
        # Build messages
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": request.message}
        ]
        
        # Call LLM with tools
        response = await llm_service.chat_completion(
            messages=messages,
            tools=TOOLS
        )
        
        # Handle function calls if present
        if "tool_calls" in response and response["tool_calls"]:
            # Execute tool calls
            tool_results = await execute_tool_calls(
                response["tool_calls"],
                mock_user_id,
                data_service
            )
            
            # Add assistant message with tool calls
            messages.append({
                "role": "assistant",
                "content": response.get("content", ""),
                "tool_calls": response["tool_calls"]
            })
            
            # Add tool results
            for result in tool_results:
                messages.append({
                    "role": "tool",
                    "tool_call_id": result["tool_call_id"],
                    "content": result["content"]
                })
            
            # Get final response
            final_response = await llm_service.chat_completion(messages)
            response_text = final_response["content"]
        else:
            response_text = response["content"]
        
        # TODO: Save to chat history in database
        
        return ChatResponse(
            response=response_text,
            metadata={"tool_calls_made": len(response.get("tool_calls", []))}
        )
        
    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


async def execute_tool_calls(
    tool_calls: List[dict],
    user_id,
    data_service
) -> List[dict]:
    """Execute function tool calls"""
    
    results = []
    
    for tool_call in tool_calls:
        function_name = tool_call["function"]["name"]
        arguments = json.loads(tool_call["function"]["arguments"])
        
        try:
            # Execute the appropriate function
            if function_name == "get_brain_data":
                result = await handle_get_brain_data(user_id, arguments, data_service)
            elif function_name == "get_state_distribution":
                result = await handle_get_state_distribution(user_id, arguments, data_service)
            elif function_name == "compare_time_periods":
                result = await handle_compare_time_periods(user_id, arguments, data_service)
            elif function_name == "find_patterns":
                result = await handle_find_patterns(user_id, arguments, data_service)
            elif function_name == "get_cognitive_score":
                result = await handle_get_cognitive_score(user_id, arguments, data_service)
            elif function_name == "get_baseline":
                result = await handle_get_baseline(user_id, data_service)
            else:
                result = {"error": f"Unknown function: {function_name}"}
            
            results.append({
                "tool_call_id": tool_call["id"],
                "content": json.dumps(result)
            })
            
        except Exception as e:
            results.append({
                "tool_call_id": tool_call["id"],
                "content": json.dumps({"error": str(e)})
            })
    
    return results


async def handle_get_brain_data(user_id, args, data_service):
    """Handle get_brain_data tool call"""
    
    start_time = parse_relative_time(args["start_time"])
    end_time = parse_relative_time(args["end_time"])
    granularity = args.get("granularity", "5min")
    
    data = await data_service.get_brain_data(
        user_id, start_time, end_time, granularity
    )
    
    # Summarize for LLM (don't send all data points)
    summary = {
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "total_points": len(data),
        "sample_points": data[:5] if len(data) > 5 else data,
        "states_detected": list(set(p.get('state') for p in data if p.get('state')))
    }
    
    return summary


async def handle_get_state_distribution(user_id, args, data_service):
    """Handle get_state_distribution tool call"""
    
    start_time, end_time = parse_time_period(args["time_period"])
    
    distribution = await data_service.get_state_distribution(
        user_id, start_time, end_time
    )
    
    return {
        "time_period": args["time_period"],
        "distribution": distribution.model_dump()
    }


async def handle_compare_time_periods(user_id, args, data_service):
    """Handle compare_time_periods tool call"""
    
    period1_start, period1_end = parse_time_period(args["period1"])
    period2_start, period2_end = parse_time_period(args["period2"])
    
    comparison = await data_service.compare_time_periods(
        user_id,
        period1_start, period1_end,
        period2_start, period2_end,
        args.get("metric", "all")
    )
    
    return comparison


async def handle_find_patterns(user_id, args, data_service):
    """Handle find_patterns tool call"""
    
    time_range = args.get("time_range", "last 7 days")
    start_time, end_time = parse_time_period(time_range)
    
    patterns = await data_service.find_patterns(
        user_id,
        args["pattern_type"],
        start_time,
        end_time,
        args.get("activity")
    )
    
    return patterns


async def handle_get_cognitive_score(user_id, args, data_service):
    """Handle get_cognitive_score tool call"""
    
    start_time, end_time = parse_time_period(args["time_period"])
    
    score = await data_service.get_cognitive_score(
        user_id, start_time, end_time
    )
    
    return {
        "time_period": args["time_period"],
        "cognitive_score": score
    }


async def handle_get_baseline(user_id, data_service):
    """Handle get_baseline tool call"""
    
    # Get last 30 days
    end_time = datetime.now()
    start_time = end_time - timedelta(days=30)
    
    distribution = await data_service.get_state_distribution(
        user_id, start_time, end_time
    )
    
    score = await data_service.get_cognitive_score(
        user_id, start_time, end_time
    )
    
    return {
        "period": "last 30 days",
        "avg_cognitive_score": score,
        "avg_state_distribution": distribution.model_dump()
    }


def parse_time_period(period: str) -> tuple:
    """Parse time period string into start and end times"""
    
    now = datetime.now()
    
    if period == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif period == "yesterday":
        start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
    elif period == "this week":
        start = now - timedelta(days=now.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif period == "last week":
        start = now - timedelta(days=now.weekday() + 7)
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=7)
    elif "last" in period and "days" in period:
        # Parse "last 7 days", "last 30 days", etc.
        days = int(''.join(filter(str.isdigit, period)))
        start = now - timedelta(days=days)
        end = now
    else:
        # Default to today
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    
    return start, end
