# Grinch Box - CircuitPython Useless Box Project

A CircuitPython project for reading GPIO inputs (microswitch and toggle switch) for a useless box.

## Project Videos

### Completed/Working Version

[![Completed Grinch Box](https://img.youtube.com/vi/qPNQ77u-mzM/0.jpg)](https://youtu.be/qPNQ77u-mzM)

### Behind the Scenes - Progress & Components

[![Behind the Scenes](https://img.youtube.com/vi/nJ25WAER2go/0.jpg)](https://youtu.be/nJ25WAER2go)

## Setup

1. **Connect your CircuitPython device** via USB
2. The device should mount as `/Volumes/CIRCUITPY` (macOS)

## Quick Start

### Upload Code

**Using Makefile:**
```bash
make upload
```

**Using script:**
```bash
chmod +x upload.sh
./upload.sh
```

**Manual:**
```bash
cp code.py /Volumes/CIRCUITPY/code.py
```

### Access REPL (Interactive Python)

**Using Makefile:**
```bash
make repl
```

**Using script:**
```bash
chmod +x repl.sh
./repl.sh
```

**Manual (using screen):**
```bash
screen /dev/tty.usbmodem1234 115200
# To exit: Press Ctrl+A then K, then Y (or Ctrl+A then \)
```

**Manual (using cu):**
```bash
cu -l /dev/tty.usbmodem1234 -s 115200
# To exit: Type ~. (tilde then period)
```

### Monitor Serial Output (Non-interactive)

**Using Makefile:**
```bash
make monitor
```

This will show the output from your `code.py` program (state changes, print statements, etc.)

## Finding Your Serial Port

The Makefile will try to auto-detect your serial port, but you can find it manually:

```bash
# List available serial ports
ls /dev/tty.usbmodem* /dev/tty.usbserial* /dev/ttyACM*

# Or use the Makefile helper
make find-port
```

Common port names on macOS:
- `/dev/tty.usbmodem*` (most CircuitPython boards)
- `/dev/tty.usbserial*` (some USB-to-serial adapters)
- `/dev/ttyACM*` (Linux-style, less common on macOS)

## Installing Serial Tools (if needed)

**screen** (recommended, usually pre-installed on macOS):
```bash
# Usually already installed, but if not:
brew install screen
```

**cu** (alternative):
```bash
brew install cu
```

**pyserial** (Python-based):
```bash
pip install pyserial
# Then use: python -m serial.tools.miniterm /dev/tty.usbmodem1234 115200
```

## Makefile Commands

- `make upload` - Copy code.py to CIRCUITPY drive
- `make repl` - Open serial REPL (interactive Python)
- `make monitor` - Monitor serial output (non-interactive)
- `make ls` - List files on CIRCUITPY drive
- `make find-port` - Find connected serial port
- `make clean` - Remove Python cache files
- `make help` - Show all commands

## Override Variables

If your device uses different paths, you can override:

```bash
make upload CIRCUITPY=/Volumes/MYBOARD
make repl SERIAL_PORT=/dev/tty.usbmodem5678
make monitor BAUD_RATE=9600
```

## Wiring

- **GPIO 4 (Microswitch)**: One terminal to GPIO 4, other to GND
- **GPIO 5 (Toggle Switch)**: Configure based on your 6-pin switch wiring

## Troubleshooting

**"CIRCUITPY drive not found"**
- Make sure your device is connected via USB
- Check that it's mounted: `ls /Volumes/CIRCUITPY*`
- Some boards need to be put into bootloader mode first

**"Serial port not found"**
- Make sure your device is connected
- Check available ports: `ls /dev/tty.*`
- Try unplugging and replugging the USB cable
- Some boards need drivers installed

**"Permission denied" on serial port**
- You may need to add your user to the dialout group (Linux)
- On macOS, you might need to grant Terminal/iTerm full disk access

**Stuck in REPL / Only printing dots**
- If you're stuck and only seeing '.' characters:
  1. Press **Ctrl+C** to interrupt (may need to press a few times)
  2. Then exit using the method for your terminal:
     - **screen**: Press `Ctrl+A` then `K`, then `Y` (or `Ctrl+A` then `\`)
     - **cu**: Type `~.` (tilde then period)
     - **miniterm**: Press `Ctrl+]`
- If still stuck, you can force-kill the terminal:
  - Find the process: `ps aux | grep screen` (or `cu` or `miniterm`)
  - Kill it: `kill -9 <PID>`
  - Or just close the terminal window and open a new one
