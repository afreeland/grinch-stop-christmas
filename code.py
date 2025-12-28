"""
CircuitPython Useless Box
Reads GPIO 4 (toggle switch) and GPIO 5 (microswitch)
Controls DC motor on GPIO 14 and GPIO 15

Wiring Notes:
- GPIO 4 (Toggle Switch): 6-pin 3-state toggle switch
- GPIO 5 (Microswitch): Roller style microswitch
- GPIO 14 & 15: DC motor direction control (R_en and L_en are hardwired HIGH)
"""

import board
import digitalio
import time
import random

# ============================================================================
# GPIO Configuration
# ============================================================================

# GPIO 4 - Toggle Switch (was labeled as microswitch, but is actually toggle)
toggle_switch = digitalio.DigitalInOut(board.GP4)
toggle_switch.direction = digitalio.Direction.INPUT
toggle_switch.pull = digitalio.Pull.UP

# GPIO 5 - Microswitch (was labeled as toggle switch, but is actually microswitch)
microswitch = digitalio.DigitalInOut(board.GP5)
microswitch.direction = digitalio.Direction.INPUT
microswitch.pull = digitalio.Pull.UP  # Internal pull-up: LOW when pressed

# Motor speed control using pulse-width modulation (time-based)
# Set USE_SPEED_CONTROL to False for full speed, True for controlled speed
USE_SPEED_CONTROL = True  # Set to True to enable slower speed

# Adjust these values to control motor speed (only used if USE_SPEED_CONTROL = True)
MOTOR_ON_TIME = 0.008   # Time motor is ON (seconds) - lower = slower
MOTOR_OFF_TIME = 0.025  # Time motor is OFF (seconds) - higher = slower
# Effective speed = MOTOR_ON_TIME / (MOTOR_ON_TIME + MOTOR_OFF_TIME)
# Example: 0.008 / (0.008 + 0.025) = ~24% speed (slower than before)

# Random delay before motor starts (after toggle is turned on)
DELAY_MIN = 0.5   # Minimum delay in seconds
DELAY_MAX = 1.5   # Maximum delay in seconds

# GPIO 14 & 15 - DC Motor Direction Control
motor_pin_a = digitalio.DigitalInOut(board.GP14)
motor_pin_a.direction = digitalio.Direction.OUTPUT
motor_pin_a.value = False

motor_pin_b = digitalio.DigitalInOut(board.GP15)
motor_pin_b.direction = digitalio.Direction.OUTPUT
motor_pin_b.value = False

# Motor state tracking for pulse-width control
motor_pulse_state = False
motor_pulse_last_time = 0

# ============================================================================
# State Machine
# ============================================================================

# States for the useless box
IDLE = "IDLE"              # Motor stopped, waiting
EXTENDING = "EXTENDING"     # Motor forward (extending finger)
RETRACTING = "RETRACTING"  # Motor reverse (retracting finger)

current_state = IDLE

# Current switch states
toggle_state = None
microswitch_state = None

# Previous states for change detection
prev_toggle_state = None
prev_microswitch_state = None

# ============================================================================
# Switch Reading Functions
# ============================================================================

def read_toggle_switch():
    """
    Read toggle switch on GPIO 4
    Returns: True if HIGH, False if LOW
    """
    return toggle_switch.value

def read_microswitch():
    """
    Read microswitch on GPIO 5
    Returns: True if pressed, False if released
    Note: Logic may need to be adjusted based on wiring
    """
    # With pull-up: LOW when pressed, HIGH when released
    # So: not value = True when pressed (LOW), False when released (HIGH)
    # BUT: If switch shows PRESSED when not pressed, it's likely NC or wired differently
    # Try direct reading: HIGH = pressed, LOW = released
    return microswitch.value  # Direct: HIGH = pressed, LOW = released
    # If this doesn't work, try: return not microswitch.value

def read_microswitch_raw():
    """Get raw GPIO value for debugging"""
    return microswitch.value

def get_toggle_state():
    """
    Get toggle switch state as string
    Returns: "HIGH" or "LOW"
    """
    return "HIGH" if read_toggle_switch() else "LOW"

def get_microswitch_state():
    """
    Get microswitch state as string
    Returns: "PRESSED" or "RELEASED"
    """
    return "PRESSED" if read_microswitch() else "RELEASED"

# ============================================================================
# Motor Control Functions
# ============================================================================

