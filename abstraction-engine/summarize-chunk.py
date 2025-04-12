import sys
import subprocess

# Load the chunk
with open(sys.argv[1], 'r') as f:
    chunk = f.read()

# Summarize the chunk
prompt = f"Summarize the following code in detail:\n\n{chunk}"
result = subprocess.run(
    ["ollama", "run", "phi", prompt],
    capture_output=True,
    text=True
)

# Print the summary
print(result.stdout.strip())
