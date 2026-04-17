import Jetson.GPIO as GPIO
import time

# Set up pins
RED_PIN = 17
YELLOW_PIN = 27
GREEN_PIN = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(YELLOW_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(GREEN_PIN, GPIO.OUT, initial=GPIO.LOW)

try:
    print("🔴 Testing RED LED...")
    GPIO.output(RED_PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(RED_PIN, GPIO.LOW)
    print("✅ RED LED works!")
    
    print("\n🟡 Testing YELLOW LED...")
    GPIO.output(YELLOW_PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(YELLOW_PIN, GPIO.LOW)
    print("✅ YELLOW LED works!")
    
    print("\n🟢 Testing GREEN LED...")
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(GREEN_PIN, GPIO.LOW)
    print("✅ GREEN LED works!")
    
    print("\n🎉 All LEDs working!")
    
finally:
    GPIO.cleanup()
    print("GPIO cleaned up")