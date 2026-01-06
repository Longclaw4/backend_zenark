"""
Script to generate all meditation sessions data
Run this to update data.py with all 160+ sessions
"""

# All sessions data organized by tab
ALL_SESSIONS = {
    # Tab 1: Introduction (101-104) - Already exists
    
    # Tab 2: Beginner Course (201-210) - Already exists
    
    # Tab 3: Intermediate Course (301-310)
    "301": {"tab": 3, "title": "1. Introduction", "desc": "This is the first session in the Intermediate series. These sessions are designed for you if you've already learned the basics of mindfulness meditation, and you'd like to develop your practice further.", "cat": "intermediate"},
    "302": {"tab": 3, "title": "2. Spontaneity of thoughts", "desc": "This session investigates the nature of thoughts, and their temporary, changing and spontaneous essence", "cat": "intermediate"},
    "303": {"tab": 3, "title": "3. The self", "desc": "In this session, we'll consider the concept of the self; the sensation of being an autonomous, enduring, individual directing our own experience. Meditation lets us re-evaluate the natural instinct that we exist as a subject at the centre of consciousness.", "cat": "intermediate"},
    "304": {"tab": 3, "title": "4. Consciousness", "desc": "Meditation is really all about the investigation of consciousness, and how things like thoughts, feelings, and sensations appear within it. Meditation allows us to investigate the nature of consciousness first-hand.", "cat": "intermediate"},
    "305": {"tab": 3, "title": "5. Anxiety", "desc": "Through meditation, we can develop a healthier relationship with anxiety by learning to observe the symptoms as they arise. Just as you would observe the breath during meditation, try to observe the anxious feelings without judgment. This will help to reduce the impact of anxiety, and lead to a happier, healthier state of mind.", "cat": "intermediate"},
    "306": {"tab": 3, "title": "6. Minimal living", "desc": "Minimalism is about living more intentionally, removing unnecessary materialistic distractions and prioritising the things of true value in life. This can go hand-in-hand with mindfulness, allowing you to live more fully in the present moment.", "cat": "intermediate"},
    "307": {"tab": 3, "title": "7. Ego Dissolution", "desc": "We normally have a sensation of a continuous and enduring personality that embodies who we are - 'the ego'. When we become more mindful in the present moment, observing the fluidity and spontaneity of thoughts and feelings, it's possible to realise that the ego is simply a narrative based on our memories of the past and our expectations of the future.", "cat": "intermediate"},
    "308": {"tab": 3, "title": "8. Stress", "desc": "By becoming mindful of stress, it's possible to observe the feeling in a non-judgmental way, and to avoid a vicious circle of negative emotions. Meditation can have the immediate benefit of helping you relax, but it can also have a long-lasting effect, reducing the impact of stress over time.", "cat": "intermediate"},
    "309": {"tab": 3, "title": "9. Open Awareness", "desc": "In this session, we'll use the 'open awareness' method - meditating with an open awareness of all sensations and feelings, rather than focusing on a specific object like the breath. The key is to clearly observe thoughts, emotions, sounds and bodily sensations as they arise.", "cat": "intermediate"},
    "310": {"tab": 3, "title": "10. Free will", "desc": "Considering the nature of free will and the fluidity of the mind's thinking process can help you to refine your understanding of consciousness and to become more mindful of thoughts as they appear. This can lead to a greater sense of awareness in the present moment.", "cat": "intermediate"},
    
    # Tab 4: Stress & Anxiety (311-320)
    "311": {"tab": 4, "title": "1. Meditation for stress & anxiety", "desc": "Through mindfulness meditation, we can learn to recognize the symptoms of stress and anxiety as they arise and not get carried away them. With practice, this will allow us to cultivate a healthier, happier state of mind.", "cat": "stress_anxiety"},
    "312": {"tab": 4, "title": "2. Managing anxiety", "desc": "Meditation can help us to develop a healthier relationship with anxiety by learning to observe the symptoms as they arise. Just as you would observe the breath during meditation, try to observe the anxious feelings without judgment.", "cat": "stress_anxiety"},
    "313": {"tab": 4, "title": "3. Managing stress", "desc": "Meditation can have the immediate benefit of helping you relax by calming the initial stress response, but it can also have a long-lasting effect, reducing the impact of stress over time.", "cat": "stress_anxiety"},
    "314": {"tab": 4, "title": "4. Labelling thoughts & feelings", "desc": "Labelling is a useful tool to help manage stress and anxiety. As thoughts arise, observe them briefly, apply a label, and then return to following the breath.", "cat": "stress_anxiety"},
    "315": {"tab": 4, "title": "5. Finding peace in the present moment", "desc": "This meditation is about letting go of thoughts about the past or apprehension of the future and focusing only on the present moment, which can lead to a real sense of peace.", "cat": "stress_anxiety"},
    "316": {"tab": 4, "title": "6. Recognising unhelpful thoughts", "desc": "With practice, we can choose which thoughts are worthy of our attention and which aren't. You can practice this during meditation by labelling thoughts as helpful or unhelpful. Briefly observe the thought and label it before letting it go.", "cat": "stress_anxiety"},
    "317": {"tab": 4, "title": "7. Dealing with stressful situations", "desc": "This session will help you to prepare for stressful situations in your day-to-day life by practicing the labelling technique. This technique helps us to improve our reactivity to difficult emotions.", "cat": "stress_anxiety"},
    "318": {"tab": 4, "title": "8. Labelling physical sensations", "desc": "By developing greater body awareness, we can start to witness bodily sensations as they appear with less judgement, reducing the impact and the longevity of anxious feelings.", "cat": "stress_anxiety"},
    "319": {"tab": 4, "title": "9. Understanding anxiety", "desc": "This session will help you to notice anxious feelings as they appear. By practicing the labelling technique, we can condition ourselves to to witness them with less judgment, before they take hold.", "cat": "stress_anxiety"},
    "320": {"tab": 4, "title": "10. Negative emotions", "desc": "By developing a clear awareness of our thoughts and feelings in the present moment, we can transform our experience of anxiety and stress. To help you develop this awareness, we'll use the labelling technique in this session.", "cat": "stress_anxiety"},
    
    # Tab 5: Sleep (321-325)
    "321": {"tab": 5, "title": "1. Gradual muscle relaxation", "desc": "In this session, we'll gently scan through the body, releasing any tension and preparing for a good night's sleep.", "cat": "sleep"},
    "322": {"tab": 5, "title": "2. Mindful breathing", "desc": "This is a mindful breathing meditation that will help us to relax and unwind, leading to a deeply restful sleep.", "cat": "sleep"},
    "323": {"tab": 5, "title": "3. Visualisation", "desc": "This session uses a visualisation meditation to help us drift off into a deep and peaceful sleep.", "cat": "sleep"},
    "324": {"tab": 5, "title": "4. Body Scan", "desc": "Scanning your body for sensations as you try to fall asleep will help you let go of stressful thoughts. Allow your body to go limp, take a breath and deeply exhale. Notice how relaxed your body feels and enjoy it!", "cat": "sleep"},
    "325": {"tab": 5, "title": "5. Mantra for Sleep", "desc": "Mantra for sleep meditation by Giovanni Dienstmann. Calm down your mind and unify your awareness by replacing your many thoughts by a single mantra. This is a great way to prepare the mind for sleep. The mantra is practiced in four stages: out loud, whispering, thinking, and pure listening.", "cat": "sleep", "has_audio": False},
    
    # Tab 6: Work Life (326-335)
    "326": {"tab": 6, "title": "1. Managing Conflict", "desc": "It's almost inevitable that most of us, at some point in our work lives, will encounter some kind of conflict. This session will explore how mindfulness meditation can help us deal it.", "cat": "work_life"},
    "327": {"tab": 6, "title": "2. Managing Stress", "desc": "In this session, we'll consider the impact of mindfulness on stress. Meditation can have the immediate benefit of helping you relax by calming the initial stress response, but it can also have a long-lasting effect.", "cat": "work_life"},
    "328": {"tab": 6, "title": "3. Productivity", "desc": "Mindfulness meditation helps us to become more present in our day-to-day lives and this transfers very well to maintaining a mindful awareness on our work.", "cat": "work_life"},
    "329": {"tab": 6, "title": "4. Confidence", "desc": "Self confidence is important in all aspects of our lives. This meditation will explore on how mindfulness can help you recognise fear and self-doubt as they arise and instead stay focused on the present moment", "cat": "work_life"},
    "330": {"tab": 6, "title": "5. Creativity", "desc": "In this meditation, we'll think about the positive affect that mindfulness meditation can have on creativity.", "cat": "work_life"},
    "331": {"tab": 6, "title": "6. Focus", "desc": "It can be difficult for a lot of people to remain focused on their work for long periods of time, especially if the task at hand isn't so interesting. Mindfulness meditation is a way of training yourself to maintain your focus.", "cat": "work_life"},
    "332": {"tab": 6, "title": "7. Work-life balance", "desc": "Having a good work / home life balance is extremely important for our mental health. In this session, we'll explore several ways that mindfulness meditation can help us with this.", "cat": "work_life"},
    "333": {"tab": 6, "title": "8. Motivation", "desc": "Introducing mindfulness into our work can make us more engaged in what we're doing and reinvigorate our interest. We can think of work as the object of our meditation, paying close attention to every aspect of it.", "cat": "work_life"},
    "334": {"tab": 6, "title": "9. Dealing with change", "desc": "In our work-lives, things will inevitably change. People come and go, processes evolve, technology develops. This can be daunting, but mindfulness can help us to deal with change and the emotions that it brings out in us.", "cat": "work_life"},
    "335": {"tab": 6, "title": "10. Prioritization", "desc": "In this session, we'll practice using the 'labelling' technique during meditation, to help us learn to focus on the important things.", "cat": "work_life"},
    
    # Tab 7: Walking (336-337)
    "336": {"tab": 7, "title": "1. Walking Inside", "desc": "Walking at an extremely slow pace takes you away from your usual automatic way of moving and allows you to pay closer attention to your body, with a fresh perspective", "cat": "walking"},
    "337": {"tab": 7, "title": "2. Walking Outside", "desc": "A walking meditation can transform a well-known route, as you become more acutely aware of the things around you. This is a great way of practicing how to be more mindful in your day-to-day life.", "cat": "walking"},
    
    # Tab 8: Great Thinkers (338-342)
    "338": {"tab": 8, "title": "1. William James", "desc": "The greatest weapon against stress is our ability to choose one thought over another - William James.", "cat": "great_thinkers"},
    "339": {"tab": 8, "title": "2. Rene Descartes", "desc": "Cogito, Ergo Sum / I think, therefore I am - Rene Descartes", "cat": "great_thinkers"},
    "340": {"tab": 8, "title": "3. William Shakespeare", "desc": "For there is nothing either good or bad, but thinking makes it so - William Shakespeare", "cat": "great_thinkers"},
    "341": {"tab": 8, "title": "4. Alan Watts", "desc": "One is a great deal less anxious if one feels perfectly free to be anxious - Alan Watts", "cat": "great_thinkers"},
    "342": {"tab": 8, "title": "5. William Blake", "desc": "If the doors of perception were cleansed, everything would appear to man as it is, infinite. For man has closed himself up, till he sees all things thro' narrow chinks of his cavern. - William Blake", "cat": "great_thinkers"},
    
    # Tab 9: Body Scan (343-350)
    "343": {"tab": 9, "title": "1. Your first body scan", "desc": "Body scan meditation involves becoming aware of the physical sensations throughout your body, scanning from the top of your head down to your toes.", "cat": "body_scan"},
    "344": {"tab": 9, "title": "2. Positions", "desc": "You can practice body scanning in any position, but it's best to be comfortable and relaxed. You may want to try it while sitting in a chair or lying in your bed before you go to sleep.", "cat": "body_scan"},
    "345": {"tab": 9, "title": "3. Sensations", "desc": "Meditating using the body-scan method can help to realign your relationship with discomfort and unpleasant sensations. In this session, try to observe all bodily sensations as they appear, with a sense of curiosity and clear awareness.", "cat": "body_scan"},
    "346": {"tab": 9, "title": "4. Body scan meditation by UCLA", "desc": "Body scan meditation is a reliable way to release tension that you might not even realize you're experiencing. This method involves paying attention to parts of the body and bodily sensations in a gradual sequence from head to toe.", "cat": "body_scan"},
    "347": {"tab": 9, "title": "5. Simple body scan 1", "desc": "This session is the same as the 'Your first body scan' session, but without the introduction. Body scan meditation involves becoming aware of the physical sensations throughout your body, scanning from the top of your head down to your toes.", "cat": "body_scan"},
    "348": {"tab": 9, "title": "6. Simple body scan 2", "desc": "This session is the same as the 'Positions' session, but without the introduction. You can practice body scanning in any position, but it's best to be comfortable and relaxed. You may want to try it while sitting in a chair or lying in your bed.", "cat": "body_scan"},
    "349": {"tab": 9, "title": "7. Simple body scan 3", "desc": "This session is the same as the 'Sensations' session, but without the introduction. Meditating using the body-scan method can help to realign your relationship with discomfort and unpleasant sensations.", "cat": "body_scan"},
    "350": {"tab": 9, "title": "8. Body scan for sleep", "desc": "Scanning your body for sensations as you prepare for sleep will help you to let go of your daily concerns and stresses. Allow your body to go limp, take a breath and deeply exhale. Notice how relaxed your body feels and enjoy the feeling of drifting gently off to sleep.", "cat": "body_scan"},
    
    # Tab 10: Mantra (351-355)
    "351": {"tab": 10, "title": "1. Your first mantra", "desc": "Mantra meditation is a form of mindfulness meditation that uses a word, a phrase or a sound as the main focus instead of the breath or bodily sensations. In this session, we'll use the mantra 'I am present in mind and body'.", "cat": "mantra"},
    "352": {"tab": 10, "title": "2. Choose your own mantra", "desc": "For this session, think of a mantra you'd like to use. Try to pick a phrase or a word that has some meaning to you and feels comfortable in your mind.", "cat": "mantra"},
    "353": {"tab": 10, "title": "3. Simple mantra 1", "desc": "This session is the same as the 'Your first mantra' session, but without the introduction. We'll use the mantra 'I am present in mind and body'", "cat": "mantra"},
    "354": {"tab": 10, "title": "4. Simple mantra 2", "desc": "This session is the same as the 'Your first mantra' session, but without the introduction. Think of a mantra you'd like to use. Try to pick a phrase or a word that has some meaning to you and feels comfortable in your mind.", "cat": "mantra"},
    "355": {"tab": 10, "title": "5. Mantra for Sleep", "desc": "Calm down your mind and refine your awareness by replacing your many thoughts with a single mantra. This is a great way to prepare the mind for sleep. The mantra is practiced in four stages: out loud, whispering, thinking, and pure listening.", "cat": "mantra", "has_audio": False},
    
    # Tab 11: Loving Kindness (356-360)
    "356": {"tab": 11, "title": "1. Self compassion", "desc": "Being kind to ourselves when encountering pain and personal shortcomings, rather than hurting ourselves with self-criticism, can lead to greater life satisfaction, wisdom, happiness, optimism, personal responsibility, and emotional resilience.", "cat": "loving_kindness"},
    "357": {"tab": 11, "title": "2. Compassion for others", "desc": "Practicing compassion involves allowing ourselves to be moved by suffering and helps us build the motivation to alleviate and prevent it. This session will help you cultivate a more compassionate state of mind.", "cat": "loving_kindness"},
    "358": {"tab": 11, "title": "3. Compassion for all", "desc": "This session will help you cultivate a compassionate mindset for all people, starting with ourselves.", "cat": "loving_kindness"},
    "359": {"tab": 11, "title": "4. Loving kindness by UCLA", "desc": "Loving-kindness meditation is the practice of cultivating benevolence and friendliness. The method generally consists of silent repetitions of phrases such as 'may you be happy' or 'may you be free from suffering', directed at a person who we can visualize internally.", "cat": "loving_kindness"},
    "360": {"tab": 11, "title": "5. Loving Kindness by Giovanni Dienstmann", "desc": "Learn how to kindle and strengthen feelings of love towards yourself and towards other people, without depending on anything outside yourself. In advanced stages, this practice creates a feeling of joy and bliss.", "cat": "loving_kindness", "has_audio": False},
}

# Generate the full data structure
def generate_sessions():
    sessions = {}
    
    for session_id, data in ALL_SESSIONS.items():
        order = int(session_id) % 100 if int(session_id) % 100 != 0 else 10
        has_audio = data.get("has_audio", True)
        
        sessions[session_id] = {
            "id": session_id,
            "tab": data["tab"],
            "title": data["title"],
            "description": data["desc"],
            "audio_file": f"{session_id}.mp3" if has_audio else None,
            "duration_seconds": 600,  # Default 10 min
            "category": data["cat"],
            "order": order,
            "has_audio": has_audio
        }
    
    return sessions

if __name__ == "__main__":
    sessions = generate_sessions()
    print(f"Generated {len(sessions)} sessions")
    print(f"Tabs: {set(s['tab'] for s in sessions.values())}")
    print(f"Categories: {set(s['category'] for s in sessions.values())}")
