import os
import time
import atexit
import signal

class TrafficSignalController:
    def __init__(self):
        """Initialize GPIO for traffic signals"""
        self.RED_PIN = 17
        self.YELLOW_PIN = 27
        self.GREEN_PIN = 22
        self.gpio_available = False
        
        # Debounce variables
        self.current_signal = None
        self.signal_change_time = 0
        self.min_signal_duration = 2  # Keep signal for at least 2 seconds
        self.signal_buffer = []
        self.buffer_size = 5  # Smooth over 5 frames

        try:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.RED_PIN, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(self.YELLOW_PIN, GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(self.GREEN_PIN, GPIO.OUT, initial=GPIO.LOW)
            self.GPIO = GPIO
            self.gpio_available = True
            print("[GPIO] ✅ Hardware mode initialized")
            
            # Register cleanup on exit only
            atexit.register(self.cleanup)
            
        except Exception as e:
            print(f"[GPIO] ⚠️  Simulation mode ({str(e)[:50]})")
            self.GPIO = None

    def set_signal(self, signal):
        """Set traffic signal LED with debouncing"""
        
        # Add signal to buffer
        self.signal_buffer.append(signal)
        if len(self.signal_buffer) > self.buffer_size:
            self.signal_buffer.pop(0)
        
        # Use majority vote from buffer (smooth out fluctuations)
        if len(self.signal_buffer) == self.buffer_size:
            signal_counts = {
                "RED": self.signal_buffer.count("RED"),
                "YELLOW": self.signal_buffer.count("YELLOW"),
                "GREEN": self.signal_buffer.count("GREEN")
            }
            smoothed_signal = max(signal_counts, key=signal_counts.get)
        else:
            smoothed_signal = signal
        
        # Only change if signal is different AND minimum time has passed
        current_time = time.time()
        if smoothed_signal != self.current_signal and \
           (current_time - self.signal_change_time) >= self.min_signal_duration:
            
            self.current_signal = smoothed_signal
            self.signal_change_time = current_time
            self._activate_signal(smoothed_signal)

    def _activate_signal(self, signal):
        """Actually activate the LED"""
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
                # Turn off all LEDs first
                self.GPIO.output(self.RED_PIN, self.GPIO.LOW)
                self.GPIO.output(self.YELLOW_PIN, self.GPIO.LOW)
                self.GPIO.output(self.GREEN_PIN, self.GPIO.LOW)
                time.sleep(0.5)
                self.GPIO.cleanup()
                print("[GPIO] ✅ Cleaned up")
            except Exception as e:
                print(f"[GPIO Cleanup Error] {e}")