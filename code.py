# Hydration Battle Station - Main Loop
# This is the entry point: CircuitPython runs code.py automatically on boot.

import time
import board
import busio
import digitalio
import adafruit_ssd1306

# ─── GeeekPi/52Pi Breadboard Kit Compatibility ───────────────────
# The GeeekPi EP-0164 board has an onboard buzzer whose BEEP pin floats
# by default, causing it to scream on power-up. Drive GP13 LOW immediately
# to silence it before anything else runs.
_buzzer_silence = digitalio.DigitalInOut(board.GP13)
_buzzer_silence.direction = digitalio.Direction.OUTPUT
_buzzer_silence.value = False

import config
from score_tracker import ScoreTracker
from display_manager import DisplayManager
from animations import Animator

# ─── Hardware Setup ──────────────────────────────────────────────

# I2C for OLED display
i2c = busio.I2C(
    scl=board.GP1,  # config.I2C_SCL_PIN
    sda=board.GP0,  # config.I2C_SDA_PIN
)

# OLED display
oled = adafruit_ssd1306.SSD1306_I2C(
    config.DISPLAY_WIDTH,
    config.DISPLAY_HEIGHT,
    i2c,
    addr=config.DISPLAY_I2C_ADDR,
)

# Buttons with internal pull-up (press connects to GND)
btn1 = digitalio.DigitalInOut(board.GP16)
btn1.direction = digitalio.Direction.INPUT
btn1.pull = digitalio.Pull.UP

btn2 = digitalio.DigitalInOut(board.GP17)
btn2.direction = digitalio.Direction.INPUT
btn2.pull = digitalio.Pull.UP

# ─── Initialize Modules ─────────────────────────────────────────

scores = ScoreTracker()
display = DisplayManager(oled)
animator = Animator(display)

# ─── State ───────────────────────────────────────────────────────

last_activity = time.monotonic()
idle_showing_alltime = False
idle_last_switch = time.monotonic()

# Debounce tracking
btn1_was_pressed = False
btn2_was_pressed = False
both_held_start = None
daily_reset_done = False

# ─── Splash Screen ──────────────────────────────────────────────

display.draw_splash_screen()
time.sleep(2)
display.draw_daily_scoreboard(scores)

# ─── Helper Functions ────────────────────────────────────────────

def is_pressed(btn):
    """Buttons are active LOW with pull-up resistors."""
    return not btn.value


def handle_button_press(player):
    """Process a single button press: add water, animate, refresh display."""
    global last_activity, idle_showing_alltime

    player_name = config.PLAYER_1_NAME if player == 1 else config.PLAYER_2_NAME

    # Check if this press changes the leader
    old_leader = scores.daily_leader()
    oz = scores.add_water(player)
    new_leader = scores.daily_leader()

    # Show button press animation
    animator.button_press(player, oz, player_name)

    # If leadership changed, celebrate!
    if new_leader != old_leader and new_leader != 0:
        new_leader_name = config.PLAYER_1_NAME if new_leader == 1 else config.PLAYER_2_NAME
        animator.leader_change(new_leader_name)

    # Return to daily scoreboard
    display.draw_daily_scoreboard(scores)
    last_activity = time.monotonic()
    idle_showing_alltime = False


def handle_daily_reset():
    """Reset daily scores when both buttons held for RESET_HOLD_TIME."""
    global last_activity, idle_showing_alltime

    scores.reset_daily()
    animator.daily_reset()
    display.draw_alltime_reset_warning()  # Hint to keep holding for all-time reset
    last_activity = time.monotonic()
    idle_showing_alltime = False


def handle_alltime_reset():
    """Reset all-time scores when both buttons held for ALLTIME_RESET_HOLD_TIME."""
    global last_activity, idle_showing_alltime

    scores.reset_alltime()
    animator.daily_reset()
    display.draw_alltime_reset_confirmation()
    time.sleep(2)
    display.draw_daily_scoreboard(scores)
    last_activity = time.monotonic()
    idle_showing_alltime = False


# ─── Main Loop ───────────────────────────────────────────────────

while True:
    now = time.monotonic()
    b1 = is_pressed(btn1)
    b2 = is_pressed(btn2)

    # --- Both buttons held = reset gesture ---
    if b1 and b2:
        if both_held_start is None:
            both_held_start = now
        held_time = now - both_held_start

        if daily_reset_done and held_time >= config.ALLTIME_RESET_HOLD_TIME:
            # Held long enough for all-time reset
            handle_alltime_reset()
            both_held_start = None
            daily_reset_done = False
            while is_pressed(btn1) or is_pressed(btn2):
                time.sleep(0.05)
        elif not daily_reset_done and held_time >= config.RESET_HOLD_TIME:
            # Held long enough for daily reset — hint to keep holding
            handle_daily_reset()
            daily_reset_done = True
    else:
        if daily_reset_done:
            # Released after daily reset but before all-time — go back to scoreboard
            display.draw_daily_scoreboard(scores)
        daily_reset_done = False
        both_held_start = None

        # --- Single button press (with debounce) ---
        if b1 and not btn1_was_pressed:
            handle_button_press(1)
        elif b2 and not btn2_was_pressed:
            handle_button_press(2)

    btn1_was_pressed = b1
    btn2_was_pressed = b2

    # --- Idle screen cycling ---
    idle_time = now - last_activity
    if idle_time >= config.IDLE_TIMEOUT:
        if now - idle_last_switch >= config.IDLE_CYCLE_INTERVAL:
            idle_showing_alltime = not idle_showing_alltime
            if idle_showing_alltime:
                display.draw_alltime_scoreboard(scores)
            else:
                display.draw_daily_scoreboard(scores)
            idle_last_switch = now

    time.sleep(0.02)  # 50 Hz polling — responsive without burning CPU
