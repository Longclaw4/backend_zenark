"""
Add this to your langraph_tool.py on VPS
Then access: http://72.61.170.25:8000/analytics/active_users
"""

# Add this endpoint to langraph_tool.py (before if __name__ == "__main__")

@app.get("/analytics/active_users")
async def get_active_users():
    """Get real-time active user count - NO AUTH REQUIRED"""
    try:
        if chats_col is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        from datetime import datetime, timedelta
        
        # Active in last 10 minutes
        ten_minutes_ago = datetime.utcnow() - timedelta(minutes=10)
        
        pipeline_10min = [
            {"$match": {"timestamp": {"$gte": ten_minutes_ago}}},
            {"$group": {"_id": "$userId", "last_activity": {"$max": "$timestamp"}}},
            {"$count": "active_now"}
        ]
        
        result_10min = await chats_col.aggregate(pipeline_10min).to_list(length=1)
        active_now = result_10min[0]['active_now'] if result_10min else 0
        
        # Active in last hour
        one_hour_ago = datetime.utcnow() - timedelta(hours=1)
        users_last_hour = len(await chats_col.distinct("userId", {"timestamp": {"$gte": one_hour_ago}}))
        
        # Active today
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        users_today = len(await chats_col.distinct("userId", {"timestamp": {"$gte": today_start}}))
        
        # Total all-time
        total_users = len(await chats_col.distinct("userId"))
        
        # Total conversations
        total_conversations = await chats_col.count_documents({})
        
        return JSONResponse(content={
            "status": "success",
            "active_now": active_now,
            "active_last_hour": users_last_hour,
            "active_today": users_today,
            "total_users": total_users,
            "total_conversations": total_conversations,
            "timestamp": datetime.utcnow().isoformat(),
            "server": "VPS 72.61.170.25"
        })
        
    except Exception as e:
        logging.error(f"Error getting active users: {e}")
        return JSONResponse(content={
            "status": "error",
            "error": str(e)
        }, status_code=500)


@app.get("/analytics/dashboard")
async def analytics_dashboard():
    """Complete analytics dashboard - NO AUTH REQUIRED"""
    try:
        if chats_col is None or reports_col is None:
            raise HTTPException(status_code=500, detail="Database not initialized")
        
        from datetime import datetime, timedelta
        
        # Get various metrics
        total_users = len(await chats_col.distinct("userId"))
        total_conversations = await chats_col.count_documents({})
        total_reports = await reports_col.count_documents({})
        
        # Active users last 24h
        yesterday = datetime.utcnow() - timedelta(hours=24)
        active_24h = len(await chats_col.distinct("userId", {"timestamp": {"$gte": yesterday}}))
        
        # Peak hours (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        pipeline_hourly = [
            {"$match": {"timestamp": {"$gte": week_ago}}},
            {"$group": {
                "_id": {"hour": {"$hour": "$timestamp"}},
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]
        
        peak_hours = await chats_col.aggregate(pipeline_hourly).to_list(length=5)
        
        # Average distress score
        pipeline_avg_score = [
            {"$match": {"score": {"$exists": True}}},
            {"$group": {"_id": None, "avg_score": {"$avg": "$score"}}}
        ]
        
        avg_score_result = await reports_col.aggregate(pipeline_avg_score).to_list(length=1)
        avg_score = round(avg_score_result[0]['avg_score'], 2) if avg_score_result else 0
        
        return JSONResponse(content={
            "status": "success",
            "metrics": {
                "total_users": total_users,
                "total_conversations": total_conversations,
                "total_reports": total_reports,
                "active_last_24h": active_24h,
                "average_distress_score": avg_score
            },
            "peak_hours": [
                {
                    "hour": f"{item['_id']['hour']:02d}:00",
                    "activity_count": item['count']
                }
                for item in peak_hours
            ],
            "timestamp": datetime.utcnow().isoformat(),
            "server": "VPS 72.61.170.25"
        })
        
    except Exception as e:
        logging.error(f"Error getting analytics: {e}")
        return JSONResponse(content={
            "status": "error",
            "error": str(e)
        }, status_code=500)
