# AI-Powered Exam Buddy
# Provides intelligent study guidance using OpenAI

import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# Exam-specific knowledge base
EXAM_STRATEGIES = {
    "JEE": {
        "subjects": ["Physics", "Chemistry", "Mathematics"],
        "tips": [
            "Master NCERT thoroughly before moving to advanced books",
            "Practice 3+ years of previous papers",
            "Focus on conceptual clarity over memorization",
            "Daily problem-solving: 2-3 hours minimum",
            "Weak topics first, then strengthen strong areas"
        ],
        "resources": "NCERT, HC Verma (Physics), OP Tandon (Chemistry), RD Sharma (Math)"
    },
    "NEET": {
        "subjects": ["Physics", "Chemistry", "Biology"],
        "tips": [
            "Biology = NCERT line-by-line (most important)",
            "Physics: 300+ numerical practice mandatory",
            "Chemistry: Daily organic reactions revision",
            "Weekly mock tests are non-negotiable",
            "Error log book for every wrong answer"
        ],
        "resources": "NCERT (Biology), DC Pandey (Physics), MS Chauhan (Chemistry)"
    },
    "CUET": {
        "subjects": ["Domain subjects", "General Test", "Language"],
        "tips": [
            "Domain subjects = NCERT deep-dive",
            "General test = 1 year current affairs coverage",
            "Language section: 30 min daily reading practice",
            "University-specific syllabus check mandatory",
            "Time management: 60 min per section practice"
        ],
        "resources": "NCERT, Current Affairs compilations, Previous year papers"
    },
    "GATE": {
        "subjects": ["Engineering Core", "Aptitude", "Mathematics"],
        "tips": [
            "Standard textbooks > coaching notes",
            "Previous 15 years papers analysis essential",
            "Virtual calculator practice (2 weeks before exam)",
            "Revision: 3 cycles minimum",
            "Weak subjects: 60% time allocation"
        ],
        "resources": "Standard textbooks, GATE previous papers, NPTEL lectures"
    }
}

STUDY_TECHNIQUES = {
    "time_management": "Use Pomodoro: 25 min focused study + 5 min break. Track daily hours.",
    "active_recall": "Close book, write what you remember. Test yourself before reviewing.",
    "spaced_repetition": "Review after 1 day, 3 days, 7 days, 14 days for long-term retention.",
    "feynman": "Explain concepts in simple terms as if teaching a 12-year-old.",
    "practice_testing": "70% practice problems, 30% reading. Testing > passive reading.",
    "interleaving": "Mix different subjects/topics in one session for better retention.",
    "mind_mapping": "Create visual connections between topics for better recall."
}

async def get_exam_buddy_response(question: str, session_id: str = "", context: str = "") -> str:
    """
    Generate intelligent exam-focused responses using AI.
    
    Args:
        question: Student's question/message
        session_id: Session identifier
        context: Additional context for the question
    
    Returns:
        str: AI-generated study guidance
    """
    try:
        # Get API key from environment
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return "I'm having trouble connecting to my knowledge base. Please try again later."
        
        # Detect exam type from question
        question_lower = question.lower()
        detected_exam = None
        exam_context = ""
        
        for exam_name, exam_data in EXAM_STRATEGIES.items():
            if exam_name.lower() in question_lower:
                detected_exam = exam_name
                exam_context = f"\n\nExam: {exam_name}\nKey subjects: {', '.join(exam_data['subjects'])}\nTop strategies: {'; '.join(exam_data['tips'][:3])}\nRecommended resources: {exam_data['resources']}"
                break
        
        # Build system prompt
        system_prompt = f"""You are an expert Study Buddy AI specializing in exam preparation and academic success.

Your role:
- Provide specific, actionable study advice
- Be encouraging but realistic
- Focus on proven study techniques
- Give concrete examples and strategies
- Keep responses concise (3-4 sentences max)

Study Techniques Available:
{chr(10).join([f"- {k}: {v}" for k, v in STUDY_TECHNIQUES.items()])}
{exam_context}

Guidelines:
1. If student asks about a specific exam, use the exam-specific strategies
2. If asking about study methods, recommend proven techniques
3. If asking about time management, give specific schedules
4. If asking about stress, acknowledge it and provide coping strategies
5. Always end with ONE actionable next step

Context: {context if context else 'General study guidance'}

Keep responses under 100 words. Be specific, not generic."""

        # Create LLM instance
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            openai_api_key=api_key
        )
        
        # Generate response
        response = await llm.ainvoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=question)
        ])
        
        # Extract response text
        response_text = response.content if isinstance(response.content, str) else str(response.content)
        
        return response_text.strip()
        
    except Exception as e:
        # Fallback response on error
        return f"I understand you're asking about: '{question}'. Let me help you with that. Could you provide more details about what specific aspect you need help with?"
