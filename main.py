#Motor speed 
#       - speed of the motor lol
#       - (RPM)(Allegadly between 0-8000rpm)(Can support up to 10000rpm)
#Theoretical motor torque
#       - Requested motor torque
#       - (Nm)(10hz)(Allegadly between -60Nm to 60Nm)
#Actual motor torque
#       - Actual measured motor torque
#       - (Nm)(10hz)(Allegadly between -60Nm to 60Nm)(apparently can spike to 80Nm)
#Motor Phase Current
#       - Current across three inverter output phases
#       - (Amps)(10hz)(Allegadly between 0A to 350A)(can spike to 400A)
#Motor Frequency
#       - Electrical frequency of the three phase AC Waveform sent to motor
#       - (Hz)(10hz)(Allegadly between 0Hz to 400hz)
#       - IMPORTANT: FREQ HEAVILY DEPENDS ON MOTOR SPEED RPM RANGE
#       - For this data were gna use 0-8000rpm - 0-400hz
#Heat Sink Temperature
#       - Temperature of the heat sink inside the sevcon
#       - (Celsius)(1hz)(Allegadly between 25 to 85 degrees celsius)(cuts around 90)
#Motor Temperature
#       - Temperature of the motor thermistor(i think)
#       - (Celsius)(1hz)(Allegadly between 30 to 120 degrees celsius)(cuts around 130)
#DC Bus Voltage
#       - Inverters input voltage from the accumulator
#       - (Volts)(10hz)(Allegadly between 80V to 120V)(can spike to 450V)
#DC Bus Current
#       - Total current flowing in and out of the converter
#       - (Amps)(10hz)(Allegadly between 0A to 300A)
#       - (would start from -300 but we dont have regenerative braking)

#------------------

import json
from time import time_ns
from mcap.writer import Writer
from mcap.reader import make_reader
from numpy import number
 
#------------------
#MCAP WRITER FOR GPS DATA, EDITED FOR GPS SCHEMA (check gps-corrected-schema.json for reference)
#------------------

can_data = "sevcon_gen4_fake_silverstone_lap.json"

# get json data from file 
with open(can_data, "r") as f:
    gps_data = json.load(f)

with open("sevconfakedata.mcap", "wb") as stream:
    writer = Writer(stream)
    writer.start()

    # Register schema for CAN message format
    schema_speed = writer.register_schema(
        name="sevcon.Speed",
        encoding="jsonschema",
        data=json.dumps({
            "type": "object",
            "properties": {
                "motorspeed": {"type": "number"},
                "theoreticaltorque": {"type": "number"},
                "actualtorque": {"type": "number"},
            },
            "required": ["motorspeed", "theoreticaltorque", "actualtorque"]
        }).encode("utf-8"),
    )
    schema_phase = writer.register_schema(
        name="sevcon.Phase",
        encoding="jsonschema",
        data=json.dumps({
            "type": "object",
            "properties": {
                "phase": {"type": "number"},
                "frequency": {"type": "number"},
            },
            "required": ["phase", "frequency"]
        }).encode("utf-8"),
    )
    schema_temperature = writer.register_schema(
        name="sevcon.Temperature",
        encoding="jsonschema",
        data=json.dumps({
            "type": "object",
            "properties": {
                "Heatsink_temp": {"type": "number"},
                "motor_temperature": {"type": "number"},
            },
            "required": ["Heatsink_temp", "motor_temperature"]
        }).encode("utf-8"),
    )
    schema_electrical = writer.register_schema(
        name="sevcon.Electrical",
        encoding="jsonschema",
        data=json.dumps({
            "type": "object",
            "properties": {
                "DC_Bus_Voltage": {"type": "integer"},
                "DC_Bus_Current": {"type": "integer"},
            },
            "required": ["DC_Bus_Voltage", "DC_Bus_Current"]
        }).encode("utf-8"),
    )
    
    # Register channel
    channels = {
        "/vehicle/sevcon/speed": writer.register_channel(
            schema_id=schema_speed,
            topic="/vehicle/sevcon/speed",
            message_encoding="json",
        ),
        "/vehicle/sevcon/phase": writer.register_channel(
            schema_id=schema_phase,
            topic="/vehicle/sevcon/phase",
            message_encoding="json",
        ),
        "/vehicle/sevcon/temperature": writer.register_channel(
            schema_id=schema_temperature,
            topic="/vehicle/sevcon/temperature",
            message_encoding="json",
        ),
        "/vehicle/sevcon/electrical": writer.register_channel(
            schema_id=schema_electrical,
            topic="/vehicle/sevcon/electrical",
            message_encoding="json",
        ),
    }
    

    for entry in gps_data:
        topic = entry["topic"]
        log_time = int(entry["timestamp"])
        data_json = json.dumps(entry["data"]).encode("utf-8")
        
        # Add message to MCAP file
        writer.add_message(
            channel_id=channels[topic],
            log_time=log_time,
            publish_time=time_ns(),
            data=data_json,
        )

    writer.finish()

print("Reading MCAP file contents:")
print("=" * 50)

with open("sevconfakedata.mcap", "rb") as f:
    reader = make_reader(f)
    
    message_count = 0
    for schema, channel, message in reader.iter_messages():
        try:
            json_data = json.loads(message.data.decode("utf-8"))
            print(f"Message {message_count + 1}:")
            print(f"  Topic: {channel.topic}")
            print(f"  Log Time: {message.log_time}")
            print(f"  Data: {json_data}")
            print("-" * 30)
            message_count += 1
            
            
            # if message_count >= 5:
            #     print(f"... (showing first 5 messages out of total)")
            #     break
                
        except json.JSONDecodeError as e:
            print(f"JSON decode error in topic '{channel.topic}': {e}")
            print(f"Raw data: {message.data}")

# """