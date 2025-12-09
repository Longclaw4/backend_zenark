"""
VPS Active Users Checker
SSH into VPS and check active users from the running backend
"""

# Commands to run on VPS to check active users

# 1. SSH into VPS
ssh root@72.61.170.25
# Password: GenericPassword123#

# 2. Navigate to backend directory
cd /root/Mental_Study_Chat-main

# 3. Check if backend is running
pm2 status

# 4. View backend logs (shows active requests in real-time)
pm2 logs backend --lines 50

# 5. Check MongoDB for active users
python3 << 'EOF'
import os
from datetime import datetime, timedelta
from pymongo import MongoClient

# Get MongoDB URI from environment
MONGO_URI = os.getenv('MONGO_DB_OFFICIAL')
DB_NAME = os.getenv('MONGO_DB_NAME_OFFICIAL', 'zenark_db')

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
chats_col = db["chat_sessions"]

# Active in last 10 minutes
ten_min_ago = datetime.utcnow() - timedelta(minutes=10)
active_users = list(chats_col.aggregate([
    {"$match": {"timestamp": {"$gte": ten_min_ago}}},
    {"$group": {"_id": "$userId"}}
]))

print(f"\n🟢 ACTIVE NOW (Last 10 min): {len(active_users)} users")

# Active today
today = datetime.utcnow().replace(hour=0, minute=0, second=0)
today_users = len(list(chats_col.distinct("userId", {"timestamp": {"$gte": today}})))
print(f"📅 ACTIVE TODAY: {today_users} users")

# Total users
total = len(list(chats_col.distinct("userId")))
print(f"👥 TOTAL USERS: {total} users\n")

client.close()
EOF
