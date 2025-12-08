# Exam Buddy MongoDB Memory Integration Guide

## Problem
Currently, Exam Buddy loses conversation history when:
- User logs out and logs back in
- Server restarts
- Frontend generates a new session_id

## Solution
Use **user_id** (from JWT token) instead of **session_id** to maintain history.

## Backend Changes Needed

### 1. Update the Exam Buddy API Endpoint

The endpoint needs to:
1. Extract `user_id` from JWT token
2. Use `user_id` to retrieve/store conversation history
3. Ignore the frontend's `session_id` for memory purposes

**Example endpoint structure:**
```python
@app.post("/exam_buddy/chat")
async def exam_buddy_chat(request: ExamBuddyRequest):
    # 1. Decode JWT to get user_id
    payload = decode_jwt(request.token)
    user_id = payload.get("id")
    
    # 2. Get MongoDB memory using user_id (NOT session_id)
    from exam_buddy_memory import get_exam_buddy_memory
    memory = await get_exam_buddy_memory(user_id, chats_col)
    
    # 3. Add user message to history
    await memory.add_user_message(request.question)
    
    # 4. Get response from exam buddy
    from exam_buddy import get_exam_buddy_response
    response = await get_exam_buddy_response(
        question=request.question,
        user_id=user_id,  # Use user_id instead of session_id
        context=request.context or ""
    )
    
    # 5. Add AI response to history
    await memory.add_ai_message(response)
    
    return {"response": response}
```

### 2. Update exam_buddy.py

Change `get_exam_buddy_response` to accept `user_id` instead of `session_id`:

```python
async def get_exam_buddy_response(
    question: str,
    user_id: str,  # Changed from session_id
    context: str = "",
    **kwargs
):
    # Use user_id for memory retrieval
    ...
```

### 3. MongoDB Collection Structure

The exam buddy conversations will be stored as:
```json
{
    "user_id": "507f1f77bcf86cd799439011",
    "chat_type": "exam_buddy",
    "messages": [
        {"role": "user", "content": "How do I prepare for JEE?"},
        {"role": "assistant", "content": "Focus on NCERT first..."}
    ],
    "created_at": "2025-12-08T10:00:00Z",
    "updated_at": "2025-12-08T10:05:00Z"
}
```

## Frontend Changes Needed

### Option 1: No Changes Required (Recommended)
- Backend ignores `session_id` and uses `user_id` from JWT
- Frontend can keep sending random `session_id`
- History is maintained via `user_id`

### Option 2: Send user_id explicitly
```javascript
const response = await fetch('/exam_buddy/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
        question: userMessage,
        token: token  // Backend extracts user_id from this
    })
});
```

## Benefits

✅ **Persistent Memory**: History survives logout/login
✅ **Cross-Device**: Same history on mobile/desktop
✅ **Server Restart Safe**: Data in MongoDB, not RAM
✅ **User-Centric**: Each user has their own conversation thread

## Testing

1. Login as User A
2. Chat with exam buddy: "How to prepare for NEET?"
3. Logout
4. Login again as User A
5. Send: "What did we discuss?"
6. Bot should remember the NEET conversation ✅

## Files Created

1. `exam_buddy_memory.py` - MongoDB memory implementation
2. `EXAM_BUDDY_MEMORY_GUIDE.md` - This guide

## Next Steps

Ask your backend developer to:
1. Create the `/exam_buddy/chat` endpoint (or update existing one)
2. Integrate `exam_buddy_memory.py`
3. Use `user_id` from JWT instead of `session_id`
4. Test with the steps above
