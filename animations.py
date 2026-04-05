# Animations - Hydration Battle Station
# Fun visual feedback for button presses and events

import time
import random
import config


# Encouraging messages shown on button press
ENCOURAGEMENTS = [
    "Nice!",
    "Stay hydrated!",
    "Splash!",
    "Chug chug!",
    "H2O yeah!",
    "Refreshing!",
    "Gulp!",
    "Hydro homie!",
    "Water champ!",
    "Drip drip!",
]

LEADER_CHANGE_MESSAGES = [
    "NEW LEADER!",
    "TAKEOVER!",
    "DETHRONED!",
    "OVERTAKEN!",
]


class Animator:
    def __init__(self, display_manager):
        """
        Args:
            display_manager: DisplayManager instance
        """
        self.dm = display_manager
        self.display = display_manager.display

    def button_press(self, player, oz_added, player_name):
        """Animate a button press: show +oz and an encouraging message."""
        self.dm.clear()

        # Big "+4 oz" in the center
        oz_text = f"+{oz_added} oz"
        x = (config.DISPLAY_WIDTH - len(oz_text) * 6) // 2
        self.display.text(oz_text, x, 12, 1)

        # Player name
        name_x = (config.DISPLAY_WIDTH - len(player_name) * 6) // 2
        self.display.text(player_name, name_x, 28, 1)

        # Random encouragement
        msg = random.choice(ENCOURAGEMENTS)
        msg_x = (config.DISPLAY_WIDTH - len(msg) * 6) // 2
        self.display.text(msg, msg_x, 46, 1)

        # Draw water drop accents on the sides
        self._draw_drops()

        self.dm.show()
        time.sleep(config.ANIMATION_DURATION)

    def leader_change(self, new_leader_name):
        """Celebrate a change in the daily lead."""
        self.dm.clear()

        msg = random.choice(LEADER_CHANGE_MESSAGES)
        msg_x = (config.DISPLAY_WIDTH - len(msg) * 6) // 2
        self.display.text(msg, msg_x, 8, 1)

        # Decorative lines
        for x in range(config.DISPLAY_WIDTH):
            self.display.pixel(x, 20, 1)
            self.display.pixel(x, 44, 1)

        # Crown icon centered
        self.dm._draw_bitmap(self.dm.__class__.__dict__.get('CROWN', b'\x00' * 8), 60, 24)

        name_x = (config.DISPLAY_WIDTH - len(new_leader_name) * 6) // 2
        self.display.text(new_leader_name, name_x, 30, 1)

        self.display.text("takes the lead!", 10, 50, 1)

        self.dm.show()
        time.sleep(1.2)

    def daily_reset(self):
        """Animate the daily reset action."""
        # Flash effect
        for i in range(3):
            self.display.fill(1)
            self.dm.show()
            time.sleep(0.1)
            self.display.fill(0)
            self.dm.show()
            time.sleep(0.1)

        self.dm.draw_reset_confirmation()
        time.sleep(1.5)

    def _draw_drops(self):
        """Draw small water drop accents in corners."""
        # Simple 3-pixel drops in corners
        for y_off, x_positions in [(4, [4, 120]), (50, [8, 116])]:
            for x in x_positions:
                self.display.pixel(x, y_off, 1)
                self.display.pixel(x - 1, y_off + 1, 1)
                self.display.pixel(x, y_off + 1, 1)
                self.display.pixel(x + 1, y_off + 1, 1)
                self.display.pixel(x, y_off + 2, 1)
