#!/bin/bash
# ============================================
# Quick Deployment Script for Journaling Feature
# Run this after pushing to GitHub
# ============================================

echo "========================================="
echo "  Journaling Feature - Quick Deploy"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Step 1: Pulling latest code...${NC}"
cd /root/app
git pull origin main

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Code pulled successfully${NC}"
else
    echo "✗ Failed to pull code"
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 2: Restarting FastAPI service...${NC}"
sudo systemctl restart fastapi

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Service restarted${NC}"
else
    echo "✗ Failed to restart service"
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 3: Waiting for service to start...${NC}"
sleep 3

echo ""
echo -e "${YELLOW}Step 4: Checking service status...${NC}"
sudo systemctl is-active --quiet fastapi

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Service is running${NC}"
else
    echo "✗ Service is not running"
    echo "Check logs: sudo journalctl -u fastapi -n 50"
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 5: Testing journaling endpoint...${NC}"
response=$(curl -s http://localhost:8000/journal/daily-prompt)

if echo "$response" | grep -q "success"; then
    echo -e "${GREEN}✓ Journaling endpoints are working!${NC}"
    echo "Response: $response"
else
    echo "✗ Journaling endpoint test failed"
    echo "Response: $response"
fi

echo ""
echo -e "${YELLOW}Step 6: Checking logs for journaling initialization...${NC}"
sudo journalctl -u fastapi -n 20 --no-pager | grep -i journaling

echo ""
echo "========================================="
echo -e "${GREEN}  Deployment Complete!${NC}"
echo "========================================="
echo ""
echo "Useful commands:"
echo "  - View logs: sudo journalctl -u fastapi -f"
echo "  - Check status: sudo systemctl status fastapi"
echo "  - Test endpoint: curl http://localhost:8000/journal/daily-prompt"
echo ""
