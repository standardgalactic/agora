#!/usr/bin/python3

import sys
import re

with open(sys.argv[1], 'r') as f:
    text = f.read()

# Code keyword patterns (expand this over time)
code_keywords = [
    r"\b(def|function|return|class|const|let|var|import|export|if|else|for|while|try|catch|#include|public|private)\b",
    r"<\/?\w+>",  # HTML tags
    r"[{}<>();=]",  # syntax symbols
    r"^\s*(\$|#|>>>|\.\.\.)",  # shell, python prompts
    r"\b(console\.log|print|echo|System\.out\.println)\b",
]

# Heuristic: count matching patterns
score = 0
for pattern in code_keywords:
    matches = re.findall(pattern, text, re.MULTILINE)
    score += len(matches)

symbol_ratio = len(re.findall(r"[{}();<>=]", text)) / max(1, len(text))
if symbol_ratio > 0.02:
    score += 1

# Threshold: tweak this!
if score >= 5:
    print("code")
else:
    print("text")

