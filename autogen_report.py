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

⚠️ CRITICAL ANTI-HALLUCINATION RULES ⚠️
1. ONLY use information EXPLICITLY stated in the conversation above
2. DO NOT infer, assume, or add topics the user did not mention
3. If the user talked about "girlfriend", DO NOT mention "mother" or "parents"
4. If the user talked about "exams", DO NOT add "family pressure" unless they said it
5. If the user talked about "sleep", DO NOT add "anxiety" unless they mentioned it
6. STICK TO THEIR EXACT WORDS AND TOPICS

EXAMPLES OF WHAT NOT TO DO:
❌ WRONG: "You're worried about your mother's reaction to your exam results"
   (If they never mentioned mother)
✅ CORRECT: "You're worried about your exam results"

❌ WRONG: "Your family pressure is causing stress"
   (If they never mentioned family)
✅ CORRECT: "Your exam stress is affecting your sleep"

❌ WRONG: "You're concerned about disappointing your parents"
   (If they only mentioned girlfriend)
✅ CORRECT: "You're concerned about your girlfriend's feelings"

Generate a CONCISE "Personal Wellness Guide":

1. *Emotional Validation* (4-5 sentences)
   - Acknowledge ONLY the EXACT feelings they stated (use their words!)
   - Use natural, warm language (not clinical)
   - Validate their experience deeply
   - Show understanding of THEIR SPECIFIC situation (not a generic one)
   - DO NOT add people, relationships, or concerns they didn't mention

2. *Your Gentle Step Forward* (1 specific action, 1 line)
   - A single, compassionate, low-effort immediate action to solidify progress and maintain momentum
   - Based ONLY on what they actually discussed

3. *Quick ZenMode* (2 activities, 1 line each)
   - Two calming activities relevant to THEIR ACTUAL situation

4. *Safety Net* (1 line, only if they mentioned distress/crisis)
   - Crisis helpline ONLY if they expressed severe distress

5. *Motivational Quote* (suggest one quote)
   - Suggest one motivational quote which is most suited to them
   - Should resonate with their ACTUAL situation

FINAL CHECK BEFORE RESPONDING:
- Did I mention "mother", "father", "parents", or "family" when they didn't? REMOVE IT.
- Did I mention any topic the user did NOT bring up? REMOVE IT.
- Am I using their actual words and concerns? If no, REWRITE.

CRITICAL: 
- Use "you/your" not "the student"
- Be warm and direct, not clinical
- ONLY reference topics they ACTUALLY discussed (check twice!)
- Emotional validation should be 4-5 sentences
- NO HALLUCINATIONS - stick to their exact topics!"""

        analyst_prompt = f"""You are a behavioral data analyst reviewing a student's conversation patterns.

Conversation:
{conversation_text[:5000]}

⚠️ CRITICAL ANTI-HALLUCINATION RULES ⚠️
1. ONLY analyze what was EXPLICITLY discussed in the conversation
2. DO NOT infer topics, relationships, or issues not mentioned
3. If they talked about "girlfriend", DO NOT mention "mother", "father", or "family"
4. If they talked about "exams", DO NOT add "parental pressure" unless stated
5. STICK TO THEIR EXACT WORDS - do not generalize or assume

EXAMPLES OF WHAT NOT TO DO:
❌ WRONG: "worry about mother discovering something"
   (If they never mentioned mother)
✅ CORRECT: "exam-related stress"

❌ WRONG: "anxiety related to parental expectations"
   (If they never mentioned parents)
✅ CORRECT: "self-imposed exam pressure"

❌ WRONG: "fear of family reaction"
   (If they only talked about girlfriend)
✅ CORRECT: "relationship concerns"

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
[Summary based ONLY on what they ACTUALLY said - use their exact topics]
DO NOT mention mother, father, parents, or family unless they explicitly discussed them.

*Behavioral Impact:* (1-2 sentences)
[What user can bring to their behavior based ONLY on the conversation topics]

FINAL CHECK:
- Did I mention "mother", "father", "parents", or "family" when they didn't? REMOVE IT.
- Did I mention any person, relationship, or issue NOT in the conversation? REMOVE IT.
- Am I analyzing their ACTUAL words or making assumptions? Stick to ACTUAL.

CRITICAL: 
- Each strength/weakness must be exactly 2 words
- List 3-5 items for each category
- Be specific based on ACTUAL conversation (not assumptions)
- Use "you/your" in Overall Pattern and Behavioral Impact
- DOUBLE-CHECK: No hallucinated topics!
- NO MENTIONS of people/relationships not discussed!"""

        planner_prompt = f"""Role: You are the Personalized Mental Wellness Planner Generator. Your task is to construct a highly actionable, evidence-based Weekly Mental Wellness Plan that drives positive behavioral change, based on the user's current status and identified constraints.

Based on this conversation:
{conversation_text[:2000]}

Output MUST be ONLY this concise structure, filling in the content. Do not add any preamble or extra text.

### Your Personalized Weekly Plan

1. FOCUS: [3 Core Focus Areas, comma-separated, e.g., Stress Reduction, Behavioral Activation, Sleep Hygiene]

2. ACTIONS:
* *[Action 1 Name]:* Days: [Suggested Days, e.g., Mon/Thu]. When: [Context, e.g., Before first meeting]. Task: [Specific, low-effort task]. Reflect: [Self-aware question, e.g., How did this shift your energy?].
* *[Action 2 Name]:* Days: [Suggested Days, e.g., Tue/Fri]. When: [Context, e.g., During lunch break]. Task: [Specific, low-effort task]. Reflect: [Self-aware question, e.g., What feeling did you notice?].
* *[Action 3 Name]:* Days: [Suggested Days, e.g., Wed/Sat]. When: [Context, e.g., When arriving home]. Task: [Specific, low-effort task]. Reflect: [Self-aware question, e.g., Did tension decrease?].
* *[Action 4 Name (Optional)]:* Days: [Suggested Day, e.g., Sun]. When: [Context, e.g., Before sleep]. Task: [Specific, low-effort task]. Reflect: [Self-aware question, e.g., What positive was created this week?].

3. GENTLE STEP: [1 compassionate, actionable follow-up sentence for the next day.]

CRITICAL RULES:
- Be culturally appropriate for Indian students
- Make tasks realistic and achievable
- Focus on gradual improvement
- Use ONLY the structure above, no extra text"""

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
