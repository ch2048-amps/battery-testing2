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
    print("del 1")
    keithleyPS = rm.open_resource('USB0::0x05E6::0x2230::9104291::INSTR')
    print("open ps")
    keithleyEL = rm.open_resource('USB0::0x05E6::0x2380::802436012717810052::INSTR')
    print("open el")

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

    # set output of each channel
    print("Attempt outputs")
    keithleyPS.write('APPL CH1, 1.03, 0.0')  
    keithleyPS.write('APPL CH2, 1.16, 0.0')  
    keithleyPS.write('APPL CH3, 1.13, 0.0') 
    print(" Outputs set. \n")
    
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
    # rounds = 2
    # t = 45*60 # time per round in seconds

    # for i in range (rounds):
    #     keithleyPS.write('APPL CH1, 1.00, 0.0')  
    #     time.sleep(t)
    #     keithleyPS.write('APPL CH1, 0.00, 0.0')
    #     time.sleep(t)

    # print("end")


    # DC load thing
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
    print("attempt fetch")
    print(keithleyEL.query('FETC:VOLT?')) # get the voltage across the terminals
    # print(keithleyEL.query('FETC:VOLT:MAX?')) # get the maximum last recprded voltage
    # print(keithleyEL.query('FETC:VOLT:MIN?')) # get the minimum last recorded voltage
    # print(keithleyEL.query('FETC:CURR:MAX?'))
    # print(keithleyEL.query('FETC:CURR:MIN?'))
    # print(keithleyEL.query('FETC:POW:MAX?'))
    # print(keithleyEL.query('FETC:POW:MIN?'))
    print("end of prog")

except(KeyboardInterrupt):
    print('Keyboard Interrupted execution!')

except:
    print('Timeout!')
time.sleep(3)
keithleyPS.close()

