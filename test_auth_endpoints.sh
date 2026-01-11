#!/bin/bash

# ============================================
# Authentication Test Script
# Tests all auth endpoints after deployment
# ============================================

echo "=========================================="
echo "  Testing Authentication Endpoints"
echo "=========================================="
echo ""

# Configuration
BASE_URL="http://localhost:8000"
TEST_EMAIL="test_$(date +%s)@example.com"
TEST_PASSWORD="TestPassword123!"
TEST_NAME="Test User"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test counter
PASSED=0
FAILED=0

# Test 1: Signup
echo "Test 1: User Signup"
echo "-------------------"
SIGNUP_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"$TEST_NAME\",
    \"email\": \"$TEST_EMAIL\",
    \"password\": \"$TEST_PASSWORD\",
    \"school\": \"Test School\",
    \"class_name\": \"10A\",
    \"roles\": [\"student\"]
  }")

SIGNUP_CODE=$(echo "$SIGNUP_RESPONSE" | tail -n 1)
SIGNUP_BODY=$(echo "$SIGNUP_RESPONSE" | head -n -1)

if [ "$SIGNUP_CODE" = "200" ]; then
    echo -e "${GREEN}✅ PASS: Signup successful (200)${NC}"
    echo "Response: $SIGNUP_BODY"
    ((PASSED++))
else
    echo -e "${RED}❌ FAIL: Signup failed (HTTP $SIGNUP_CODE)${NC}"
    echo "Response: $SIGNUP_BODY"
    ((FAILED++))
fi
echo ""

# Test 2: Signin
echo "Test 2: User Signin"
echo "-------------------"
SIGNIN_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/auth/signin" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$TEST_EMAIL\",
    \"password\": \"$TEST_PASSWORD\"
  }")

SIGNIN_CODE=$(echo "$SIGNIN_RESPONSE" | tail -n 1)
SIGNIN_BODY=$(echo "$SIGNIN_RESPONSE" | head -n -1)

if [ "$SIGNIN_CODE" = "200" ]; then
    echo -e "${GREEN}✅ PASS: Signin successful (200)${NC}"
    TOKEN=$(echo "$SIGNIN_BODY" | grep -o '"token":"[^"]*"' | cut -d'"' -f4)
    echo "Token received: ${TOKEN:0:50}..."
    ((PASSED++))
else
    echo -e "${RED}❌ FAIL: Signin failed (HTTP $SIGNIN_CODE)${NC}"
    echo "Response: $SIGNIN_BODY"
    ((FAILED++))
    TOKEN=""
fi
echo ""

# Test 3: Invalid Credentials
echo "Test 3: Invalid Credentials"
echo "---------------------------"
INVALID_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/auth/signin" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$TEST_EMAIL\",
    \"password\": \"WrongPassword123!\"
  }")

INVALID_CODE=$(echo "$INVALID_RESPONSE" | tail -n 1)

if [ "$INVALID_CODE" = "401" ]; then
    echo -e "${GREEN}✅ PASS: Invalid credentials rejected (401)${NC}"
    ((PASSED++))
else
    echo -e "${RED}❌ FAIL: Expected 401, got $INVALID_CODE${NC}"
    ((FAILED++))
fi
echo ""

# Test 4: Duplicate Email
echo "Test 4: Duplicate Email"
echo "----------------------"
DUP_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Another User\",
    \"email\": \"$TEST_EMAIL\",
    \"password\": \"AnotherPass123!\",
    \"school\": \"Test School\",
    \"class_name\": \"10B\",
    \"roles\": [\"student\"]
  }")

DUP_CODE=$(echo "$DUP_RESPONSE" | tail -n 1)

if [ "$DUP_CODE" = "400" ]; then
    echo -e "${GREEN}✅ PASS: Duplicate email rejected (400)${NC}"
    ((PASSED++))
else
    echo -e "${RED}❌ FAIL: Expected 400, got $DUP_CODE${NC}"
    ((FAILED++))
fi
echo ""

# Test 5: Signout
echo "Test 5: User Signout"
echo "-------------------"
SIGNOUT_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/auth/signout")

SIGNOUT_CODE=$(echo "$SIGNOUT_RESPONSE" | tail -n 1)

if [ "$SIGNOUT_CODE" = "200" ]; then
    echo -e "${GREEN}✅ PASS: Signout successful (200)${NC}"
    ((PASSED++))
else
    echo -e "${RED}❌ FAIL: Signout failed (HTTP $SIGNOUT_CODE)${NC}"
    ((FAILED++))
fi
echo ""

# Test 6: Change Password (if we have a token)
if [ -n "$TOKEN" ]; then
    echo "Test 6: Change Password"
    echo "----------------------"
    CHANGE_PW_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/auth/changepassword" \
      -H "Content-Type: application/json" \
      -d "{
        \"email\": \"$TEST_EMAIL\",
        \"old_password\": \"$TEST_PASSWORD\",
        \"new_password\": \"NewPassword123!\"
      }")
    
    CHANGE_PW_CODE=$(echo "$CHANGE_PW_RESPONSE" | tail -n 1)
    
    if [ "$CHANGE_PW_CODE" = "200" ]; then
        echo -e "${GREEN}✅ PASS: Password changed (200)${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ FAIL: Password change failed (HTTP $CHANGE_PW_CODE)${NC}"
        ((FAILED++))
    fi
    echo ""
    
    # Test 7: Change Name
    echo "Test 7: Change Name"
    echo "------------------"
    CHANGE_NAME_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/auth/changename" \
      -H "Content-Type: application/json" \
      -d "{
        \"email\": \"$TEST_EMAIL\",
        \"new_name\": \"Updated Test User\",
        \"token\": \"$TOKEN\"
      }")
    
    CHANGE_NAME_CODE=$(echo "$CHANGE_NAME_RESPONSE" | tail -n 1)
    
    if [ "$CHANGE_NAME_CODE" = "200" ]; then
        echo -e "${GREEN}✅ PASS: Name changed (200)${NC}"
        ((PASSED++))
    else
        echo -e "${RED}❌ FAIL: Name change failed (HTTP $CHANGE_NAME_CODE)${NC}"
        ((FAILED++))
    fi
    echo ""
fi

# Summary
echo "=========================================="
echo "  Test Summary"
echo "=========================================="
echo ""
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed!${NC}"
    echo ""
    echo "Authentication is working correctly!"
    echo "You can now use these endpoints in production."
    exit 0
else
    echo -e "${RED}⚠️  Some tests failed!${NC}"
    echo ""
    echo "Please check the logs:"
    echo "  sudo journalctl -u fastapi -n 100"
    exit 1
fi
