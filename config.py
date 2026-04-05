# Hydration Battle Station - Configuration
# Edit these values to personalize your device!

# --- Player Names ---
PLAYER_1_NAME = "Stephen"
PLAYER_2_NAME = "Buddy"

# --- Water Increment ---
OZ_PER_PRESS = 4  # Each button press adds this many oz

# --- Pin Assignments (Raspberry Pi Pico) ---
BUTTON_1_PIN = 16  # GP16 - Player 1 button
BUTTON_2_PIN = 17  # GP17 - Player 2 button
I2C_SDA_PIN = 0    # GP0  - OLED SDA
I2C_SCL_PIN = 1    # GP1  - OLED SCL

# --- Display Settings ---
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
DISPLAY_I2C_ADDR = 0x3C

# --- Timing (seconds) ---
IDLE_TIMEOUT = 10       # Seconds before idle screen cycling starts
IDLE_CYCLE_INTERVAL = 5 # Seconds between screen switches in idle mode
ANIMATION_DURATION = 0.8 # How long button-press animations last
RESET_HOLD_TIME = 3     # Hold both buttons this long to reset daily scores

# --- Save File ---
SAVE_FILE = "/scores.json"
