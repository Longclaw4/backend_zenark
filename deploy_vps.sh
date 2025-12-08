#!/bin/bash
# ============================================
# VPS Deployment Script for Mental Health Bot
# Run this script on the VPS after SSH login
# ============================================

set -e  # Exit on error

echo "========================================="
echo "  Mental Health Bot - VPS Deployment"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_DIR="/root/app"  # Change this if your app is in a different location
SERVICE_NAME="fastapi"
BRANCH="main"

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check if app directory exists
if [ ! -d "$APP_DIR" ]; then
    print_error "App directory not found: $APP_DIR"
    print_info "Please update APP_DIR variable in this script"
    exit 1
fi

print_info "Navigating to app directory..."
cd "$APP_DIR"
print_success "Current directory: $(pwd)"

# Check git status
print_info "Checking git status..."
git status

# Stash any local changes (if any)
if ! git diff-index --quiet HEAD --; then
    print_info "Stashing local changes..."
    git stash
fi

# Pull latest changes
print_info "Pulling latest changes from $BRANCH..."
if git pull origin "$BRANCH"; then
    print_success "Code updated successfully"
else
    print_error "Failed to pull changes"
    exit 1
fi

# Check if requirements.txt exists and install dependencies
if [ -f "requirements.txt" ]; then
    print_info "Installing/updating dependencies..."
    pip install -r requirements.txt --upgrade
    print_success "Dependencies updated"
else
    print_info "No requirements.txt found, skipping dependency installation"
fi

# Restart the service
print_info "Restarting $SERVICE_NAME service..."
if sudo systemctl restart "$SERVICE_NAME"; then
    print_success "Service restarted successfully"
else
    print_error "Failed to restart service"
    exit 1
fi

# Wait a moment for service to start
sleep 2

# Check service status
print_info "Checking service status..."
if sudo systemctl is-active --quiet "$SERVICE_NAME"; then
    print_success "Service is running!"
    
    # Show last few log lines
    echo ""
    print_info "Last 10 log lines:"
    sudo journalctl -u "$SERVICE_NAME" -n 10 --no-pager
else
    print_error "Service is not running!"
    echo ""
    print_info "Last 20 error logs:"
    sudo journalctl -u "$SERVICE_NAME" -n 20 --no-pager
    exit 1
fi

echo ""
print_success "========================================="
print_success "  Deployment completed successfully!"
print_success "========================================="
echo ""
print_info "Useful commands:"
echo "  - View logs: sudo journalctl -u $SERVICE_NAME -f"
echo "  - Check status: sudo systemctl status $SERVICE_NAME"
echo "  - Restart: sudo systemctl restart $SERVICE_NAME"
echo ""
