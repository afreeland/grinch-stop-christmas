#!/bin/bash
# Open CircuitPython REPL

SERIAL_PORT="${1:-$(ls -1 /dev/tty.usbmodem* /dev/tty.usbserial* /dev/ttyACM* 2>/dev/null | head -1)}"
BAUD_RATE="${2:-115200}"

if [ -z "$SERIAL_PORT" ] || [ ! -e "$SERIAL_PORT" ]; then
    echo "Error: Serial port not found"
    echo "Available ports:"
    ls -1 /dev/tty.usbmodem* /dev/tty.usbserial* /dev/ttyACM* 2>/dev/null || echo "  None found"
    echo ""
    echo "Usage: ./repl.sh [SERIAL_PORT] [BAUD_RATE]"
    echo "Example: ./repl.sh /dev/tty.usbmodem1234 115200"
    exit 1
fi

echo "Opening REPL on $SERIAL_PORT at $BAUD_RATE baud..."
echo ""
echo "TO EXIT:"
echo "  If using screen: Press Ctrl+A then K, then Y (or Ctrl+A then \\)"
echo "  If using cu: Type ~. (tilde then period)"
echo "  If using miniterm: Press Ctrl+]"
echo ""
echo "If stuck printing dots, try: Ctrl+C (interrupt), then exit method above"
echo ""

# Try screen first, then cu, then miniterm
if command -v screen &> /dev/null; then
    screen "$SERIAL_PORT" "$BAUD_RATE"
elif command -v cu &> /dev/null; then
    cu -l "$SERIAL_PORT" -s "$BAUD_RATE"
elif command -v miniterm.py &> /dev/null; then
    miniterm.py "$SERIAL_PORT" "$BAUD_RATE"
else
    echo "Error: No serial terminal found. Install one of:"
    echo "  - screen (brew install screen)"
    echo "  - cu (brew install cu)"
    echo "  - pyserial (pip install pyserial)"
    exit 1
fi
