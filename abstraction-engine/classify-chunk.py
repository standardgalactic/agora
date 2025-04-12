import sys
import subprocess
import re

def quick_heuristics(text):
    """Quick regex-based heuristics to identify code."""
    code_keywords = ['function', 'var', 'const', 'class', 'def', 'import', 'public', 'private', '<html>', '</', '{', '}']
    if any(kw in text for kw in code_keywords):
        return True
    if re.search(r'[{<>}();=]', text) and len(text) < 1000:
        return True
    return False

def classify_with_phi(text):
    """Use phi-4 to classify the text."""
    prompt = f"Is the following text mostly code? Answer only 'yes' or 'no'.\n\n{text}"
    result = subprocess.run(
        ["ollama", "run", "phi", prompt],
        capture_output=True,
        text=True
    )
    return "yes" in result.stdout.lower()

# Load text from the file
with open(sys.argv[1], 'r') as f:
    chunk = f.read()

# Classify the chunk
if quick_heuristics(chunk):
    print("code")
elif classify_with_phi(chunk):
    print("code")
else:
    print("text")
