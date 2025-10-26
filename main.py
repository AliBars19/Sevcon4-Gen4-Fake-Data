#what does the sevcon4 gen4 node generally record?

#DOUBLE CHECK ALL ALLEGADLY VALUES

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