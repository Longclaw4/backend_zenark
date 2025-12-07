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
{conversation_text[:5000]}

CRITICAL: Base your analysis ONLY on the conversation above. DO NOT invent or assume topics not mentioned.

Generate a CONCISE "Personal Wellness Guide":

1. *Emotional Validation* (4-5 sentences)
   - Acknowledge ONLY the feelings they actually expressed
   - Use natural, warm language (not clinical)
   - Validate their experience deeply
   - Show understanding of their specific situation

2. *Your Gentle Step Forward* (1 specific action, 1 line)
   - A single, compassionate, low-effort immediate action to solidify progress and maintain momentum
   - Based on THEIR actual concerns

3. *Quick ZenMode* (2 activities, 1 line each)
   - Two calming activities relevant to THEIR situation

4. *Safety Net* (1 line, only if they mentioned distress/crisis)
   - Crisis helpline ONLY if they expressed severe distress

5. *Motivational Quote* (suggest one quote)
   - Suggest one motivational quote which is most suited to them
   - Should resonate with their specific situation

CRITICAL: 
- Use "you/your" not "the student"
- Be warm and direct, not clinical
- ONLY reference topics they actually discussed
- Emotional validation should be 4-5 sentences"""

        analyst_prompt = f"""You are a behavioral data analyst reviewing a student's conversation patterns.

Conversation:
{conversation_text[:5000]}

CRITICAL: Base your analysis ONLY on what was actually discussed. DO NOT invent topics.

Provide "Key Insights" with this structure:

*Strengths:* (3-5 items, each 2 words)
- [2-word strength 1] (e.g., "Seeks help", "Self-aware")
- [2-word strength 2]
- [2-word strength 3]
- [2-word strength 4] (if applicable)
- [2-word strength 5] (if applicable)

*Weaknesses:* (3-5 items, each 2 words)
- [2-word weakness 1] (e.g., "Sleep disruption", "Exam anxiety")
- [2-word weakness 2]
- [2-word weakness 3]
- [2-word weakness 4] (if applicable)
- [2-word weakness 5] (if applicable)

*Overall Pattern:* (2-3 sentences)
[Summary of their emotional/behavioral pattern based ONLY on what they said]

*Behavioral Impact:* (1-2 sentences)
[What user can bring to their behavior or life based on the conversation]

CRITICAL: 
- Each strength/weakness must be exactly 2 words
- List 3-5 items for each category
- Be specific based on actual conversation
- Use "you/your" in Overall Pattern and Behavioral Impact"""

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
