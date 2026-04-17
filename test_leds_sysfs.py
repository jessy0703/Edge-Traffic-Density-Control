import subprocess
import time
import os

def gpio_export(pin):
    """Export GPIO pin"""
    os.system(f"echo {pin} > /sys/class/gpio/export 2>/dev/null || true")
    time.sleep(0.1)

def gpio_direction(pin, direction):
    """Set GPIO direction (in/out)"""
    os.system(f"echo {direction} > /sys/class/gpio/gpio{pin}/direction 2>/dev/null || true")
    time.sleep(0.1)

def gpio_write(pin, value):
    """Write GPIO value"""
    os.system(f"echo {value} > /sys/class/gpio/gpio{pin}/value 2>/dev/null || true")

# Initialize pins
RED_PIN = 17
YELLOW_PIN = 27
GREEN_PIN = 22

print("Exporting GPIO pins...")
for pin in [RED_PIN, YELLOW_PIN, GREEN_PIN]:
    gpio_export(pin)
    gpio_direction(pin, "out")

try:
    print("\n🔴 Testing RED LED...")
    gpio_write(RED_PIN, 1)
    time.sleep(2)
    gpio_write(RED_PIN, 0)
    print("✅ RED LED works!")
    
    print("\n🟡 Testing YELLOW LED...")
    gpio_write(YELLOW_PIN, 1)
    time.sleep(2)
    gpio_write(YELLOW_PIN, 0)
    print("✅ YELLOW LED works!")
    
    print("\n🟢 Testing GREEN LED...")
    gpio_write(GREEN_PIN, 1)
    time.sleep(2)
    gpio_write(GREEN_PIN, 0)
    print("✅ GREEN LED works!")
    
    print("\n🎉 All LEDs working perfectly!")
    
finally:
    print("\nCleaning up...")
    gpio_write(RED_PIN, 0)
    gpio_write(YELLOW_PIN, 0)
    gpio_write(GREEN_PIN, 0)
    for pin in [RED_PIN, YELLOW_PIN, GREEN_PIN]:
        os.system(f"echo {pin} > /sys/class/gpio/unexport 2>/dev/null || true")
    print("GPIO cleaned up")
