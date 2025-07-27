# attempt at a custom SSD1306 micropython driver with 128x64 initialization
# based on Adafruit SSD1306 library parameters
# not tested as i currently have no ssd1306 at the ready

from micropython import const
import framebuf
from machine import Pin, I2C
import time

# SSD1306 Commands
SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xA4)
SET_NORM_INV = const(0xA6)
SET_DISP = const(0xAE)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xA0)
SET_MUX_RATIO = const(0xA8)
SET_COM_OUT_DIR = const(0xC0)
SET_DISP_OFFSET = const(0xD3)
SET_COM_PIN_CFG = const(0xDA)
SET_DISP_CLK_DIV = const(0xD5)
SET_PRECHARGE = const(0xD9)
SET_VCOM_DESEL = const(0xDB)
SET_CHARGE_PUMP = const(0x8D)

class CustomSSD1306(framebuf.FrameBuffer):
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.external_vcc = external_vcc
        self.width = width
        self.height = height
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        
        # Initialize display with proper parameters for different sizes
        self.init_display()

    def write_cmd(self, cmd):
        """Write a single command"""
        self.i2c.writeto(self.addr, bytearray([0x80, cmd]))

    def write_data(self, buf):
        """Write data buffer"""
        # Split into chunks if needed for I2C buffer limits
        chunk_size = 32
        for i in range(0, len(buf), chunk_size):
            chunk = buf[i:i+chunk_size]
            data = bytearray([0x40]) + chunk
            self.i2c.writeto(self.addr, data)

    def init_display(self):
        """Initialize display with Adafruit-compatible parameters"""
        print(f"Initializing {self.width}x{self.height} display...")
        
        # Turn display off
        self.write_cmd(SET_DISP | 0x00)
        
        # Set display clock divide ratio/oscillator frequency
        self.write_cmd(SET_DISP_CLK_DIV)
        self.write_cmd(0x80)  # Suggested ratio 0x80
        
        # Set multiplex ratio
        self.write_cmd(SET_MUX_RATIO)
        self.write_cmd(self.height - 1)
        
        # Set display offset
        self.write_cmd(SET_DISP_OFFSET)
        self.write_cmd(0x0)  # No offset
        
        # Set start line address
        self.write_cmd(SET_DISP_START_LINE | 0x0)
        
        # Charge pump setting
        self.write_cmd(SET_CHARGE_PUMP)
        if self.external_vcc:
            self.write_cmd(0x10)
        else:
            self.write_cmd(0x14)
        
        # Memory addressing mode
        self.write_cmd(SET_MEM_ADDR)
        self.write_cmd(0x00)  # Horizontal addressing mode
        
        # Set segment re-map
        self.write_cmd(SET_SEG_REMAP | 0x1)
        
        # Set COM output scan direction
        self.write_cmd(SET_COM_OUT_DIR | 0x08)
        
        # Set COM pins hardware configuration - CRITICAL FOR DIFFERENT DISPLAY SIZES
        self.write_cmd(SET_COM_PIN_CFG)
        if (self.width == 128) and (self.height == 64):
            # 128x64 displays need 0x12
            com_pins = 0x12
            contrast = 0xCF if not self.external_vcc else 0x9F
            print("Using 128x64 configuration: comPins=0x12")
        elif (self.width == 128) and (self.height == 32):
            # 128x32 displays need 0x02
            com_pins = 0x02
            contrast = 0x8F
            print("Using 128x32 configuration: comPins=0x02")
        elif (self.width == 96) and (self.height == 16):
            com_pins = 0x02
            contrast = 0xAF if not self.external_vcc else 0x10
            print("Using 96x16 configuration: comPins=0x02")
        elif (self.width == 64) and (self.height == 32):
            com_pins = 0x12
            contrast = 0xCF if not self.external_vcc else 0x10
            print("Using 64x32 configuration: comPins=0x12")
        else:
            # Default/unknown
            com_pins = 0x02
            contrast = 0x8F
            print(f"Using default configuration for {self.width}x{self.height}")
        
        self.write_cmd(com_pins)
        
        # Set contrast control
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)
        
        # Set pre-charge period
        self.write_cmd(SET_PRECHARGE)
        if self.external_vcc:
            self.write_cmd(0x22)
        else:
            self.write_cmd(0xF1)
        
        # Set VCOMH deselect level
        self.write_cmd(SET_VCOM_DESEL)
        self.write_cmd(0x40)
        
        # Set entire display on/off
        self.write_cmd(SET_ENTIRE_ON)  # Resume to RAM content display
        
        # Set normal display (not inverted)
        self.write_cmd(SET_NORM_INV)
        
        # Deactivate scroll
        self.write_cmd(0x2E)
        
        # Turn display on
        self.write_cmd(SET_DISP | 0x01)
        
        # Clear display
        self.fill(0)
        self.show()
        print("Display initialization complete!")

    def show(self):
        """Update the display"""
        # Set column address range
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(0)           # Column start address
        self.write_cmd(self.width - 1)  # Column end address
        
        # Set page address range
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)           # Page start address
        self.write_cmd(self.pages - 1)  # Page end address
        
        # Write display data
        self.write_data(self.buffer)

    def poweroff(self):
        """Turn off the display"""
        self.write_cmd(SET_DISP | 0x00)

    def poweron(self):
        """Turn on the display"""
        self.write_cmd(SET_DISP | 0x01)

    def contrast(self, contrast):
        """Set display contrast (0-255)"""
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        """Invert display colors"""
        self.write_cmd(SET_NORM_INV | (invert & 1))

# Test the custom driver
def test_custom_driver():
    print("=== Testing Custom SSD1306 Driver ===")
    
    # Initialize I2C
    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
    print("I2C devices:", [hex(addr) for addr in i2c.scan()])
    
    # Initialize display with proper 128x64 settings
    oled = CustomSSD1306(128, 64, i2c, addr=0x3C)
    
    # Test 1: Clear display
    print("Test 1: Clearing display...")
    oled.fill(0)
    oled.show()
    time.sleep(1)
    
    # Test 2: Simple text
    print("Test 2: Displaying text...")
    oled.fill(0)
    oled.text('Custom Driver', 0, 0)
    oled.text('128x64 Test', 0, 10)
    oled.text('GME 12864-70', 0, 20)
    oled.text('Working?', 0, 30)
    oled.text('Line 5', 0, 40)
    oled.text('Line 6', 0, 50)
    oled.show()
    time.sleep(3)
    
    # Test 3: Graphics
    print("Test 3: Drawing graphics...")
    oled.fill(0)
    oled.text('Graphics Test:', 0, 0)
    
    # Draw rectangles
    oled.rect(10, 15, 30, 20, 1)
    oled.fill_rect(50, 15, 30, 20, 1)
    
    # Draw lines
    oled.line(0, 40, 127, 40, 1)
    oled.line(64, 0, 64, 63, 1)
    
    # Draw pixels
    for x in range(0, 128, 4):
        oled.pixel(x, 50, 1)
    
    oled.show()
    time.sleep(3)
    
    # Test 4: Contrast
    print("Test 4: Testing contrast...")
    for contrast_val in [0x00, 0x7F, 0xFF, 0xCF]:
        oled.fill(0)
        oled.text(f'Contrast: {hex(contrast_val)}', 0, 20)
        oled.show()
        oled.contrast(contrast_val)
        time.sleep(1)
    
    print("Test complete! Check if display shows clear text and graphics.")
    return oled

# Run the test
if __name__ == "__main__":
    test_custom_driver()
