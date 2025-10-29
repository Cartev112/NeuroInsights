"""LLM service for brain data analysis"""

from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
import json
import logging

from app.config import get_settings
from app.core.llm.prompts import SYSTEM_PROMPT, QUERY_ANALYSIS_TEMPLATE
from app.core.llm.tools import TOOLS

settings = get_settings()
logger = logging.getLogger(__name__)


class LLMService:
    """Service for interacting with OpenAI LLM"""
    
    def __init__(self):
        api_key = (settings.OPENAI_API_KEY or "").strip()
        if not api_key:
            logger.warning("OPENAI_API_KEY not provided. Falling back to mock insights.")
            self.client = None
        else:
            self.client = AsyncOpenAI(api_key=api_key)
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
        
        if not self.client:
            logger.debug("LLM client unavailable; returning fallback response.")
            return {
                "content": self._fallback_response(messages),
                "role": "assistant"
            }

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
                        "type": getattr(tc, "type", "function"),
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in message.tool_calls
                ]
            
            return result
            
        except Exception as e:
            logger.exception("LLM chat completion failed: %s", e)
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
        
        try:
            response = await self.chat_completion(messages, tools=TOOLS)
            return response["content"]
        except Exception:
            logger.warning("Falling back to heuristic analysis for query: %s", query)
            return self._fallback_analysis(query, context)
    
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
        
        try:
            response = await self.chat_completion(messages, temperature=0.8)
            return response["content"]
        except Exception:
            logger.warning("Falling back to heuristic insight generation.")
            return self._fallback_insight(data_summary, baseline)
    
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
        
        try:
            response = await self.chat_completion(messages, temperature=0.7)
            return response["content"]
        except Exception:
            logger.warning("Falling back to heuristic daily summary for %s.", date)
            return self._fallback_daily_summary(date, data_summary, baseline)
    
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context dictionary into readable string"""
        
        formatted = []
        for key, value in context.items():
            if isinstance(value, (dict, list)):
                formatted.append(f"{key}: {json.dumps(value, indent=2)}")
            else:
                formatted.append(f"{key}: {value}")
        
        return "\n".join(formatted)

    def _fallback_response(self, messages: List[Dict[str, str]]) -> str:
        """Provide a minimal response when LLM is unavailable"""
        user_content = ""
        for message in reversed(messages):
            if message.get("role") == "user" and message.get("content"):
                user_content = message["content"]
                break
        return (
            "LLM service is temporarily unavailable. "
            "Here's the last request for reference:\n\n"
            f"{user_content[:500]}"
        )

    def _fallback_analysis(self, query: str, context: Optional[Dict[str, Any]]) -> str:
        """Generate a simple analysis response without LLM access"""
        lines = [f"I can't reach the LLM right now, but here's a quick take on: \"{query}\"."]
        if context:
            lines.append("Relevant context:")
            for key, value in context.items():
                lines.append(f"- {key}: {value}")
        lines.append("Consider reviewing your dashboard metrics for deeper insights until AI summaries resume.")
        return "\n".join(lines)

    def _fallback_insight(self, data_summary: Dict[str, Any], baseline: Optional[Dict[str, Any]]) -> str:
        """Generate a simple insight when LLM is unavailable"""
        score = data_summary.get("cognitive_score", 0)
        distribution = data_summary.get("state_distribution", {})
        focus = distribution.get("deep_focus", 0) + distribution.get("creative_flow", 0)
        stress = distribution.get("stressed", 0)

        insight_lines = [
            "Insight: Focus levels are strong today." if focus >= 40 else "Insight: Focus time is moderate today.",
            f"Evidence: Cognitive score {score}/100, focus states {focus:.1f}% of the time, stress {stress:.1f}%."
        ]
        if focus >= 40:
            recommendation = "Keep leveraging the routines that supported deep focus today."
        else:
            recommendation = "Schedule focused work during your top-performing hours and limit distractions."
        insight_lines.append(f"Recommendation: {recommendation}")
        return "\n".join(insight_lines)

    def _fallback_daily_summary(
        self,
        date: str,
        data_summary: Dict[str, Any],
        baseline: Optional[Dict[str, Any]]
    ) -> str:
        """Generate a simple daily summary when LLM is unavailable"""
        score = data_summary.get("cognitive_score", 0)
        distribution = data_summary.get("state_distribution", {})
        focus = data_summary.get("focus_time", 0)
        stress = data_summary.get("stress_level", 0)

        summary_lines = [
            f"Daily Summary for {date}:",
            f"- Overall cognitive score: {score}/100.",
            f"- Focus states accounted for {focus:.1f}% of the day.",
            f"- Stress signals remained around {stress:.1f}%." if stress else "- Minimal stress detected today.",
        ]

        if baseline and isinstance(baseline, dict):
            baseline_score = baseline.get("cognitive_score")
            if baseline_score is not None:
                diff = score - baseline_score
                trend = "above" if diff > 0 else "below" if diff < 0 else "matching"
                summary_lines.append(f"- Compared to baseline: {abs(diff):.1f} points {trend} your average.")

        if focus >= 40:
            summary_lines.append("Highlights: Strong sustained focus—consider repeating today's schedule for deep work.")
        else:
            summary_lines.append("Highlights: Focus time was limited; identify periods of distraction to adjust tomorrow.")

        summary_lines.append("Tomorrow's tip: Plan priority tasks during your highest focus windows and include short breaks.")
        return "\n".join(summary_lines)


# Singleton instance
_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """Get or create LLM service instance"""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
