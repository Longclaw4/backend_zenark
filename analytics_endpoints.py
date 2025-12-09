"""
Add this endpoint to langraph_tool.py to track active users in real-time
"""

# Add this to your langraph_tool.py file (after other endpoints)

@app.get("/analytics/active_users")
async def get_active_users():
    """Get real-time active user count"""
    try:
        if chats_col is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        from datetime import datetime, timedelta
        
        # Active in last 10 minutes
        ten_minutes_ago = datetime.utcnow() - timedelta(minutes=10)
        
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
                    "messages_count": {"$sum": 1}
                }
            }
        ]
        
        active_users = await chats_col.aggregate(pipeline).to_list(length=None)
        
        # Active in last hour
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        pipeline_hour = [
            {
                "$match": {
                    "timestamp": {"$gte": one_hour_ago}
                }
            },
            {
                "$group": {
                    "_id": "$userId"
                }
            },
            {
                "$count": "users_last_hour"
            }
        ]
        
        result_hour = await chats_col.aggregate(pipeline_hour).to_list(length=1)
        users_last_hour = result_hour[0]['users_last_hour'] if result_hour else 0
        
        # Today's users
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        pipeline_today = [
            {
                "$match": {
                    "timestamp": {"$gte": today_start}
                }
            },
            {
                "$group": {
                    "_id": "$userId"
                }
            },
            {
                "$count": "users_today"
            }
        ]
        
        result_today = await chats_col.aggregate(pipeline_today).to_list(length=1)
        users_today = result_today[0]['users_today'] if result_today else 0
        
        return JSONResponse(content={
            "active_now": len(active_users),  # Last 10 minutes
            "active_last_hour": users_last_hour,
            "active_today": users_today,
            "timestamp": datetime.utcnow().isoformat(),
            "details": [
                {
                    "user_id": str(user["_id"]),
                    "last_activity": user["last_activity"].isoformat(),
                    "messages": user["messages_count"]
                }
                for user in active_users
            ]
        })
        
    except Exception as e:
        logging.error(f"Error getting active users: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analytics/dashboard")
async def analytics_dashboard():
    """Complete analytics dashboard"""
    try:
        if chats_col is None or reports_col is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        from datetime import datetime, timedelta
        
        # Total users
        total_users = len(await chats_col.distinct("userId"))
        
        # Total conversations
        total_conversations = await chats_col.count_documents({})
        
        # Total reports generated
        total_reports = await reports_col.count_documents({})
        
        # Active users (last 24 hours)
        yesterday = datetime.utcnow() - timedelta(hours=24)
        active_24h = len(await chats_col.distinct("userId", {"timestamp": {"$gte": yesterday}}))
        
        # Peak usage time (group by hour)
        pipeline_hourly = [
            {
                "$match": {
                    "timestamp": {"$gte": datetime.utcnow() - timedelta(days=7)}
                }
            },
            {
                "$group": {
                    "_id": {
                        "hour": {"$hour": "$timestamp"}
                    },
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"count": -1}
            },
            {
                "$limit": 5
            }
        ]
        
        peak_hours = await chats_col.aggregate(pipeline_hourly).to_list(length=5)
        
        return JSONResponse(content={
            "total_users": total_users,
            "total_conversations": total_conversations,
            "total_reports": total_reports,
            "active_last_24h": active_24h,
            "peak_hours": [
                {
                    "hour": f"{item['_id']['hour']:02d}:00",
                    "activity_count": item['count']
                }
                for item in peak_hours
            ],
            "timestamp": datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Error getting analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))
