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
        # PART 1: THERAPIST AGENT (Wellness Guide)
        # ============================================
        therapist_prompt = f"""You are a compassionate mental health therapist analyzing a student's conversation.

Student Name: {name}

Conversation:
{conversation_text[:3000]}

Generate a "Personal Wellness Guide" with these sections:

1. **Emotional Validation** (2-3 sentences)
   - Acknowledge their feelings and struggles
   - Show empathy and understanding

2. **Immediate Micro-Action** (1 specific action)
   - One small, doable step they can take today
   - Make it concrete and achievable

3. **ZenMode Prescription** (2-3 activities)
   - Calming activities suited to their situation
   - Examples: breathing exercises, journaling, nature walk

4. **Professional Safety Net** (if needed)
   - Crisis helplines if distress is high
   - Encouragement to seek professional help

Keep tone warm, non-judgmental, and supportive. Focus on hope and actionable steps."""

        therapist_response = llm.invoke([
            SystemMessage(content="You are an empathetic mental health therapist."),
            HumanMessage(content=therapist_prompt)
        ])
        
        therapist_content = therapist_response.content if isinstance(therapist_response.content, str) else str(therapist_response.content)
        
        # ============================================
        # PART 2: DATA ANALYST AGENT (Strengths & Weaknesses)
        # ============================================
        analyst_prompt = f"""You are a behavioral data analyst reviewing a student's conversation patterns.

Conversation:
{conversation_text[:3000]}

Analyze and provide:

1. **Strengths** (3-5 specific behavioral strengths)
   - Examples: "Shows resilience by seeking help", "Self-aware about stress triggers"
   - Be specific, not generic

2. **Weaknesses/Growth Areas** (3-5 specific challenges)
   - Examples: "Struggles with time management", "Difficulty setting boundaries"
   - Frame as growth opportunities, not failures

3. **Overall Pattern** (2-3 sentences)
   - Summary of their emotional/behavioral patterns
   - Key insights about their coping style

Format your response as:

**Strengths:**
- [strength 1]
- [strength 2]
...

**Growth Areas:**
- [area 1]
- [area 2]
...

**Overall Pattern:**
[summary paragraph]"""

        analyst_response = llm.invoke([
            SystemMessage(content="You are a behavioral data analyst."),
            HumanMessage(content=analyst_prompt)
        ])
        
        analyst_content = analyst_response.content if isinstance(analyst_response.content, str) else str(analyst_response.content)
        
        # ============================================
        # PART 3: 7-DAY SELF-CARE PLANNER
        # ============================================
        planner_prompt = f"""You are a wellness coach creating a personalized 7-day self-care plan.

Based on this conversation:
{conversation_text[:2000]}

Create a realistic 7-day plan with:

**Day 1-7 Structure:**
- Morning routine (10-15 min)
- Study/work focus (with breaks)
- Social connection activity
- Evening wind-down
- ZenMode activity

Make it:
- Culturally appropriate for Indian students
- Realistic and achievable
- Focused on gradual improvement
- Include specific times/durations

Format as:
**Day 1: [Theme]**
Morning: ...
Afternoon: ...
Evening: ...
ZenMode: ..."""

        planner_response = llm.invoke([
            SystemMessage(content="You are a wellness coach and routine planner."),
            HumanMessage(content=planner_prompt)
        ])
        
        planner_content = planner_response.content if isinstance(planner_response.content, str) else str(planner_response.content)
        
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
                    "content": f"Analysis for {name}: Based on the conversation, the student shows engagement. Further monitoring recommended."
                },
                {
                    "name": "DataAnalystAgent",
                    "content": "**Strengths:**\n- Seeking support\n- Open communication\n\n**Growth Areas:**\n- Stress management\n- Coping strategies\n\n**Overall Pattern:**\nStudent is actively engaging with mental health support."
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
