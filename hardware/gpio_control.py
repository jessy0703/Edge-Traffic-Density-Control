class TrafficSignalController:
    def __init__(self):
        """Initialize GPIO for traffic signals"""
        print("[GPIO] Traffic signal controller initialized (simulation mode)")
    
    def set_signal(self, signal):
        """Set traffic signal LED"""
        if signal == "RED":
            print("[SIGNAL] 🔴 RED - High Traffic (STOP)")
        elif signal == "YELLOW":
            print("[SIGNAL] 🟡 YELLOW - Medium Traffic (PREPARE)")
        elif signal == "GREEN":
            print("[SIGNAL] 🟢 GREEN - Low Traffic (GO)")
    
    def cleanup(self):
        """Clean up GPIO"""
        print("[GPIO] Cleaned up")
