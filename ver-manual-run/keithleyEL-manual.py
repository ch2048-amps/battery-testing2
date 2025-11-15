# keithley power supply basic program

import pyvisa
import time

# parameters Unit
n = 2       # [ ] number of total measurements (is TotalTime/t)
t = 6       # [s] time between measurements in seconds

TotalTime = n*t     # total time in seconds, unused is for reference

# Continue prog
rm = pyvisa.ResourceManager(r'C:\WINDOWS\system32\visa64.dll')

print("Resource Manager: ")
print(rm)
print("\nList all resources: ")
print(rm.list_resources())
print()

try:
    '''connect to instrument'''
    print("Attempt initation:")
    keithleyEL = rm.open_resource('USB0::0x05E6::0x2380::802436012717810052::INSTR')
    print("open el")

    print("Query 1: " + keithleyEL.query('*IDN?'))
    keithleyEL.write("*rst; status:preset; *cls")

    '''timeout'''
    keithleyEL.timeout = 10000 # 10s

    # Define string terminations
    keithleyEL.write_termination = '\n'
    keithleyEL.read_termination = '\n'
   
    # Set string terminations
    print('VISA termination string (write) set to newline: ASCII ',
          ord(keithleyEL.write_termination))
    print('VISA termination string (read) set to newline: ASCII ',
          ord(keithleyEL.read_termination))

    # Get the ID info of the power supply
    print('supply ID string:\n  ', keithleyEL.query('*IDN?'), flush=True)
    print("completed setup. \n")

    # Code goes here
    print("Begin Instructions \n")
    # Do basic setup for the power supply
    # keithleyEL.write('CAL:CLE') # clear calibration 

    print("Attempt to enable channel outputs")

    # Set voltage level limit?
    # Set current level limit?
    print("dc load start init")
    keithleyEL.write('CURR:PROT:STAT 1') # enable over-current protection
    keithleyEL.write('CURR:PROT:LEV 2')  # set over-current level [A]
    keithleyEL.write('CURR:PROT:DEL 1')  # set amt time [s] oc level can be violated
    print("init dc load")

    # # set voltage bounds in CC [V]
    # keithleyEL.write('CURR:LOW 1')
    # keithleyEL.write('CURR:HIGH 2')

    # # set voltage load regulates when operating in CV [V]
    # keithleyEL.write('VOLT 5')

    # # set current bounds in CV mode [A]
    # keithleyEL.write('VOLT:LOW 1')
    # keithleyEL.write('VOLT:HIGH 2')
    
    # # set resistance when operating in constant resistance mode [OHMS]
    # keithleyEL.write('RES 5')


    # can replace ALL with CH1, CH2, CH3 or ALL
    print("Query output: ")
    print(" Voltage: " + keithleyEL.query('FETC:VOLT?')) # read the outputted voltage
    # print(" Maximum Current: " + keithleyEL.query('FETC:CURR?:MAX')) # read the outputted current
    # print(" Minimum Current: " + keithleyEL.query('FETC:CURR?:MIN')) # read the outputted current
    # print(" Maximum Power: " + keithleyEL.query('FETC:POW?:MAX'))  # read the power outputted
    # print(" Minimum Power: " + keithleyEL.query('FETC:POW?:MIN'))  # read the power outputted
  
    # commands:
    # print(keithleyEL.query('FETC:VOLT?')) # get the voltage across the terminals
    # print(keithleyEL.query('FETC:VOLT:MAX?')) # get the maximum last recprded voltage
    # print(keithleyEL.query('FETC:VOLT:MIN?')) # get the minimum last recorded voltage
    # print(keithleyEL.query('FETC:CURR:MAX?'))
    # print(keithleyEL.query('FETC:CURR:MIN?'))
    # print(keithleyEL.query('FETC:POW:MAX?'))
    # print(keithleyEL.query('FETC:POW:MIN?'))

    # measure vs fetch
    # measure: take a new single-point measurement
    # fetch: retrieve the most recent measurement after measruement cycle initiated with INIT
    # fetch tends to be faster

	# '''Take [n] measurements spaced every t[s]'''
    for i in range (n):
        print(" Voltage: " + keithleyEL.query('FETC:VOLT?')) # read the outputted voltage
        # print(" Maximum Current: " + keithleyEL.query('FETC:CURR?:MAX')) # read the outputted current
        # print(" Minimum Current: " + keithleyEL.query('FETC:CURR?:MIN')) # read the outputted current
        # print(" Maximum Power: " + keithleyEL.query('FETC:POW?:MAX'))  # read the power outputted
        # print(" Minimum Power: " + keithleyEL.query('FETC:POW?:MIN'))  # read the power outputted

        time.sleep(t)

    print("end")

except(KeyboardInterrupt):
    print('Keyboard Interrupted execution!')

except:
    print('Timeout!')
time.sleep(3)
keithleyEL.close()
