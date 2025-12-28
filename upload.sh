#!/bin/bash
# Simple upload script for CircuitPython

CIRCUITPY="${1:-/Volumes/CIRCUITPY}"

if [ ! -d "$CIRCUITPY" ]; then
    echo "Error: CIRCUITPY drive not found at $CIRCUITPY"
    echo "Trying to find it..."
    CIRCUITPY_FOUND=$(ls -d /Volumes/CIRCUITPY* 2>/dev/null | head -1)
    if [ -n "$CIRCUITPY_FOUND" ]; then
        echo "Found at: $CIRCUITPY_FOUND"
        CIRCUITPY="$CIRCUITPY_FOUND"
    else
        echo "CIRCUITPY drive not found. Is your device connected?"
        exit 1
    fi
fi

echo "Uploading code.py to $CIRCUITPY..."
cp code.py "$CIRCUITPY/code.py"
echo "✓ Upload complete!"
