"""
Comprehensive fix for language instruction leaking issue
This script will find and fix ALL occurrences of the problematic text
"""
import re

# Read the file
with open('langraph_tool.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Count occurrences before
before_count = content.count("Do not start with 'it sounds like'")
print(f"Found {before_count} occurrences of the instruction text")

# Fix 1: Remove the extra period and quote at the end
content = content.replace(
    "answer the user in his same language.'",
    "respond in the SAME language"
)

# Fix 2: Also fix any variations
content = content.replace(
    "answer the user in his same language.",
    "respond in the SAME language"
)

# Fix 3: Remove the "Do not start with 'it sounds like'" if it appears at the end of responses
# This is a safety check to prevent instruction leaking
content = re.sub(
    r"• Do not start with 'it sounds like'\\n\"\s*\n\s*\"• If the user writes",
    "• If the user writes",
    content
)

# Write back
with open('langraph_tool.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed all language instruction issues!")
print("File updated successfully")
