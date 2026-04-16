import RPi.GPIO as GPIO
import time

# GPIO Pin definitions
RED_PIN = 17
YELLOW_PIN = 27
GREEN_PIN = 22

class TrafficSignalController:
    def __init__(self):
        """Initialize GPIO for traffic signals"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RED_PIN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(YELLOW_PIN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(GREEN_PIN, GPIO.OUT, initial=GPIO.LOW)
        print("[GPIO] Traffic signal controller initialized")
    
    def set_signal(self, signal):
        """Set traffic signal LED"""
        # Turn off all LEDs first
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(YELLOW_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        
        # Turn on selected LED
        if signal == "RED":
            GPIO.output(RED_PIN, GPIO.HIGH)
            print("[SIGNAL] 🔴 RED - High Traffic (STOP)")
        elif signal == "YELLOW":
            GPIO.output(YELLOW_PIN, GPIO.HIGH)
            print("[SIGNAL] 🟡 YELLOW - Medium Traffic (PREPARE)")
        elif signal == "GREEN":
            GPIO.output(GREEN_PIN, GPIO.HIGH)
            print("[SIGNAL] 🟢 GREEN - Low Traffic (GO)")
        else:
            print(f"[ERROR] Unknown signal: {signal}")
    
    def cleanup(self):
        """Clean up GPIO"""
        GPIO.cleanup()
        print("[GPIO] Cleaned up")

# Usage example
if __name__ == "__main__":
    controller = TrafficSignalController()
    
    try:
        controller.set_signal("RED")
        time.sleep(2)
        controller.set_signal("YELLOW")
        time.sleep(2)
        controller.set_signal("GREEN")
        time.sleep(2)
    finally:
        controller.cleanup()