def motor_stop():
    """Stop the motor (both pins LOW)"""
    motor_pin_a.value = False
    motor_pin_b.value = False

def motor_forward():
    """Run motor forward direction (extending arm)"""
    motor_pin_a.value = False
    motor_pin_b.value = True

def motor_reverse():
    """Run motor reverse direction (retracting arm)"""
    motor_pin_a.value = True
    motor_pin_b.value = False

def motor_forward_pulsed():
    """Run motor forward with pulse-width modulation for speed control"""
    global motor_pulse_state, motor_pulse_last_time
    current_time = time.monotonic()
    
    if current_time - motor_pulse_last_time >= (MOTOR_ON_TIME if motor_pulse_state else MOTOR_OFF_TIME):
        motor_pulse_state = not motor_pulse_state
        motor_pulse_last_time = current_time
        if motor_pulse_state:
            motor_pin_a.value = False
            motor_pin_b.value = True
        else:
            motor_pin_a.value = False
            motor_pin_b.value = False

def motor_reverse_pulsed():
    """Run motor reverse with pulse-width modulation for speed control"""
    global motor_pulse_state, motor_pulse_last_time
    current_time = time.monotonic()
    
    if current_time - motor_pulse_last_time >= (MOTOR_ON_TIME if motor_pulse_state else MOTOR_OFF_TIME):
        motor_pulse_state = not motor_pulse_state
        motor_pulse_last_time = current_time
        if motor_pulse_state:
            motor_pin_a.value = True
            motor_pin_b.value = False
        else:
            motor_pin_a.value = False
            motor_pin_b.value = False

def motor_set_direction(forward=True):
    """Set motor direction"""
    if forward:
        motor_forward()
    else:
        motor_reverse()

# ============================================================================
# State Machine Logic
# ============================================================================

def set_state(new_state):
    """Change state and print status"""
    global current_state
    if current_state != new_state:
        print(f"[STATE CHANGE] {current_state} -> {new_state}")
        current_state = new_state

def handle_toggle_change(is_high):
    """
    Handle toggle switch state change
    Logic: 
    - LOW -> HIGH: Person turned on Christmas, start extending
    - HIGH -> LOW: Arm hit toggle (while extending), reverse direction
    - LOW: Do nothing (Christmas is off)
    """
    global current_state
    
    if is_high:
        print("[TOGGLE HIGH] Christmas is ON - Grinch is thinking...")
        # Person flipped toggle to HIGH - start extending arm
        # Note: Limit switch may be pressed when arm is retracted (normal starting position)
        if current_state == IDLE:
            # Add random delay before starting (makes it more "grinchy" and less predictable)
            delay = random.uniform(DELAY_MIN, DELAY_MAX)
            print(f"[ACTION] Waiting {delay:.2f}s before extending...")
            time.sleep(delay)
            print("[ACTION] Starting extension from retracted position...")
            if USE_SPEED_CONTROL:
                motor_forward_pulsed()
            else:
                motor_forward()
            set_state(EXTENDING)
    else:
        print("[TOGGLE LOW] Toggle switch is LOW")
        # If we're extending and toggle goes LOW, arm hit it - reverse
        if current_state == EXTENDING:
            print("[ACTION] Arm hit toggle! Stopping and reversing...")
            motor_stop()
            time.sleep(0.2)  # Brief pause before reversing
            if USE_SPEED_CONTROL:
                motor_reverse_pulsed()
            else:
                motor_reverse()
            set_state(RETRACTING)
        # If toggle is LOW and we're idle, do nothing (Christmas is off)

def handle_microswitch_pressed():
    """
    Handle microswitch press
    Logic: If retracting, stop motor (finger has retracted fully)
    Note: Limit switch is normally pressed when arm is fully retracted (resting position)
    """
    global current_state
    print("[MICROSWITCH PRESSED] Limit switch hit")
    
    if current_state == RETRACTING:
        print("[ACTION] Arm fully retracted, stopping motor")
        motor_stop()
        set_state(IDLE)
        print("[READY] Arm is now in retracted position, ready for next cycle")
    elif current_state == EXTENDING:
        # This shouldn't normally happen, but handle it safely
        print("[WARNING] Limit switch pressed while extending - stopping motor")
        motor_stop()
        set_state(IDLE)
    else:
        # Limit switch pressed while idle - this is normal (arm resting against it)
        # Don't do anything, just log it
        if current_state == IDLE:
            print("[INFO] Limit switch pressed (normal - arm is retracted)")
        else:
            print("[SAFETY] Limit switch pressed unexpectedly, stopping motor")
            motor_stop()
            set_state(IDLE)

