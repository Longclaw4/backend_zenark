#!/bin/bash

# Test script for authentication bug
# This script reproduces the signup → signin failure

echo "🧪 Testing Authentication Bug"
echo "=============================="
echo ""

# Configuration
API_BASE="https://service.zenark.in/zenark"
TEST_EMAIL="bugtest_$(date +%s)@example.com"
TEST_PASSWORD="TestPassword123!"
TEST_NAME="Bug Test User"

echo "📧 Test Email: $TEST_EMAIL"
echo "🔐 Test Password: $TEST_PASSWORD"
echo ""

# Step 1: Signup
echo "Step 1: Creating new user via /api/auth/signup"
echo "----------------------------------------------"

SIGNUP_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$API_BASE/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"$TEST_NAME\",
    \"email\": \"$TEST_EMAIL\",
    \"password\": \"$TEST_PASSWORD\",
    \"school\": \"Test School\",
    \"class\": \"10A\",
    \"roles\": [\"student\"]
  }")

SIGNUP_BODY=$(echo "$SIGNUP_RESPONSE" | head -n -1)
SIGNUP_STATUS=$(echo "$SIGNUP_RESPONSE" | tail -n 1)

echo "Response Status: $SIGNUP_STATUS"
echo "Response Body: $SIGNUP_BODY"
echo ""

if [ "$SIGNUP_STATUS" != "200" ]; then
  echo "❌ SIGNUP FAILED - Cannot proceed with signin test"
  exit 1
fi

echo "✅ Signup successful!"
echo ""

# Wait a moment for database to sync
echo "⏳ Waiting 2 seconds for database sync..."
sleep 2
echo ""

# Step 2: Signin
echo "Step 2: Attempting signin with same credentials"
echo "-----------------------------------------------"

SIGNIN_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$API_BASE/api/auth/signin" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$TEST_EMAIL\",
    \"password\": \"$TEST_PASSWORD\"
  }")

SIGNIN_BODY=$(echo "$SIGNIN_RESPONSE" | head -n -1)
SIGNIN_STATUS=$(echo "$SIGNIN_RESPONSE" | tail -n 1)

echo "Response Status: $SIGNIN_STATUS"
echo "Response Body: $SIGNIN_BODY"
echo ""

# Analyze result
echo "=============================="
echo "📊 Test Results"
echo "=============================="

if [ "$SIGNIN_STATUS" = "200" ]; then
  echo "✅ BUG FIXED! Signin successful!"
  echo ""
  echo "Token received:"
  echo "$SIGNIN_BODY" | grep -o '"token":"[^"]*"' || echo "$SIGNIN_BODY"
  exit 0
elif [ "$SIGNIN_STATUS" = "401" ]; then
  echo "⚠️  Signin returned 401 (Unauthorized)"
  echo "This might indicate a password verification issue"
  exit 1
elif [ "$SIGNIN_STATUS" = "500" ]; then
  echo "❌ BUG CONFIRMED! Signin returned 500 error"
  echo ""
  echo "This is the bug we're trying to fix."
  echo "Check backend logs for the error details:"
  echo ""
  echo "  sudo journalctl -u zenark-auth -n 50"
  echo "  # OR"
  echo "  sudo journalctl -u fastapi -n 50 | grep -i signin"
  exit 1
else
  echo "⚠️  Unexpected status code: $SIGNIN_STATUS"
  exit 1
fi
