# Sevcon4-Gen4-Fake-Data

This project provides tools for generating and managing fake data for a Sevcon Gen4 motor controller, commonly used in Formula Student electric vehicles. The data generator creates realistic sensor readings that simulate various motor controller parameters during a lap at Silverstone circuit.

## Features

- Generates realistic fake data for Sevcon Gen4 motor controller parameters
- Supports multiple sensor channels:
  - Motor Speed (0-8000 RPM)
  - Theoretical and Actual Torque (-60 to 60 Nm)
  - Phase Current (0-350A) and Frequency (0-400Hz)
  - Heat Sink Temperature (25-85°C)
  - Motor Temperature (30-120°C)
  - DC Bus Voltage (80-120V) and Current (0-300A)
- Stores data in MCAP format for efficient storage and retrieval
- Includes JSON schema validation for data integrity

## Files

- `main.py` - Python script for generating and processing fake sensor data
- `sevcon-schema.json` - JSON schema definitions for all sensor channels
- `sevcon_gen4_fake_silverstone_lap.json` - Sample lap data in JSON format
- `sevconfakedata.mcap` - Generated MCAP file containing the processed data

## Data Channels

### Speed Channel (`/vehicle/sevcon/speed`)
- Motor speed (RPM)
- Theoretical torque (Nm)
- Actual torque (Nm)
- Update rate: 10Hz

### Phase Channel (`/vehicle/sevcon/phase`)
- Phase current (A)
- Electrical frequency (Hz)
- Update rate: 10Hz

### Temperature Channel (`/vehicle/sevcon/temperature`)
- Heat sink temperature (°C)
- Motor temperature (°C)
- Update rate: 1Hz

### Electrical Channel (`/vehicle/sevcon/electrical`)
- DC bus voltage (V)
- DC bus current (A)
- Update rate: 10Hz

## Usage

1. Ensure you have Python installed with the required packages (mcap-ros2-support)
2. Run the script:
   ```bash
   python main.py
   ```
3. The script will:
   - Read the sample lap data from `sevcon_gen4_fake_silverstone_lap.json`
   - Process and validate the data against the schema
   - Generate an MCAP file (`sevconfakedata.mcap`)
   - Display the contents of the generated MCAP file

## Technical Details

- Motor speed range: 0-8000 RPM (can support up to 10000 RPM)
- Torque range: -60 to 60 Nm (can spike to 80 Nm)
- Phase current: 0-350A (can spike to 400A)
- Frequency range: 0-400Hz (proportional to motor speed)
- Heat sink temperature: 25-85°C (cuts off around 90°C)
- Motor temperature: 30-120°C (cuts off around 130°C)
- DC bus voltage: 80-120V (can spike to 450V)
- DC bus current: 0-300A (no regenerative braking support)