def handle_microswitch_released():
    """
    Handle microswitch release
    Logic: When arm extends, limit switch releases (arm moves away from it)
    """
    global current_state
    print("[MICROSWITCH RELEASED] Limit switch released (arm extending)")
    # When limit switch releases during extension, that's expected - don't change state
    # Only reset if we're in an unexpected state
    if current_state not in [IDLE, EXTENDING, RETRACTING]:
        print("[RESET] Unexpected state, resetting to IDLE")
        motor_stop()
        set_state(IDLE)

# ============================================================================
# Main Loop
# ============================================================================

print("=" * 50)
print("Useless Box - GPIO & Motor Control")
print("=" * 50)
print("GPIO 4: Toggle Switch (person flips this)")
print("GPIO 5: Microswitch (limit switch - arm position)")
print("GPIO 14 & 15: DC Motor Control")
print("")
print("Behavior:")
print("  - Toggle LOW: Christmas OFF, do nothing (idle, arm retracted)")
print("  - Toggle HIGH: Christmas ON, extend arm forward")
print("  - Toggle goes LOW (arm hit it): Reverse until limit switch")
print("  - Limit switch pressed (while retracting): Stop and return to idle")
print("  - Note: Limit switch is normally PRESSED when arm is retracted")
print("")
if USE_SPEED_CONTROL:
    speed_pct = (MOTOR_ON_TIME / (MOTOR_ON_TIME + MOTOR_OFF_TIME)) * 100
    print(f"Motor Speed Control: ENABLED ({speed_pct:.0f}% speed)")
    print("  Adjust MOTOR_ON_TIME and MOTOR_OFF_TIME to change speed")
else:
    print("Motor Speed Control: DISABLED (full speed)")
    print("  Set USE_SPEED_CONTROL = True to enable speed control")
print("Press Ctrl+C to stop\n")

# Initialize motor to stopped
motor_stop()
set_state(IDLE)

# Initialize previous states
prev_toggle_state = read_toggle_switch()
prev_microswitch_state = read_microswitch()

# Debug: Print initial switch states
print(f"[INIT] Toggle switch: {'HIGH' if prev_toggle_state else 'LOW'}")
print(f"[INIT] Limit switch: {'PRESSED' if prev_microswitch_state else 'RELEASED'}")
print(f"[INIT] Raw microswitch.value: {microswitch.value} (True=HIGH/released, False=LOW/pressed)")
print(f"[INIT] With pull-up, LOW (False) = pressed, HIGH (True) = released")
print("")

while True:
    # Read current states
    toggle_state = read_toggle_switch()
    microswitch_state = read_microswitch()
    
    # Handle toggle switch changes
    if toggle_state != prev_toggle_state:
        handle_toggle_change(toggle_state)
        prev_toggle_state = toggle_state
    
    # Also check toggle state continuously while extending
    # (in case we miss the transition or need to react immediately)
    if current_state == EXTENDING and not toggle_state:
        # Toggle went LOW while extending - arm hit it
        print("[ACTION] Toggle LOW detected while extending - reversing...")
        motor_stop()
        time.sleep(0.2)  # Brief pause before reversing
        if USE_SPEED_CONTROL:
            motor_reverse_pulsed()
        else:
            motor_reverse()
        set_state(RETRACTING)
        prev_toggle_state = toggle_state  # Update to prevent re-trigger
    
    # Apply motor control with speed control if enabled
    if USE_SPEED_CONTROL:
        if current_state == EXTENDING:
            motor_forward_pulsed()
        elif current_state == RETRACTING:
            motor_reverse_pulsed()
    
    # Safety check: if we're retracting and limit switch is released unexpectedly
    if current_state == RETRACTING and not microswitch_state:
        # This shouldn't happen normally, but handle it gracefully
        if prev_microswitch_state:  # Was pressed, now released
            print("[WARNING] Limit switch released while retracting - continuing...")
    
    # Detect microswitch press (only care about press, not release)
    if microswitch_state and not prev_microswitch_state:
        handle_microswitch_pressed()
        prev_microswitch_state = microswitch_state
    elif not microswitch_state and prev_microswitch_state:
        handle_microswitch_released()
        prev_microswitch_state = microswitch_state
    
    # Check every 50ms for responsive detection
    time.sleep(0.05)
