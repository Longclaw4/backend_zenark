"""
Quick script to fix the language instruction syntax error in langraph_tool.py
"""

# Read the file
with open('langraph_tool.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the problematic line - remove the extra .' at the end
old_text = "answer the user in his same language.'"
new_text = "respond in the SAME language"

# Replace all occurrences
fixed_content = content.replace(old_text, new_text)

# Write back
with open('langraph_tool.py', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("✅ Fixed language instruction syntax errors!")
print(f"Replaced {content.count(old_text)} occurrences")
