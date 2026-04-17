import os
import time

class TrafficSignalController:
    def __init__(self):
        """Initialize GPIO for traffic signals"""
        self.RED_PIN = 17
        self.YELLOW_PIN = 27
        self.GREEN_PIN = 22
        
        # Try to initialize real GPIO, fall back to simulation
        self.gpio_available = self._init_gpio()
        
        if self.gpio_available:
            print("[GPIO] ✅ Traffic signal controller initialized (HARDWARE MODE)")
        else:
            print("[GPIO] ⚠️  Running in SIMULATION MODE")
    
    def _init_gpio(self):
        """Try to initialize GPIO"""
        try:
            # Try direct sysfs approach
            for pin in [self.RED_PIN, self.YELLOW_PIN, self.GREEN_PIN]:
                os.system(f"echo {pin} > /sys/class/gpio/export 2>/dev/null")
            time.sleep(0.2)
            
            for pin in [self.RED_PIN, self.YELLOW_PIN, self.GREEN_PIN]:
                os.system(f"echo out > /sys/class/gpio/gpio{pin}/direction 2>/dev/null")
            
            return True
        except:
            return False
    
    def set_signal(self, signal):
        """Set traffic signal LED"""
        if not self.gpio_available:
            # Simulation mode
            if signal == "RED":
                print("[SIGNAL] 🔴 RED - High Traffic (STOP)")
            elif signal == "YELLOW":
                print("[SIGNAL] 🟡 YELLOW - Medium Traffic (PREPARE)")
            elif signal == "GREEN":
                print("[SIGNAL] 🟢 GREEN - Low Traffic (GO)")
            return
        
        # Hardware mode - try to control LEDs
        try:
            # Turn off all
            os.system(f"echo 0 > /sys/class/gpio/gpio{self.RED_PIN}/value 2>/dev/null")
            os.system(f"echo 0 > /sys/class/gpio/gpio{self.YELLOW_PIN}/value 2>/dev/null")
            os.system(f"echo 0 > /sys/class/gpio/gpio{self.GREEN_PIN}/value 2>/dev/null")
            
            # Turn on selected
            if signal == "RED":
                os.system(f"echo 1 > /sys/class/gpio/gpio{self.RED_PIN}/value 2>/dev/null")
                print("[SIGNAL] 🔴 RED - High Traffic (STOP)")
            elif signal == "YELLOW":
                os.system(f"echo 1 > /sys/class/gpio/gpio{self.YELLOW_PIN}/value 2>/dev/null")
                print("[SIGNAL] 🟡 YELLOW - Medium Traffic (PREPARE)")
            elif signal == "GREEN":
                os.system(f"echo 1 > /sys/class/gpio/gpio{self.GREEN_PIN}/value 2>/dev/null")
                print("[SIGNAL] 🟢 GREEN - Low Traffic (GO)")
        except Exception as e:
            print(f"[GPIO Error] {e}")
    
    def cleanup(self):
        """Clean up GPIO"""
        if self.gpio_available:
            try:
                for pin in [self.RED_PIN, self.YELLOW_PIN, self.GREEN_PIN]:
                    os.system(f"echo 0 > /sys/class/gpio/gpio{pin}/value 2>/dev/null")
                    os.system(f"echo {pin} > /sys/class/gpio/unexport 2>/dev/null")
                print("[GPIO] ✅ Cleaned up")
            except:
                pass
