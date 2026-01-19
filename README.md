# Smart Walker

A health monitoring system for wearable devices that tracks vital signs and environmental conditions using a Raspberry Pi.

## Features

- **Heart Rate Monitoring**: Real-time heart rate measurement using the MAX30102 pulse oximetry sensor
- **Temperature Monitoring**: Temperature sensing with alarm capabilities for overheating detection
- **Data Acquisition**: Collects and processes physiological data from multiple sensors
- **Threaded Sensor Processing**: Non-blocking sensor data collection and processing

## Hardware Requirements

- Raspberry Pi (with GPIO support)
- MAX30102 Pulse Oximetry Sensor (I2C interface)
- DS18B20 Temperature Sensor (1-Wire interface)
- Buzzer and LED (for temperature alarm alerts)
- Appropriate power supply and connection cables

## Project Structure

- `main.py` - Main entry point for sensor data collection with command-line arguments
- `heartrate_monitor.py` - Heart rate monitoring class using threaded sensor processing
- `max30102.py` - MAX30102 sensor driver with register configuration
- `hrcalc.py` - Heart rate calculation algorithms
- `temp_monitor.py` - Temperature monitoring with alarm functionality
- `test.py` - Testing utilities

## Installation

1. Clone or download the project to your Raspberry Pi
2. Install required Python packages:
   ```bash
   pip install numpy
   sudo apt-get install python3-smbus
   sudo apt-get install python3-rpi.gpio
   ```

3. Enable I2C and 1-Wire interfaces on Raspberry Pi:
   ```bash
   sudo raspi-config
   ```

## Usage

### Basic Heart Rate Monitoring

Run the sensor for the default 30 seconds:
```bash
python3 main.py
```

### Custom Duration

Monitor for a specific duration in seconds:
```bash
python3 main.py -t 60
```

### Raw Data Output

Print raw sensor data instead of processed results:
```bash
python3 main.py -r
```

### Combined Options

Get raw data for 60 seconds:
```bash
python3 main.py -r -t 60
```

## Features

### Heart Rate Monitoring
- Continuous data collection from MAX30102 sensor
- Real-time BPM (Beats Per Minute) calculation
- Configurable averaging for stable readings
- Both raw and processed output modes

### Temperature Monitoring
- Continuous temperature sensor polling
- Configurable alarm threshold (default: 30°C)
- Audio and visual alerts via buzzer and LED
- Celsius temperature readout

## Configuration

- **Heart Rate Loop Time**: 10ms (configurable in `HeartRateMonitor.LOOP_TIME`)
- **Temperature Alarm Limit**: 30.0°C (configurable in `temp_monitor.py`)
- **DS18B20 Sensor ID**: Configured in `temp_monitor.py`

## GPIO Pin Configuration

- **Buzzer Pin**: GPIO 12 (Board numbering)
- **LED Pin**: GPIO 11 (Board numbering)

## Notes

- The MAX30102 driver was originally designed for Python 2.7 but has been adapted for Python 3
- Ensure proper I2C address configuration for the MAX30102 sensor
- Temperature sensor requires 1-Wire protocol support enabled
- Keyboard interrupt (Ctrl+C) gracefully stops sensor operation

## License

This project is provided as-is for educational and health monitoring purposes.

## Support

For issues or questions, please review the individual module documentation or consult the sensor datasheets:
- MAX30102 Pulse Oximetry Sensor Datasheet
- DS18B20 Digital Thermometer Datasheet
