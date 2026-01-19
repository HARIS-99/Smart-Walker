from heartrate_monitor import HeartRateMonitor
import time
import RPi.GPIO as GPIO
from gpiozero import LED

BUZZER_PIN = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)

# Temperature sensor
sensor_id = "28-0000006d17a6"
sensor_file = "/sys/bus/w1/devices/" + sensor_id + "/w1_slave"

# Alarm limits
TEMP_LOW = 18.0
TEMP_HIGH = 30.0
HR_LOW = 60
HR_HIGH = 120

# Setup LEDs
temp_led = LED(17)
hr_led = LED(14)

print("=" * 50)
print("  COMBINED HEALTH MONITORING SYSTEM")
print("=" * 50)
print("Starting sensors...\n")

# Start heart rate monitor
hr_monitor = HeartRateMonitor(print_result=False)
hr_monitor.start_sensor()

def read_temp():
    try:
        with open(sensor_file, "r") as f:
            text = f.read()
        if "YES" in text:
            pos = text.find("t=")
            if pos != -1:
                return float(text[pos+2:]) / 1000.0
    except:
        pass
    return None

try:
    print("Place finger on heart rate sensor...\n")
    
    while True:
        time.sleep(5)
        
        # Get readings
        celsius = read_temp()
        bpm = hr_monitor.bpm
        
        if celsius is not None:
            print("\n" + "=" * 50)
            print("         HEALTH STATUS")
            print("=" * 50)
            
            # Temperature
            temp_alarm = celsius < TEMP_LOW or celsius > TEMP_HIGH
            print(f"Temperature: {celsius:.1f}°C  [{('ALARM' if temp_alarm else 'OK')}]")
            temp_led.on() if temp_alarm else temp_led.off()
            
            # Heart Rate
            hr_alarm = bpm > 0 and (bpm < HR_LOW or bpm > HR_HIGH)
            print(f"Heart Rate:  {bpm:.0f} bpm  [{('ALARM' if hr_alarm else 'OK')}]")
            hr_led.on() if hr_alarm else hr_led.off()
            
            print("=" * 50)
            
            if temp_alarm or hr_alarm:
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                print("⚠ ALARM ACTIVE!\n")
            else:
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                print("✓ All Normal\n")

except KeyboardInterrupt:
    print("\n\nStopped by user")

finally:
    hr_monitor.stop_sensor()
    temp_led.off()
    hr_led.off()
    GPIO.output(BUZZER_PIN, GPIO.LOW) # add this line
    print("System stopped")
