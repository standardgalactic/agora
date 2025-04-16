#!/usr/bin/python3

import sys
import time
import re
import subprocess
import os

CHUNK_SIZE = 500  # characters
SMOOTH_STEPS = 5
SLEEP_PER_CHAR = lambda wpm: 60 / (wpm * 6)  # 6 chars per word

# Simple regex-based code detector
def is_code(text):
    patterns = [
        r"\b(def|class|function|return|var|let|const|import|export|if|else|endif|fi|while|for|foreach)\b",
        r"<\/?\w+>",  # HTML tags
        r"[{}();=<>]",  # common symbols
        r"\b(console\.log|print|echo|System\.out)\b",
        r"^\s*[#$]",  # bash or prompt lines
    ]
    score = sum(len(re.findall(p, text, re.MULTILINE)) for p in patterns)
    symbol_density = len(re.findall(r"[{}();<>=]", text)) / max(1, len(text))
    return score > 4 or symbol_density > 0.02

# Smooth transition between speeds
def interpolate_speeds(start, end, steps):
    if start == end:
        return [start]
    return [int(start + (end - start) * i / steps) for i in range(1, steps + 1)]

# Read file and process
def adaptive_read(file_path):
    with open(file_path, 'r') as f:
        data = f.read()

    chunks = [data[i:i+CHUNK_SIZE] for i in range(0, len(data), CHUNK_SIZE)]

    current_speed = 44  # start slow

    for chunk in chunks:
        target_speed = 550 if is_code(chunk) else 44

        # Interpolate if changing
        if target_speed != current_speed:
            for speed in interpolate_speeds(current_speed, target_speed, SMOOTH_STEPS):
                for c in chunk[:len(chunk)//SMOOTH_STEPS]:
                    sys.stdout.write(c)
                    sys.stdout.flush()
                    time.sleep(SLEEP_PER_CHAR(speed))
            current_speed = target_speed
        else:
            for c in chunk:
                sys.stdout.write(c)
                sys.stdout.flush()
                time.sleep(SLEEP_PER_CHAR(current_speed))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 adaptive_reader.py yourfile.txt")
        sys.exit(1)

    adaptive_read(sys.argv[1])

