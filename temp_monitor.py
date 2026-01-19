import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
BUZZER_PIN = 12            # red wire on pin 12 now
LED_PIN = 11
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.LOW)
GPIO.output(LED_PIN, GPIO.LOW)

sensor_id = "28-0000006d17a6"
sensor_file = "/sys/bus/w1/devices/" + sensor_id + "/w1_slave"
ALARM_LIMIT = 30.0

print("Reading Temperature with Alarm...")

try:
    while True:
        try:
            with open(sensor_file, "r") as f:
                text = f.read()

            if "YES" in text:
                pos = text.find("t=")
                if pos != -1:
                    temp_string = text[pos+2:]
                    celsius = float(temp_string) / 1000.0
                    print(f"Current Temp: {celsius:.2f} C")

                    if celsius > ALARM_LIMIT:
                        GPIO.output(BUZZER_PIN, GPIO.HIGH)
                        GPIO.output(LED_PIN, GPIO.HIGH)
                    else:
                        GPIO.output(BUZZER_PIN, GPIO.LOW)
                        GPIO.output(LED_PIN, GPIO.LOW)
                else:
                    print("Reading...")
            else:
                print("Sensor not ready...")

            time.sleep(1)

        except Exception as e:
            print(f"Error reading sensor: {e}")
            time.sleep(1)

except KeyboardInterrupt:
    print("Stopped by user")

finally:
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.cleanup()
