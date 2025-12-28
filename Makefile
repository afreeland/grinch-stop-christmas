# CircuitPython Development Makefile
# For macOS - adjust paths for your system

# Find the CIRCUITPY drive (usually mounts as /Volumes/CIRCUITPY)
CIRCUITPY ?= /Volumes/CIRCUITPY

# Find the serial port (adjust pattern if needed)
# Common patterns: /dev/tty.usbmodem*, /dev/tty.usbserial*, /dev/ttyACM*
SERIAL_PORT ?= $(shell ls -1 /dev/tty.usbmodem* /dev/tty.usbserial* /dev/ttyACM* 2>/dev/null | head -1)

# Serial baud rate (CircuitPython default is 115200)
BAUD_RATE ?= 115200

.PHONY: help upload repl monitor ls clean find-port

help:
	@echo "CircuitPython Development Commands:"
	@echo "  make upload      - Copy code.py to CIRCUITPY drive"
	@echo "  make repl        - Open serial REPL (interactive Python)"
	@echo "  make monitor     - Monitor serial output (non-interactive)"
	@echo "  make ls          - List files on CIRCUITPY drive"
	@echo "  make find-port   - Find connected serial port"
	@echo "  make clean       - Remove Python cache files"
	@echo ""
	@echo "Variables (override with VAR=value):"
	@echo "  CIRCUITPY=$(CIRCUITPY)"
	@echo "  SERIAL_PORT=$(SERIAL_PORT)"
	@echo "  BAUD_RATE=$(BAUD_RATE)"

find-port:
	@echo "Searching for serial ports..."
	@ls -1 /dev/tty.usbmodem* /dev/tty.usbserial* /dev/ttyACM* 2>/dev/null || echo "No serial ports found. Is your device connected?"

upload: find-circuitpy
	@echo "Uploading code.py to $(CIRCUITPY)..."
	@cp code.py $(CIRCUITPY)/code.py
	@echo "✓ Upload complete!"
	@echo "The device will automatically restart and run the new code."

find-circuitpy:
	@if [ ! -d "$(CIRCUITPY)" ]; then \
		echo "Error: CIRCUITPY drive not found at $(CIRCUITPY)"; \
		echo "Trying to find it..."; \
		CIRCUITPY_FOUND=$$(ls -d /Volumes/CIRCUITPY* 2>/dev/null | head -1); \
		if [ -n "$$CIRCUITPY_FOUND" ]; then \
			echo "Found at: $$CIRCUITPY_FOUND"; \
			echo "Run: make upload CIRCUITPY=$$CIRCUITPY_FOUND"; \
		else \
			echo "CIRCUITPY drive not found. Is your device connected?"; \
		fi; \
		exit 1; \
	fi

repl: find-serial
	@echo "Opening REPL on $(SERIAL_PORT) at $(BAUD_RATE) baud..."
	@echo ""
	@echo "TO EXIT:"
	@echo "  If using screen: Press Ctrl+A then K, then Y (or Ctrl+A then \\)"
	@echo "  If using cu: Type ~. (tilde then period)"
	@echo "  If using miniterm: Press Ctrl+]"
	@echo ""
	@echo "If stuck, try: Ctrl+C (interrupt), then exit with method above"
	@echo ""
	@screen $(SERIAL_PORT) $(BAUD_RATE) || \
		cu -l $(SERIAL_PORT) -s $(BAUD_RATE) || \
		(miniterm.py $(SERIAL_PORT) $(BAUD_RATE) || echo "Install screen, cu, or pyserial-miniterm")

monitor: find-serial
	@echo "Monitoring serial output on $(SERIAL_PORT) at $(BAUD_RATE) baud..."
	@echo "Press Ctrl+C to exit"
	@screen $(SERIAL_PORT) $(BAUD_RATE) || \
		cu -l $(SERIAL_PORT) -s $(BAUD_RATE) || \
		(miniterm.py $(SERIAL_PORT) $(BAUD_RATE) || echo "Install screen, cu, or pyserial-miniterm")

find-serial:
	@if [ -z "$(SERIAL_PORT)" ] || [ ! -e "$(SERIAL_PORT)" ]; then \
		echo "Error: Serial port not found"; \
		echo "Available ports:"; \
		ls -1 /dev/tty.usbmodem* /dev/tty.usbserial* /dev/ttyACM* 2>/dev/null || echo "  None found"; \
		echo ""; \
		echo "Set SERIAL_PORT manually: make repl SERIAL_PORT=/dev/tty.usbmodem1234"; \
		exit 1; \
	fi

ls: find-circuitpy
	@echo "Files on $(CIRCUITPY):"
	@ls -lah $(CIRCUITPY)/

clean:
	@echo "Cleaning Python cache files..."
	@find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✓ Clean complete"
