# keithley power supply basic program

import pyvisa
import time

# this is only to use keysight devices
rm = pyvisa.ResourceManager(r'C:\WINDOWS\system32\visa64.dll')

print("Resource Manager: ")
print(rm)
print("\nList all resources: ")
print(rm.list_resources())
print()

try:
    '''connect to instrument'''
    print("Attempt initation:")
    keithleyPS = rm.open_resource('USB0::0x05E6::0x2230::9104291::0::INSTR')    
    print("opened")

    print("Query 1: " + keithleyPS.query('*IDN?'))
    keithleyPS.write("*rst; status:preset; *cls")

    '''timeout'''
    keithleyPS.timeout = 10000 # 10s

    # Define string terminations
    keithleyPS.write_termination = '\n'
    keithleyPS.read_termination = '\n'
   
    # Set string terminations
    print('VISA termination string (write) set to newline: ASCII ',
          ord(keithleyPS.write_termination))
    print('VISA termination string (read) set to newline: ASCII ',
          ord(keithleyPS.read_termination))

    # Get the ID info of the power supply
    print('supply ID string:\n  ', keithleyPS.query('*IDN?'), flush=True)
    print("completed setup. \n")

    # Code goes here
    print("Begin Instructions \n")
    # Do basic setup for the power supply
    # keithleyPS.write('CAL:CLE') # clear calibration 

    print("Attempt to enable channel outputs")

    # Set voltage level limit?
    # Set current level limit?

    keithleyPS.write('INST CH1')     # select channel 1
    keithleyPS.write('CHAN:OUTP ON') # enable the channel output

    keithleyPS.write('INST CH2')     # select channel 2
    keithleyPS.write('CHAN:OUTP ON') # enable the channel output

    keithleyPS.write('INST CH3')     # select channel 3
    keithleyPS.write('CHAN:OUTP ON') # enable the channel output

    print(" Channels Enabled.")
    print(" Last selected channel: " + keithleyPS.query('INST?')) # queries what channel is on
    print("\n")

    # set output of each channel (this is just a random block test
    # print("Attempt outputs")
    keithleyPS.write('APPL CH1, 1.03, 0.0')  
    keithleyPS.write('APPL CH2, 1.16, 0.0')  
    keithleyPS.write('APPL CH3, 1.13, 0.0') 
    # print(" Outputs set. \n")
    
    # can replace ALL with CH1, CH2, CH3 or ALL
    print("Query output: ")
    print(" Voltage: " + keithleyPS.query('FETC:VOLT? ALL')) # read the outputted voltage
    print(" Current: " + keithleyPS.query('FETC:CURR? ALL')) # read the outputted current
    print(" Power: " + keithleyPS.query('FETC:POW? ALL'))  # read the power outputted

    # measure vs fetch
    # measure: take a new single-point measurement
    # fetch: retrieve the most recent measurement after measruement cycle initiated with INIT
    # fetch tends to be faster

		# '''Turn on the power supply for t[s], then off for t[s] for [rounds] rounds'''
    rounds = 2
    t = 0.1*60 # time per round in seconds

    for i in range (rounds):
        keithleyPS.write('APPL CH1, 1.00, 0.0')  
        time.sleep(t)
        keithleyPS.write('APPL CH1, 0.00, 0.0')
        time.sleep(t)

    print("end")

except(KeyboardInterrupt):
    print('Keyboard Interrupted execution!')

except:
    print('Timeout!')
time.sleep(3)
keithleyPS.close()
