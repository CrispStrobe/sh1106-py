# SH1106 Example Projects for your GME 12864-70 display
# Make sure you have sh1106.py saved on your ESP32 first!

from machine import Pin, I2C, ADC
import sh1106
import time
import random

# Initialize display
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
oled = sh1106.SH1106_I2C(128, 64, i2c)

def clock_display():
    """Digital clock display"""
    print("Starting digital clock...")
    for i in range(30):  # Run for 30 seconds
        current_time = time.ticks_ms()
        seconds = (current_time // 1000) % 60
        minutes = (current_time // 60000) % 60
        
        oled.fill(0)
        oled.text('Digital Clock', 20, 0)
        oled.text(f'{minutes:02d}:{seconds:02d}', 35, 25)
        oled.text('ESP32 + SH1106', 15, 50)
        oled.show()
        time.sleep(1)

def sensor_dashboard():
    """Fake sensor dashboard"""
    print("Starting sensor dashboard...")
    
    for i in range(20):
        # Generate fake sensor data
        temp = 20 + random.randint(-5, 15)
        humidity = 45 + random.randint(-10, 20)
        pressure = 1013 + random.randint(-20, 20)
        
        oled.fill(0)
        oled.text('Sensor Data', 25, 0)
        oled.text(f'Temp: {temp}C', 0, 15)
        oled.text(f'Humidity: {humidity}%', 0, 25)
        oled.text(f'Press: {pressure}hPa', 0, 35)
        oled.text(f'Reading #{i+1}', 0, 50)
        oled.show()
        time.sleep(2)

def bouncing_ball():
    """Bouncing ball animation"""
    print("Starting bouncing ball...")
    
    x, y = 64, 32
    dx, dy = 2, 1
    
    for _ in range(100):
        oled.fill(0)
        
        # Draw title
        oled.text('Bouncing Ball', 20, 0)
        
        # Draw borders
        oled.rect(0, 10, 128, 54, 1)
        
        # Update ball position
        x += dx
        y += dy
        
        # Bounce off walls
        if x <= 2 or x >= 125:
            dx = -dx
        if y <= 12 or y >= 61:
            dy = -dy
        
        # Draw ball (3x3 pixels)
        for i in range(3):
            for j in range(3):
                oled.pixel(x+i, y+j, 1)
        
        oled.show()
        time.sleep(0.05)

def scroll_text():
    """Scrolling text display"""
    print("Starting scrolling text...")
    
    message = "   Hello World! Your SH1106 display is working perfectly with ESP32 and MicroPython!   "
    
    for offset in range(len(message) * 8):
        oled.fill(0)
        oled.text('Scrolling Text:', 10, 0)
        
        # Calculate text position
        x = 128 - (offset % (len(message) * 8))
        oled.text(message, x, 25)
        
        # Draw some decoration
        oled.line(0, 15, 127, 15, 1)
        oled.line(0, 45, 127, 45, 1)
        
        oled.show()
        time.sleep(0.1)

def bargraph_demo():
    """Bar graph demo"""
    print("Starting bar graph demo...")
    
    for i in range(50):
        oled.fill(0)
        oled.text('Bar Graph Demo', 15, 0)
        
        # Generate random data for 4 bars
        values = [random.randint(5, 50) for _ in range(4)]
        
        # Draw bars
        bar_width = 20
        bar_spacing = 30
        
        for j, value in enumerate(values):
            x = 10 + j * bar_spacing
            y = 55 - value
            oled.fill_rect(x, y, bar_width, value, 1)
            oled.text(str(value), x+2, 57)
        
        oled.show()
        time.sleep(0.5)

def menu_system():
    """Simple menu system"""
    print("Starting menu system...")
    
    menu_items = ['Clock', 'Sensors', 'Animation', 'Graph', 'Exit']
    selected = 0
    
    for cycle in range(20):  # Auto-cycle through menu
        oled.fill(0)
        oled.text('Main Menu', 30, 0)
        oled.line(0, 12, 127, 12, 1)
        
        # Draw menu items
        for i, item in enumerate(menu_items):
            y = 20 + i * 10
            if i == selected:
                # Highlight selected item
                oled.fill_rect(0, y-1, 128, 9, 1)
                oled.text(f'> {item}', 5, y, 0)  # Inverted text
            else:
                oled.text(f'  {item}', 5, y)
        
        oled.show()
        time.sleep(1)
        
        # Move selection
        selected = (selected + 1) % len(menu_items)

def temperature_graph():
    """Temperature graph over time"""
    print("Starting temperature graph...")
    
    temp_history = []
    
    for i in range(64):  # 64 data points across width
        # Generate fake temperature data
        base_temp = 22
        temp = base_temp + 5 * (0.5 - random.random()) + 2 * (i % 10 - 5) / 5
        temp_history.append(temp)
        
        oled.fill(0)
        oled.text('Temperature', 25, 0)
        oled.text(f'Current: {temp:.1f}C', 0, 55)
        
        # Draw graph
        if len(temp_history) > 1:
            for j in range(1, len(temp_history)):
                x1 = j - 1
                x2 = j
                # Scale temperature to display (15-30°C range)
                y1 = 50 - int((temp_history[j-1] - 15) * 2)
                y2 = 50 - int((temp_history[j] - 15) * 2)
                
                # Clamp to display bounds
                y1 = max(15, min(50, y1))
                y2 = max(15, min(50, y2))
                
                oled.line(x1, y1, x2, y2, 1)
        
        # Draw axes
        oled.line(0, 50, 127, 50, 1)  # X-axis
        oled.line(0, 15, 0, 50, 1)    # Y-axis
        
        oled.show()
        time.sleep(0.5)

# Main demo runner
def run_all_demos():
    """Run all demos in sequence"""
    print("🎉 SH1106 Display Working! Running demos...")
    print("Watch your display for different animations!")
    
    demos = [
        ("Digital Clock", clock_display),
        ("Sensor Dashboard", sensor_dashboard),
        ("Bouncing Ball", bouncing_ball),
        ("Scrolling Text", scroll_text),
        ("Bar Graph", bargraph_demo),
        ("Menu System", menu_system),
        ("Temperature Graph", temperature_graph)
    ]
    
    for name, demo_func in demos:
        print(f"\n--- Running {name} ---")
        oled.fill(0)
        oled.text(f'Starting...', 30, 25)
        oled.text(name, 20, 35)
        oled.show()
        time.sleep(2)
        
        try:
            demo_func()
        except Exception as e:
            print(f"Demo {name} error: {e}")
        
        time.sleep(1)
    
    # Final message
    oled.fill(0)
    oled.text('All Demos', 30, 20)
    oled.text('Complete!', 30, 35)
    oled.show()
    print("\n🎉 All demos complete!")

# Quick test
def quick_test():
    """Quick test to verify display still works"""
    oled.fill(0)
    oled.text('SH1106 Working!', 15, 20)
    oled.text('ESP32 + Python', 15, 35)
    oled.show()

# Run a quick test
quick_test()
print("Quick test displayed - your SH1106 is ready!")
print("Uncomment run_all_demos() to see all the examples!")

# Uncomment the line below to run all demos:
# run_all_demos()
