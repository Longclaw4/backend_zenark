"""
Meditation session data and metadata
"""

MEDITATION_SESSIONS = {
    # Tab 1: Introduction to Meditation
    "101": {
        "id": "101",
        "tab": 1,
        "title": "What is mindfulness?",
        "description": "Mindfulness is about observing thoughts and feelings without getting caught up in them. It's about learning to live in the present moment rather than the past or future. It's about living in the 'now.'",
        "audio_file": "101.mp3",
        "duration_seconds": 120,  # ~2 min
        "category": "introduction",
        "order": 1
    },
    "102": {
        "id": "102",
        "tab": 1,
        "title": "What is meditation?",
        "description": "When we meditate, we are concerned only by the now. The past is a memory, and the future is an expectation. We are entirely in the present, where reality is.",
        "audio_file": "102.mp3",
        "duration_seconds": 150,  # ~2.5 min
        "category": "introduction",
        "order": 2
    },
    "103": {
        "id": "103",
        "tab": 1,
        "title": "Is it for me?",
        "description": "There are many forms of meditation, and not all styles are for everyone. There isn't a 'right' or a 'wrong' way to meditate, the key thing is finding a practice that suits you.",
        "audio_file": "103.mp3",
        "duration_seconds": 130,  # ~2 min
        "category": "introduction",
        "order": 3
    },
    "104": {
        "id": "104",
        "tab": 1,
        "title": "Setup",
        "description": "You don't need any special place, position or props to meditate. Find a comfortable, position where you can feel relaxed but alert. Close your eyes, and take some deep breaths…",
        "audio_file": "104.mp3",
        "duration_seconds": 210,  # ~3.5 min
        "category": "introduction",
        "order": 4
    },
    
    # Tab 2: Beginner Meditation Course
    "201": {
        "id": "201",
        "tab": 2,
        "title": "1. Your first session",
        "description": "This is the first session in the Beginner pack, which will give you an introduction to mindfulness meditation, and will help you to start a regular practice.",
        "audio_file": "201.mp3",
        "duration_seconds": 600,  # ~10 min
        "category": "beginner_course",
        "order": 1
    },
    "202": {
        "id": "202",
        "tab": 2,
        "title": "2. Mindfulness",
        "description": "Mindfulness is the practice of developing your awareness of the present moment. By consciously noticing our thoughts, feelings and experiences, moment by moment, we can change the way we see ourselves and the world.",
        "audio_file": "202.mp3",
        "duration_seconds": 600,  # ~10 min
        "category": "beginner_course",
        "order": 2
    },
    "203": {
        "id": "203",
        "tab": 2,
        "title": "3. Vipassana",
        "description": "Mindfulness meditation has its roots in the ancient Buddhist tradition of Vipassana, which can be translated roughly as 'clear seeing'. It uses techniques to develop awareness and clarity in the present moment.",
        "audio_file": "203.mp3",
        "duration_seconds": 600,  # ~10 min
        "category": "beginner_course",
        "order": 3
    },
    "204": {
        "id": "204",
        "tab": 2,
        "title": "4. Non-judgment",
        "description": "This session introduces the concept of non-judgment - observing thoughts and feelings as they arise, without judging them. The aim isn't to push thoughts away, or to clear your mind. It is to witness them clearly, without becoming too attached to them.",
        "audio_file": "204.mp3",
        "duration_seconds": 600,  # ~10 min
        "category": "beginner_course",
        "order": 4
    },
    "205": {
        "id": "205",
        "tab": 2,
        "title": "5. Mindful Living",
        "description": "You can incorporate mindfulness into your daily life, not just into your meditation routine. The key is to become fully aware of your experiences in the present moment. Feel bodily sensations, notice the sounds around you, and observe thoughts and feelings as they come and go.",
        "audio_file": "205.mp3",
        "duration_seconds": 600,  # ~10 min
        "category": "beginner_course",
        "order": 5
    },
    "206": {
        "id": "206",
        "tab": 2,
        "title": "6. Science of meditation",
        "description": "In this session, we'll consider the science behind meditation. Meditation has been shown to increase brain matter in the hippocampus, improve memory, increase density in the pre-frontal cortex, improve problem solving and regulation of emotions, and shrink the amygdala, reducing anxiety and stress.",
        "audio_file": "206.mp3",
        "duration_seconds": 600,  # ~10 min
        "category": "beginner_course",
        "order": 6
    },
    "207": {
        "id": "207",
        "tab": 2,
        "title": "7. The present moment",
        "description": "Mindfulness is all about grounding ourselves in the present moment. We tend to live our lives ruminating on the past or planning for the future. When we become aware of our thoughts in the present moment, we can learn to let them go, instead of getting endlessly caught up in them.",
        "audio_file": "207.mp3",
        "duration_seconds": 600,  # ~10 min
        "category": "beginner_course",
        "order": 7
    },
    "208": {
        "id": "208",
        "tab": 2,
        "title": "8. Negative emotions",
        "description": "Mindfulness can help us to manage difficult emotions more effectively. By learning to become aware of thoughts and feelings as they arise, we can transform our relationship with negative emotions, allowing us to process them in a healthier way.",
        "audio_file": "208.mp3",
        "duration_seconds": 600,  # ~10 min
        "category": "beginner_course",
        "order": 8
    },
    "209": {
        "id": "209",
        "tab": 2,
        "title": "9. Sounds",
        "description": "In this session, instead of using the breath as the point of focus, we will use sounds. Pay close attention to every detail of sounds as they arise. If you get distracted by thinking, just notice the thought and return to a careful, open awareness of the sounds around you.",
        "audio_file": "209.mp3",
        "duration_seconds": 600,  # ~10 min
        "category": "beginner_course",
        "order": 9
    },
    "210": {
        "id": "210",
        "tab": 2,
        "title": "10. Conclusion",
        "description": "This is the final session in the zen beginner series. Whether you've completed these sessions in 1 week, 2 weeks or 1 month, the important thing is that you're learning a practice that you'll be able to benefit from for a lifetime.",
        "audio_file": "210.mp3",
        "duration_seconds": 600,  # ~10 min
        "category": "beginner_course",
        "order": 10
    }
}


def get_all_sessions():
    """Get all meditation sessions"""
    return list(MEDITATION_SESSIONS.values())


def get_session_by_id(session_id: str):
    """Get a specific meditation session by ID"""
    return MEDITATION_SESSIONS.get(session_id)


def get_sessions_by_tab(tab: int):
    """Get all sessions for a specific tab"""
    return [s for s in MEDITATION_SESSIONS.values() if s["tab"] == tab]


def get_sessions_by_category(category: str):
    """Get all sessions for a specific category"""
    return [s for s in MEDITATION_SESSIONS.values() if s["category"] == category]
