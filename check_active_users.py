"""
Check active users - Manual MongoDB connection
Run this and enter your MongoDB URI when prompted
"""

from datetime import datetime, timedelta
from pymongo import MongoClient

def check_active_users():
    """Check how many unique students are active"""
    
    # PASTE YOUR MONGODB URI HERE (from Render dashboard)
    MONGO_URI = input("Enter MongoDB URI (from Render): ").strip()
    DB_NAME = input("Enter Database Name (default: zenark_db): ").strip() or "zenark_db"
    
    print("\n🔄 Connecting to MongoDB...")
    
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        chats_col = db["chat_sessions"]
        
        # Test connection
        client.server_info()
        print("✅ Connected successfully!\n")
        
        # Get timestamp for 10 minutes ago
        ten_minutes_ago = datetime.utcnow() - timedelta(minutes=10)
        
        print("="*50)
        print("📊 ZENARK ACTIVE USERS DASHBOARD")
        print("="*50)
        
        # Count unique users with activity in last 10 minutes
        pipeline = [
            {
                "$match": {
                    "timestamp": {"$gte": ten_minutes_ago}
                }
            },
            {
                "$group": {
                    "_id": "$userId",
                    "last_activity": {"$max": "$timestamp"},
                    "session_count": {"$sum": 1}
                }
            }
        ]
        
        active_users = list(chats_col.aggregate(pipeline))
        
        print(f"\n🟢 ACTIVE NOW (Last 10 min): {len(active_users)} users")
        
        if active_users:
            print("\nActive Users:")
            for i, user in enumerate(active_users[:10], 1):
                user_id = str(user['_id'])[:8] + "..."
                last_seen = user['last_activity'].strftime("%H:%M:%S")
                print(f"  {i}. User {user_id} - Last seen: {last_seen}")
            
            if len(active_users) > 10:
                print(f"  ... and {len(active_users) - 10} more")
        
        # Last hour
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        users_last_hour = len(list(chats_col.distinct("userId", {"timestamp": {"$gte": one_hour_ago}})))
        print(f"\n🔵 ACTIVE (Last 1 hour): {users_last_hour} users")
        
        # Today
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        users_today = len(list(chats_col.distinct("userId", {"timestamp": {"$gte": today_start}})))
        print(f"\n📅 ACTIVE TODAY: {users_today} users")
        
        # Total all-time
        total_users = len(list(chats_col.distinct("userId")))
        print(f"\n👥 TOTAL USERS (All Time): {total_users} users")
        
        # Total conversations
        total_conversations = chats_col.count_documents({})
        print(f"💬 TOTAL CONVERSATIONS: {total_conversations}")
        
        print("\n" + "="*50)
        print(f"⏰ Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
        print("="*50 + "\n")
        
        client.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check MongoDB URI is correct")
        print("2. Make sure IP is whitelisted in MongoDB Atlas")
        print("3. Verify database name is correct")

if __name__ == "__main__":
    check_active_users()
