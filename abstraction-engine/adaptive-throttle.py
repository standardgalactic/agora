import sys
import time

def throttle(content, base_speed, target_speed, gradual=False):
    """Simulate throttled output, with gradual speed adjustment if required."""
    step_count = 50  # Number of steps for gradual adjustment
    if gradual:
        step_increment = (target_speed - base_speed) / step_count
    else:
        step_increment = 0

    current_speed = base_speed
    for char in content:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(1 / (current_speed * 60))  # Convert words/minute to delay/character

        if gradual and current_speed < target_speed:
            current_speed += step_increment

# Load the chunk
with open(sys.argv[1], 'r') as f:
    chunk = f.read()

# Determine the speed
mode = sys.argv[2]  # "code" or "text"
if mode == "code":
    throttle(chunk, base_speed=44, target_speed=550, gradual=True)
else:
    throttle(chunk, base_speed=44, target_speed=44, gradual=False)
