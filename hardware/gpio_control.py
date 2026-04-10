# Safe GPIO mock for laptop testing

try:
    import Jetson.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)

    RED = 11
    YELLOW = 13
    GREEN = 15

    GPIO.setup(RED, GPIO.OUT)
    GPIO.setup(YELLOW, GPIO.OUT)
    GPIO.setup(GREEN, GPIO.OUT)

    def set_signal(signal):
        GPIO.output(RED, False)
        GPIO.output(YELLOW, False)
        GPIO.output(GREEN, False)

        if signal == "RED":
            GPIO.output(RED, True)
        elif signal == "YELLOW":
            GPIO.output(YELLOW, True)
        elif signal == "GREEN":
            GPIO.output(GREEN, True)

    def cleanup():
        GPIO.cleanup()

except:
    # Laptop fallback (no GPIO)
    def set_signal(signal):
        print(f"[SIMULATION] Signal: {signal}")

    def cleanup():
        print("[SIMULATION] Cleanup called")