# Hydration Battle Station 💧🏆

A fun desk gadget that tracks how much water you and your coworker drink each day — because staying hydrated should be competitive.

**Each button press = +4 oz.** The OLED display shows who's winning.

---

## Hardware Shopping List

| # | Item | Price | Link |
|---|---|---|---|
| 1 | **Raspberry Pi Pico** (with pre-soldered headers) | $4–7 | [Adafruit](https://www.adafruit.com/product/6315) · [Amazon](https://www.amazon.com/pi-pico/s?k=pi+pico) |
| 2 | **SSD1306 OLED Display** (0.96", 128×64, I2C) | $6–18 | [Adafruit STEMMA QT](https://www.adafruit.com/product/326) · [Amazon](https://www.amazon.com/SSD1306/s?k=SSD1306) |
| 3 | **2× Arcade Buttons** (24mm, LED optional) | $5–10 | [Adafruit LED ($2.50 ea)](https://www.adafruit.com/product/3429) · [Amazon](https://www.amazon.com/24mm-arcade-buttons/s?k=24mm+arcade+buttons) |
| 4 | **Breadboard + Jumper Wires Kit** | $6–14 | [GeeekPi Kit (Amazon)](https://www.amazon.com/GeeekPi-Raspberry-BreadBoard-Half-Size-Breadboard/dp/B093GXJ64J) · [Adafruit](https://www.adafruit.com/product/3314) |
| 5 | **Micro-USB Cable** | Free–$3 | Any cable you already have |

**Total: ~$23–$44** depending on where you buy.

> **💡 Tip:** Get the Pico **"with headers"** so it plugs directly into the breadboard — no soldering required.

---

## Wiring Diagram

```
┌──────────────────────────────┐
│       Raspberry Pi Pico      │
│                              │
│  GP16 ●───── Button 1 ───── GND    (Player 1)
│  GP17 ●───── Button 2 ───── GND    (Player 2)
│                              │
│  GP0 (SDA) ── OLED SDA      │
│  GP1 (SCL) ── OLED SCL      │
│  3V3  ─────── OLED VCC      │
│  GND  ─────── OLED GND      │
└──────────────────────────────┘
```

### Button Wiring Detail
Each button has two terminals:
- **One terminal** → Connect to the Pico GPIO pin (GP16 or GP17)
- **Other terminal** → Connect to any GND pin on the Pico

The code uses the Pico's internal pull-up resistors, so no external resistors are needed.

### OLED Wiring Detail
The OLED has 4 pins:
| OLED Pin | Pico Pin |
|----------|----------|
| VCC | 3V3 (pin 36) |
| GND | GND (pin 38) |
| SDA | GP0 (pin 1) |
| SCL | GP1 (pin 2) |

---

## Software Setup

### Step 1: Install CircuitPython on the Pico

1. Go to [circuitpython.org/board/raspberry_pi_pico](https://circuitpython.org/board/raspberry_pi_pico/)
2. Download the latest `.uf2` file
3. Hold the **BOOTSEL** button on the Pico while plugging it into USB
4. The Pico appears as a USB drive called **RPI-RP2**
5. Drag the `.uf2` file onto the RPI-RP2 drive
6. The Pico reboots and reappears as a drive called **CIRCUITPY**

### Step 2: Install Required Libraries

1. Go to [circuitpython.org/libraries](https://circuitpython.org/libraries) and download the **Bundle for your CircuitPython version**
2. Unzip the bundle
3. From the `lib/` folder in the bundle, copy these files to the `CIRCUITPY/lib/` folder on your Pico:
   - `adafruit_ssd1306.mpy`
   - `adafruit_framebuf.mpy`
4. That's it — just two library files!

### Step 3: Copy the Code

Copy ALL of these files from this project to the root of the **CIRCUITPY** drive:
- `code.py` (main program — CircuitPython runs this automatically)
- `config.py` (settings — edit player names here!)
- `score_tracker.py`
- `display_manager.py`
- `animations.py`

### Step 4: Personalize

Open `config.py` in any text editor (Notepad works!) and change:
```python
PLAYER_1_NAME = "Stephen"   # Change to your name
PLAYER_2_NAME = "Buddy"     # Change to your coworker's name
```

Save the file — the Pico auto-restarts and you're good to go!

---

## How to Use

| Action | How |
|--------|-----|
| **Log water** | Press your button. Each press = +4 oz. |
| **See who's winning today** | Look at the screen — crown icon (♛) = leader |
| **See all-time totals** | Wait 10 seconds — screen auto-cycles to all-time view |
| **Reset daily scores** | Hold BOTH buttons for 3 seconds |
| **Power it** | Plug the Pico into any USB port or wall charger |

---

## Troubleshooting

### CIRCUITPY drive doesn't appear
- Make sure you flashed CircuitPython (Step 1), not MicroPython
- Try a different USB cable — some cables are power-only (no data)
- Hold BOOTSEL and re-plug to get back to RPI-RP2 mode

### Display shows nothing
- Check wiring: SDA→GP0, SCL→GP1, VCC→3V3, GND→GND
- Run an I2C scan to verify the display address:
  ```python
  import board, busio
  i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
  while not i2c.try_lock(): pass
  print([hex(x) for x in i2c.scan()])
  i2c.unlock()
  ```
  You should see `['0x3c']`. If not, re-check wiring.

### Buttons don't register
- Verify wiring: one terminal to GP16/GP17, other to GND
- Test in the REPL (connect via serial terminal):
  ```python
  import board, digitalio
  btn = digitalio.DigitalInOut(board.GP16)
  btn.direction = digitalio.Direction.INPUT
  btn.pull = digitalio.Pull.UP
  print(btn.value)  # Should be True (not pressed) or False (pressed)
  ```

### Scores didn't save after power loss
- The Pico's flash storage must be writable. If you see write errors:
  ```python
  import storage
  storage.remount("/", readonly=False)
  ```
  Add this to a `boot.py` file on the CIRCUITPY drive.

---

## File Overview

| File | Purpose |
|------|---------|
| `code.py` | Main loop — button polling, game logic, display updates |
| `config.py` | All settings: names, pins, timing, increment size |
| `score_tracker.py` | Score state + JSON persistence to flash |
| `display_manager.py` | OLED rendering: scoreboards, bitmaps, layouts |
| `animations.py` | Fun button-press effects and celebrations |
| `lib/` | CircuitPython library files (copy from bundle) |

---

## Customization Ideas

- **Change the oz per press**: Edit `OZ_PER_PRESS` in `config.py`
- **Add more players**: Would need code changes — but the architecture supports it
- **3D print a case**: The breadboard is ~8.5 × 5.5 cm — plenty of case designs on Thingiverse
- **Add a buzzer**: Wire a piezo buzzer to a GPIO pin for sound effects on button press
- **Go wireless**: Swap the Pico for a **Pico W** and add a web dashboard later
