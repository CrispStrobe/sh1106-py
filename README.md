# SH1106 OLED Driver for ESP32 + MicroPython

A complete MicroPython driver for SH1106-based OLED displays on ESP32 microcontrollers. This driver provides basic support for 128x64 pixel monochrome OLED displays using the SH1106 controller chip.

## 🎯 Features

- ✅ **SH1106 support** - with proper page-based addressing
- ✅ **I2C interface** - per simple 4-wire connection
- ✅ **MicroPython native** - no external dependencies
- ✅ **Graphics support** - text, pixels, lines, rectangles
- ✅ **Multiple display sizes** - 128x64 (tested), (probably) 128x32, and more
- ✅ **Hardware abstraction** - Easy to use API
- ✅ **Example projects** - Clock, animations, graphs, menus

## 📊 Wiring Diagram

```
ESP32          SH1106 Display
-----          ---------------
3.3V    -----> VDD
GND     -----> GND  
GPIO 22 -----> SCK (Clock)
GPIO 21 -----> SDA (Data)
```

### Pin Configuration
| ESP32 Pin | Display Pin | Function |
|-----------|-------------|----------|
| 3.3V      | VDD         | Power    |
| GND       | GND         | Ground   |
| GPIO 22   | SCK         | I2C Clock|
| GPIO 21   | SDA         | I2C Data |

## 🚀 Installation

1. **Flash MicroPython** to your ESP32
2. **Copy the driver** to your ESP32:
   - Save `sh1106.py` to your ESP32 filesystem
3. **Install using Thonny IDE** or any MicroPython tool

## 💡 Quick Start

```python
from machine import Pin, I2C
import sh1106

# Initialize I2C
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

# Initialize display
oled = sh1106.SH1106_I2C(128, 64, i2c)

# Display text
oled.fill(0)                    # Clear display
oled.text('Hello World!', 0, 0) # Add text
oled.text('SH1106 Working!', 0, 10)
oled.show()                     # Update display
```

## 📚 API Reference

### Constructor

```python
oled = sh1106.SH1106_I2C(width, height, i2c, addr=0x3C, external_vcc=False)
```

**Parameters:**
- `width`: Display width in pixels (usually 128)
- `height`: Display height in pixels (usually 64)
- `i2c`: I2C object
- `addr`: I2C address (default 0x3C)
- `external_vcc`: Use external VCC (default False)

### Display Methods

| Method | Description | Example |
|--------|-------------|---------|
| `fill(color)` | Fill entire display | `oled.fill(0)` |
| `pixel(x, y, color)` | Set single pixel | `oled.pixel(64, 32, 1)` |
| `text(string, x, y, color=1)` | Display text | `oled.text('Hello', 0, 0)` |
| `line(x1, y1, x2, y2, color)` | Draw line | `oled.line(0, 0, 127, 63, 1)` |
| `rect(x, y, w, h, color)` | Draw rectangle | `oled.rect(10, 10, 50, 30, 1)` |
| `fill_rect(x, y, w, h, color)` | Filled rectangle | `oled.fill_rect(10, 10, 50, 30, 1)` |
| `show()` | Update display | `oled.show()` |

### Control Methods

| Method | Description | Example |
|--------|-------------|---------|
| `contrast(value)` | Set brightness (0-255) | `oled.contrast(128)` |
| `invert(enable)` | Invert colors | `oled.invert(True)` |
| `rotate(enable)` | Rotate 180° | `oled.rotate(True)` |
| `poweroff()` | Turn off display | `oled.poweroff()` |
| `poweron()` | Turn on display | `oled.poweron()` |

### Color Values

- `0` = Black (pixel off)
- `1` = White (pixel on)

## 🎨 Example Projects

### Digital Clock
```python
import time

while True:
    current_time = time.ticks_ms()
    seconds = (current_time // 1000) % 60
    minutes = (current_time // 60000) % 60
    
    oled.fill(0)
    oled.text(f'{minutes:02d}:{seconds:02d}', 35, 25)
    oled.show()
    time.sleep(1)
```

### Temperature Monitor
```python
from machine import ADC

# Read temperature sensor (example)
sensor = ADC(Pin(36))

oled.fill(0)
oled.text('Temperature:', 0, 0)
temp = sensor.read() * 3.3 / 4095 * 100  # Convert to temp
oled.text(f'{temp:.1f}C', 0, 20)
oled.show()
```

### Graphics Demo
```python
# Draw shapes
oled.fill(0)
oled.rect(10, 10, 30, 20, 1)      # Rectangle
oled.fill_rect(50, 10, 30, 20, 1) # Filled rectangle
oled.line(0, 40, 127, 40, 1)      # Horizontal line
oled.line(64, 0, 64, 63, 1)       # Vertical line

# Draw pixels
for x in range(0, 128, 4):
    oled.pixel(x, 50, 1)

oled.show()
```

## 🔍 Troubleshooting

### No display output
- Check wiring connections
- Verify I2C address with `i2c.scan()`
- Ensure 3.3V power (not 5V)
- Try adding pull-up resistors (4.7kΩ)

### Display too dim/bright
- Use `oled.contrast(value)` to adjust brightness
- Values: 0 (dimmest) to 255 (brightest)

### I2C communication errors
- Try slower I2C frequency: `freq=100000`
- Check for loose connections
- Verify ESP32 pin assignments

### Text appears upside down
- Use `oled.rotate(True)` to flip display 180°

## 🆚 SSD1306 vs SH1106

| Feature | SSD1306 | SH1106 |
|---------|---------|--------|
| Addressing | Horizontal | Page-based |
| Buffer write | All at once | Page by page |
| Column offset | None | 2-pixel offset |
| Common mistake | Often mislabeled as SH1106 | Often mislabeled as SSD1306 |

## 🤝 Contributing

Contributions are welcome! Please:

## 📝 License

MIT License

## 🙏 Acknowledgments

- MicroPython community for the excellent platform
- Adafruit for SSD1306 reference implementation
- ESP32 community for hardware support
