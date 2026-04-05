# Score Tracker - Hydration Battle Station
# Manages daily and all-time water intake scores with flash persistence

import json
import config


class ScoreTracker:
    def __init__(self):
        self.daily = {1: 0, 2: 0}
        self.alltime = {1: 0, 2: 0}
        self._load()

    def add_water(self, player):
        """Add one press worth of water (OZ_PER_PRESS) for a player (1 or 2)."""
        oz = config.OZ_PER_PRESS
        self.daily[player] += oz
        self.alltime[player] += oz
        self._save()
        return oz

    def get_daily(self, player):
        return self.daily[player]

    def get_alltime(self, player):
        return self.alltime[player]

    def daily_leader(self):
        """Return winning player number, or 0 if tied."""
        if self.daily[1] > self.daily[2]:
            return 1
        elif self.daily[2] > self.daily[1]:
            return 2
        return 0

    def alltime_leader(self):
        """Return all-time winning player number, or 0 if tied."""
        if self.alltime[1] > self.alltime[2]:
            return 1
        elif self.alltime[2] > self.alltime[1]:
            return 2
        return 0

    def reset_daily(self):
        """Reset today's scores. All-time totals are preserved."""
        self.daily[1] = 0
        self.daily[2] = 0
        self._save()

    def _save(self):
        """Persist scores to flash as JSON."""
        data = {
            "daily": {"1": self.daily[1], "2": self.daily[2]},
            "alltime": {"1": self.alltime[1], "2": self.alltime[2]},
        }
        try:
            with open(config.SAVE_FILE, "w") as f:
                json.dump(data, f)
        except OSError:
            pass  # Flash write failed — scores stay in memory

    def _load(self):
        """Load scores from flash. If missing or corrupt, start fresh."""
        try:
            with open(config.SAVE_FILE, "r") as f:
                data = json.load(f)
            self.daily[1] = data.get("daily", {}).get("1", 0)
            self.daily[2] = data.get("daily", {}).get("2", 0)
            self.alltime[1] = data.get("alltime", {}).get("1", 0)
            self.alltime[2] = data.get("alltime", {}).get("2", 0)
        except (OSError, ValueError, KeyError):
            # File missing, corrupt, or unreadable — start fresh
            self.daily = {1: 0, 2: 0}
            self.alltime = {1: 0, 2: 0}
