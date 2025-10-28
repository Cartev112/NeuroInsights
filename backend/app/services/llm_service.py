"""LLM service for brain data analysis"""

from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
import json

from app.config import get_settings
from app.core.llm.prompts import SYSTEM_PROMPT, QUERY_ANALYSIS_TEMPLATE
from app.core.llm.tools import TOOLS

settings = get_settings()


class LLMService:
    """Service for interacting with OpenAI LLM"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict]] = None,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """
        Get chat completion from LLM
        
        Returns:
            Dict with 'content' (str) and optionally 'tool_calls' (list)
        """
        
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"
        
        try:
            response = await self.client.chat.completions.create(**kwargs)
            message = response.choices[0].message
            
            result = {
                "content": message.content or "",
                "role": message.role
            }
            
            # Check for tool calls
            if hasattr(message, 'tool_calls') and message.tool_calls:
                result["tool_calls"] = [
                    {
                        "id": tc.id,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in message.tool_calls
                ]
            
            return result
            
        except Exception as e:
            print(f"LLM Error: {e}")
            raise
    
    async def analyze_query(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Analyze a user query with optional context
        """
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
        
        if context:
            # Add context to the query
            context_str = self._format_context(context)
            messages[-1]["content"] = f"{query}\n\nContext:\n{context_str}"
        
        response = await self.chat_completion(messages, tools=TOOLS)
        return response["content"]
    
    async def generate_insight(
        self,
        data_summary: Dict[str, Any],
        baseline: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate an insight from brain data
        """
        
        prompt = f"""Based on the following brain data, generate a meaningful insight.

Data Summary:
{json.dumps(data_summary, indent=2)}

User's Baseline (for comparison):
{json.dumps(baseline, indent=2) if baseline else "No baseline available yet"}

Generate an insight that:
1. Identifies a notable pattern or trend
2. Compares to baseline when relevant
3. Provides context and explanation
4. Offers an actionable recommendation
5. Is specific and data-driven

Format your response as:
- Insight: [Clear statement of the finding]
- Evidence: [Supporting data]
- Recommendation: [Actionable next step]
"""
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.chat_completion(messages, temperature=0.8)
        return response["content"]
    
    async def generate_daily_summary(
        self,
        date: str,
        data_summary: Dict[str, Any],
        baseline: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a daily summary of cognitive performance
        """
        
        prompt = f"""Generate a daily summary of cognitive performance.

Date: {date}

Data Summary:
{json.dumps(data_summary, indent=2)}

Baseline comparison:
{json.dumps(baseline, indent=2) if baseline else "No baseline available yet"}

Generate a comprehensive daily summary that includes:
1. Overall cognitive performance assessment
2. Key highlights (what went well)
3. Areas for improvement
4. Notable patterns or transitions
5. Specific recommendations for tomorrow

Keep the tone encouraging and actionable.
"""
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
        
        response = await self.chat_completion(messages, temperature=0.7)
        return response["content"]
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context dictionary into readable string"""
        
        formatted = []
        for key, value in context.items():
            if isinstance(value, (dict, list)):
                formatted.append(f"{key}: {json.dumps(value, indent=2)}")
            else:
                formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted)


# Singleton instance
_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """Get or create LLM service instance"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
