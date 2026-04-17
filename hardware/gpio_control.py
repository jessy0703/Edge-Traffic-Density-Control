import os
import time

class TrafficSignalController:
    def __init__(self):
        """Initialize GPIO for traffic signals"""
        self.RED_PIN = 17
        self.YELLOW_PIN = 27
        self.GREEN_PIN = 22
        self.gpio_available = False
        
        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.RED_PIN, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(self.YELLOW_PIN, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(self.GREEN_PIN, GPIO.OUT, initial=GPIO.LOW)
            self.GPIO = GPIO
            self.gpio_available = True
            print("[GPIO] ✅ Hardware mode initialized")
        except Exception as e:
            print(f"[GPIO] ⚠️  Simulation mode ({str(e)[:50]})")
            self.GPIO = None
    
    def set_signal(self, signal):
        """Set traffic signal LED"""
        if not self.gpio_available:
            if signal == "RED":
                print("[SIGNAL] 🔴 RED - High Traffic (STOP)")
            elif signal == "YELLOW":
                print("[SIGNAL] 🟡 YELLOW - Medium Traffic (PREPARE)")
            elif signal == "GREEN":
                print("[SIGNAL] 🟢 GREEN - Low Traffic (GO)")
            return
        
        try:
            self.GPIO.output(self.RED_PIN, self.GPIO.LOW)
            self.GPIO.output(self.YELLOW_PIN, self.GPIO.LOW)
            self.GPIO.output(self.GREEN_PIN, self.GPIO.LOW)
            
            if signal == "RED":
                self.GPIO.output(self.RED_PIN, self.GPIO.HIGH)
                print("[SIGNAL] 🔴 RED - High Traffic (STOP)")
            elif signal == "YELLOW":
                self.GPIO.output(self.YELLOW_PIN, self.GPIO.HIGH)
                print("[SIGNAL] 🟡 YELLOW - Medium Traffic (PREPARE)")
            elif signal == "GREEN":
                self.GPIO.output(self.GREEN_PIN, self.GPIO.HIGH)
                print("[SIGNAL] 🟢 GREEN - Low Traffic (GO)")
        except Exception as e:
            print(f"[GPIO Error] {e}")
    
    def cleanup(self):
        """Clean up GPIO"""
        if self.gpio_available and self.GPIO:
            try:
                self.GPIO.cleanup()
                print("[GPIO] ✅ Cleaned up")
            except:
                pass
