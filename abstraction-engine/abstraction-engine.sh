#!/bin/bash

# Define directories and files
INPUT_FILE="$1"
MODE="$2"  # Modes: "adaptive-speed" or "summarize"
TMP_DIR=$(mktemp -d)
CHUNK_SIZE=500  # Characters per chunk
SUMMARY_DIR="./summaries"
PROGRESS_FILE="./progress.log"

# Create necessary directories
mkdir -p "$SUMMARY_DIR" "$TMP_DIR"
touch "$PROGRESS_FILE"

# Split the input file into chunks
split -b $CHUNK_SIZE -d "$INPUT_FILE" "$TMP_DIR/chunk_"

# Process each chunk
for CHUNK in "$TMP_DIR"/chunk_*; do
    TYPE=$(python3 classify-chunk.py "$CHUNK")

    if [ "$TYPE" == "code" ]; then
        if [ "$MODE" == "summarize" ]; then
            python3 summarize-chunk.py "$CHUNK" >> "$SUMMARY_DIR/summary.txt"
        else
            python3 adaptive-throttle.py "$CHUNK" code
        fi
    else
        python3 adaptive-throttle.py "$CHUNK" text
    fi
done

# Cleanup
rm -rf "$TMP_DIR"
