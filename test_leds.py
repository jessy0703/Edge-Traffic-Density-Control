import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)  # RED
GPIO.setup(27, GPIO.OUT)  # YELLOW
GPIO.setup(22, GPIO.OUT)  # GREEN

try:
    print("Testing RED LED...")
    GPIO.output(17, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(17, GPIO.LOW)
    print("✅ RED LED works!")
    
    print("\nTesting YELLOW LED...")
    GPIO.output(27, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(27, GPIO.LOW)
    print("✅ YELLOW LED works!")
    
    print("\nTesting GREEN LED...")
    GPIO.output(22, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(22, GPIO.LOW)
    print("✅ GREEN LED works!")
    
    print("\n🎉 All LEDs working perfectly!")
    
finally:
    GPIO.cleanup()
    print("GPIO cleaned up")
