"""
Fallback Responses for Zenark
Pre-written responses to reduce OpenAI API calls
"""

import random

FALLBACK_RESPONSES = {
    "greeting": [
        "Hi there! I'm Zenark, your mental health companion. How are you feeling today?",
        "Hello! I'm here to support you. What's on your mind?",
        "Hey! Thanks for reaching out. How can I help you today?",
        "Hi! I'm here to listen. How are you doing right now?",
    ],
    
    "exam_stress": [
        "Exam stress is really tough. Here's a quick tip: Try the Pomodoro technique - 25 min focused study, 5 min break. Repeat 4 times, then take a longer break. It helps maintain focus without burnout!",
        "I understand exam pressure can feel overwhelming. Remember: Break your study into small chunks, take regular breaks, and be kind to yourself. You're doing your best!",
        "Exam anxiety is normal. Try this: Write down your worries for 5 minutes, then close the paper. This helps your brain 'park' the anxiety so you can focus on studying.",
    ],
    
    "sleep_issues": [
        "Sleep troubles are common during stressful times. Try this tonight: No screens 1 hour before bed, 5-min breathing exercise, and keep a consistent sleep time. Your brain will thank you!",
        "For better sleep: Keep your room cool (18-20°C), avoid caffeine after 3pm, and try the 4-7-8 breathing technique (inhale 4s, hold 7s, exhale 8s). Repeat 4 times.",
        "Can't sleep? Try this: Get out of bed if you can't sleep after 20 minutes. Do something relaxing (read, light stretching), then try again. Don't force it!",
    ],
    
    "study_tips": [
        "Here are 3 proven study techniques:\n1. Active Recall: Close your book and write everything you remember\n2. Spaced Repetition: Review after 1, 3, 7, and 14 days\n3. Feynman Technique: Explain the concept like you're teaching a 12-year-old",
        "Study smarter, not harder! Try the Pomodoro technique: 25 min study, 5 min break. During breaks, move your body - walk, stretch, or do jumping jacks. Movement helps memory!",
        "Best study tip: Teach someone else! Explaining concepts out loud (even to yourself) reveals gaps in your understanding and strengthens memory.",
    ],
    
    "motivation": [
        "You're doing great by seeking help! That takes courage. Remember: Progress, not perfection. Every small step counts. 💪",
        "Feeling unmotivated? That's okay! Start with just 5 minutes. Tell yourself: 'I'll study for 5 minutes, then decide if I want to continue.' Usually, starting is the hardest part!",
        "Remember why you started. Your goals are valid. Your effort matters. You're stronger than you think. Keep going! 🌟",
    ],
    
    "crisis": [
        "I'm here for you, but if you're in crisis, please reach out to a professional immediately:\n\n🇮🇳 India:\n- AASRA: 91-22-27546669\n- Vandrevala Foundation: 1860-2662-345\n- iCall: 022-25521111\n\nYou're not alone. Help is available. 💙",
        "Your safety is the priority. If you're having thoughts of self-harm, please contact:\n\n🇮🇳 Emergency: 112\n- AASRA: 91-22-27546669\n- Sneha: 044-24640050\n\nThese feelings are temporary. You matter. 💙",
    ],
    
    "high_traffic": [
        "⏳ I'm experiencing high traffic right now (many students reaching out!). Your response is coming in ~15-20 seconds. While you wait, take 3 deep breaths and notice 5 things around you. 🌸",
        "⏳ Lots of students seeking support right now! You're in queue (~20s wait). Meanwhile, remember: You're doing great by reaching out. That's a sign of strength! 💪",
        "⏳ High traffic moment! Your turn is coming (~15s). Quick mindfulness tip while you wait: Close your eyes, breathe deeply, and think of one thing you're grateful for today. 🙏",
    ],
    
    "goodbye": [
        "Thank you for trusting me with your thoughts today. 🌟 Take a moment: close your eyes, take three deep breaths, and be proud of yourself for showing up. I'm here whenever you need to talk. Take care! 💙",
        "You did great today by opening up. Remember: Progress, not perfection. I'm here for you anytime. Stay strong! 💪",
        "Thanks for chatting with me. You're not alone in this journey. Come back anytime you need support. Take care of yourself! 🌸",
    ],
    
    "default": [
        "I'm here to listen and support you. Could you tell me more about what you're experiencing?",
        "I want to understand better. Can you share more about how you're feeling?",
        "Thank you for sharing. What's been on your mind lately?",
    ]
}

def get_fallback_response(category="default", user_message=""):
    """
    Get a pre-written fallback response
    
    Args:
        category: Type of response needed
        user_message: Original user message (for context)
    
    Returns:
        str: Fallback response
    """
    # Detect category from user message if not specified
    if category == "auto":
        user_lower = user_message.lower()
        
        # Greetings
        if any(word in user_lower for word in ["hi", "hello", "hey", "heya", "sup", "yo"]):
            category = "greeting"
        
        # Exam stress
        elif any(word in user_lower for word in ["exam", "test", "quiz", "marks", "fail", "score"]):
            category = "exam_stress"
        
        # Sleep issues
        elif any(word in user_lower for word in ["sleep", "insomnia", "tired", "exhausted", "can't sleep"]):
            category = "sleep_issues"
        
        # Study tips
        elif any(word in user_lower for word in ["study", "focus", "concentrate", "learn", "remember"]):
            category = "study_tips"
        
        # Motivation
        elif any(word in user_lower for word in ["motivat", "give up", "quit", "can't do", "too hard"]):
            category = "motivation"
        
        # Crisis
        elif any(word in user_lower for word in ["suicide", "kill myself", "end it", "die", "harm"]):
            category = "crisis"
        
        # Goodbye
        elif any(word in user_lower for word in ["bye", "goodbye", "thanks", "thank you", "see you"]):
            category = "goodbye"
        
        else:
            category = "default"
    
    # Get random response from category
    responses = FALLBACK_RESPONSES.get(category, FALLBACK_RESPONSES["default"])
    return random.choice(responses)


def should_use_fallback(user_message, queue_size=0):
    """
    Determine if we should use fallback instead of OpenAI
    
    Args:
        user_message: User's message
        queue_size: Current queue size
    
    Returns:
        bool: True if should use fallback
    """
    user_lower = user_message.lower()
    
    # Always use fallback for simple greetings
    if user_lower.strip() in ["hi", "hello", "hey", "heya", "sup", "yo"]:
        return True
    
    # Use fallback for crisis (immediate response needed)
    if any(word in user_lower for word in ["suicide", "kill myself", "end it all"]):
        return True
    
    # Use fallback if queue is too long (>5 users waiting)
    if queue_size > 5:
        return True
    
    return False
