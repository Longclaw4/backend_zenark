"""
AI-Powered Mental Health Report Generator
Generates personalized wellness reports using OpenAI GPT-4
"""

import os
import json
import datetime
from bson import ObjectId
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from api_key_rotator import get_api_key

load_dotenv()

def generate_autogen_report(conversation_text: str, name: str) -> dict:
    """
    Generate a comprehensive 3-part mental health report.
    
    Args:
        conversation_text: Full conversation transcript
        name: Student's name
        
    Returns:
        dict: Report with TherapistAgent and DataAnalystAgent insights
    """
    
    try:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            openai_api_key=get_api_key()
        )
        
        # ============================================
        # PARALLEL EXECUTION - All 3 agents at once
        # ============================================
        
        # Define all prompts first
        therapist_prompt = f"""You are a compassionate mental health therapist analyzing a student's conversation.

Student Name: {name}

Conversation:
{conversation_text[:3000]}

Generate a CONCISE "Personal Wellness Guide" (MAX 10 lines total):

1. *Emotional Validation* (1-2 sentences only)
   - Acknowledge their core feeling

2. *Your Next Step* (1 specific action, 1 line)
   - One immediate, doable action for today

3. *Quick ZenMode* (2 activities, 1 line each)
   - Two calming activities (e.g., "5-min breathing", "Evening walk")

4. *Safety Net* (1 line, only if high distress detected)
   - Crisis helpline number if needed

5. *Quote* (1 line)
   - One short motivational quote

CRITICAL: Keep total output under 10 lines. Be concise and actionable."""

        analyst_prompt = f"""You are a behavioral data analyst reviewing a student's conversation patterns.

Conversation:
{conversation_text[:3000]}

Provide a SINGLE CONCISE paragraph called "Key Insights" (MAX 5-6 lines):

Combine:
- Top 2 behavioral strengths (e.g., "resilient, self-aware")
- Top 2 growth areas (e.g., "time management, boundaries")
- Overall emotional pattern (1 sentence)

Format as ONE flowing paragraph:
*Key Insights:*
[Student name] demonstrates [strength 1] and [strength 2], showing [positive pattern]. However, they face challenges with [growth area 1] and [growth area 2]. Overall, [emotional/behavioral pattern summary in 1 sentence].

CRITICAL: Maximum 5-6 lines total. Be specific but brief."""

        planner_prompt = f"""You are a wellness coach creating a simple daily routine.

Based on this conversation:
{conversation_text[:2000]}

Create "Top 3 Daily Habits" (MAX 10-15 lines total):

Format as:
*Top 3 Daily Habits for This Week:*

*1. Morning Anchor (5-10 min)*
[One specific morning routine - e.g., "7:00 AM: 5-min gratitude journaling + stretching"]

*2. Study/Work Focus*
[One productivity technique - e.g., "Pomodoro: 25min study, 5min break, repeat 4x"]

*3. Evening Wind-Down (15-20 min)*
[One evening routine - e.g., "9:00 PM: No screens, 10-min breathing, early sleep"]

*Weekly Bonus:*
[One social/self-care activity - e.g., "Sunday: 30-min nature walk or call a friend"]

CRITICAL: Keep under 15 lines. Be specific with times and durations. Make it realistic for Indian students."""

        # Run all 3 agents in parallel using asyncio
        import asyncio
        
        async def generate_all_agents():
            """Nested async function to run all 3 agents in parallel"""
            
            async def get_therapist():
                response = await llm.ainvoke([
                    SystemMessage(content="You are an empathetic mental health therapist. Be CONCISE."),
                    HumanMessage(content=therapist_prompt)
                ])
                return response.content if isinstance(response.content, str) else str(response.content)
            
            async def get_analyst():
                response = await llm.ainvoke([
                    SystemMessage(content="You are a behavioral data analyst. Be CONCISE."),
                    HumanMessage(content=analyst_prompt)
                ])
                return response.content if isinstance(response.content, str) else str(response.content)
            
            async def get_planner():
                response = await llm.ainvoke([
                    SystemMessage(content="You are a wellness coach and routine planner."),
                    HumanMessage(content=planner_prompt)
                ])
                return response.content if isinstance(response.content, str) else str(response.content)
            
            # Execute all 3 in parallel (3x faster!)
            return await asyncio.gather(
                get_therapist(),
                get_analyst(),
                get_planner()
            )
        
        # Run the async function
        therapist_content, analyst_content, planner_content = asyncio.run(generate_all_agents())
        
        # ============================================
        # AGGREGATE REPORT
        # ============================================
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        report_data = {
            "name": name,
            "timestamp": timestamp,
            "report": [
                {
                    "name": "TherapistAgent",
                    "content": therapist_content
                },
                {
                    "name": "DataAnalystAgent",
                    "content": analyst_content
                },
                {
                    "name": "RoutinePlannerAgent",
                    "content": planner_content
                }
            ]
        }
        
        return sanitize(report_data)
        
    except Exception as e:
        # Fallback report on error
        return {
            "name": name,
            "timestamp": datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
            "report": [
                {
                    "name": "TherapistAgent",
                    "content": f"*Personal Wellness Guide:*\n\n1. *Validation:* You're taking a positive step by seeking support.\n\n2. *Next Step:* Take 3 deep breaths right now.\n\n3. *ZenMode:* Try 5-min meditation or a short walk.\n\n4. *Quote:* \"Progress, not perfection.\""
                },
                {
                    "name": "DataAnalystAgent",
                    "content": f"*Key Insights:*\n{name} demonstrates openness to support and self-awareness. They may benefit from developing stress management and coping strategies. Overall, the student is actively engaging with mental health resources, showing a positive step toward wellbeing."
                }
            ],
            "error": str(e)
        }


def sanitize(obj):
    """Recursively sanitize ObjectId and other non-JSON types."""
    if isinstance(obj, list):
        return [sanitize(x) for x in obj]
    if isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return obj
