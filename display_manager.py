# Display Manager - Hydration Battle Station
# Handles all OLED rendering: scoreboards, animations, messages

import time
import config

# Crown bitmap (8x8) - shown next to the leader's name
CROWN = bytearray([
    0b00000000,
    0b01000100,
    0b01101100,
    0b01111100,
    0b01111100,
    0b01111100,
    0b01111100,
    0b00000000,
])

# Water drop bitmap (8x8)
WATER_DROP = bytearray([
    0b00010000,
    0b00111000,
    0b00111000,
    0b01111100,
    0b01111100,
    0b01111100,
    0b00111000,
    0b00000000,
])

# Trophy bitmap (8x8) for all-time leader
TROPHY = bytearray([
    0b01111110,
    0b01111110,
    0b00111100,
    0b00011000,
    0b00011000,
    0b00011000,
    0b00111100,
    0b01111110,
])


class DisplayManager:
    def __init__(self, display):
        """
        Args:
            display: An initialized adafruit_ssd1306.SSD1306_I2C object
        """
        self.display = display
        self.width = config.DISPLAY_WIDTH
        self.height = config.DISPLAY_HEIGHT

    def clear(self):
        self.display.fill(0)

    def show(self):
        self.display.show()

    def _draw_bitmap(self, bitmap, x, y, w=8, h=8):
        """Draw a 1-bit bitmap at (x, y). Each byte = one row, MSB first."""
        for row in range(h):
            byte = bitmap[row]
            for col in range(w):
                if byte & (1 << (7 - col)):
                    self.display.pixel(x + col, y + row, 1)

    def draw_daily_scoreboard(self, scores):
        """Draw the main daily competition screen.

        Args:
            scores: ScoreTracker instance
        """
        self.clear()

        p1_name = config.PLAYER_1_NAME
        p2_name = config.PLAYER_2_NAME
        p1_oz = scores.get_daily(1)
        p2_oz = scores.get_daily(2)
        leader = scores.daily_leader()

        # Title bar
        self.display.text("TODAY'S BATTLE", 14, 0, 1)
        # Divider line
        for x in range(self.width):
            self.display.pixel(x, 10, 1)

        # Player 1 row
        y1 = 16
        if leader == 1:
            self._draw_bitmap(CROWN, 0, y1)
            self.display.text(f"{p1_name}", 10, y1, 1)
        else:
            self.display.text(f"{p1_name}", 2, y1, 1)
        oz_text = f"{p1_oz} oz"
        self.display.text(oz_text, self.width - len(oz_text) * 6 - 2, y1, 1)

        # Player 2 row
        y2 = 30
        if leader == 2:
            self._draw_bitmap(CROWN, 0, y2)
            self.display.text(f"{p2_name}", 10, y2, 1)
        else:
            self.display.text(f"{p2_name}", 2, y2, 1)
        oz_text = f"{p2_oz} oz"
        self.display.text(oz_text, self.width - len(oz_text) * 6 - 2, y2, 1)

        # Status bar at bottom
        if leader == 0:
            status = "TIED!"
        elif leader == 1:
            status = f"{p1_name} leads!"
        else:
            status = f"{p2_name} leads!"
        # Center the status text
        x_pos = (self.width - len(status) * 6) // 2
        self.display.text(status, x_pos, 52, 1)

        # Bottom divider
        for x in range(self.width):
            self.display.pixel(x, 50, 1)

        self.show()

    def draw_alltime_scoreboard(self, scores):
        """Draw the all-time totals screen.

        Args:
            scores: ScoreTracker instance
        """
        self.clear()

        p1_name = config.PLAYER_1_NAME
        p2_name = config.PLAYER_2_NAME
        p1_oz = scores.get_alltime(1)
        p2_oz = scores.get_alltime(2)
        leader = scores.alltime_leader()

        # Title
        self.display.text("ALL-TIME TOTALS", 10, 0, 1)
        for x in range(self.width):
            self.display.pixel(x, 10, 1)

        # Player 1
        y1 = 16
        if leader == 1:
            self._draw_bitmap(TROPHY, 0, y1)
            self.display.text(f"{p1_name}", 10, y1, 1)
        else:
            self.display.text(f"{p1_name}", 2, y1, 1)
        oz_text = f"{p1_oz} oz"
        self.display.text(oz_text, self.width - len(oz_text) * 6 - 2, y1, 1)

        # Player 2
        y2 = 30
        if leader == 2:
            self._draw_bitmap(TROPHY, 0, y2)
            self.display.text(f"{p2_name}", 10, y2, 1)
        else:
            self.display.text(f"{p2_name}", 2, y2, 1)
        oz_text = f"{p2_oz} oz"
        self.display.text(oz_text, self.width - len(oz_text) * 6 - 2, y2, 1)

        # Grand champion callout
        if leader == 0:
            status = "ALL TIED UP!"
        elif leader == 1:
            status = f"{p1_name} = CHAMP"
        else:
            status = f"{p2_name} = CHAMP"
        x_pos = (self.width - len(status) * 6) // 2
        for x in range(self.width):
            self.display.pixel(x, 50, 1)
        self.display.text(status, x_pos, 52, 1)

        self.show()

    def draw_reset_confirmation(self):
        """Show confirmation that daily scores were reset."""
        self.clear()
        self.display.text("DAILY SCORES", 20, 16, 1)
        self.display.text("RESET!", 40, 30, 1)
        self._draw_bitmap(WATER_DROP, 60, 44)
        self.show()

    def draw_splash_screen(self):
        """Show the startup splash screen."""
        self.clear()
        self._draw_bitmap(WATER_DROP, 56, 4)
        self.display.text("HYDRATION", 24, 18, 1)
        self.display.text("BATTLE", 36, 30, 1)
        self.display.text("STATION", 32, 42, 1)
        self.display.text(f"{config.OZ_PER_PRESS} oz per press", 16, 56, 1)
        self.show()
