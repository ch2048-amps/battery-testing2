import pyvisa
import time

duration = 3
t = 1               # time between samples
i = 0               # loop counter

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
    agilentMM = rm.open_resource('USB0::0x0957::0x1A07::MY53200185::0::INSTR')

    print("Query 1: " + agilentMM.query('*IDN?'))
    agilentMM.write("*rst; status:preset; *cls")

    '''timeout'''
    agilentMM.timeout = 10000 # 10s

    # Define string terminations
    agilentMM.write_termination = '\n'
    agilentMM.read_termination = '\n'
   
    # Set string terminations
    print('VISA termination string (write) set to newline: ASCII ',
          ord(agilentMM.write_termination))
    print('VISA termination string (read) set to newline: ASCII ',
          ord(agilentMM.read_termination))

    # Get the ID info 
    print('supply ID string:\n  ', agilentMM.query('*IDN?'), flush=True)
    print("completed setup. \n")

    # Code goes here
    print("Begin Instructions \n")
    # Do basic setup for the power supply

    agilentMM.write('CONF:VOLT:DC')
    #agilentMM.write('TRIG:SOUR EXT;SLOP POS') # this sets the trigger to when the thing being measured will be a sudden input; don't use otherwise

    '''
    Some info
    # agilentMM.write('READ?') # samples measurements slower than using INIT to get all measurements, then FETC to read all
    # agilentMM.write('INIT')  # log a measurement in the buffer
    # agilentMM.write('FETC?') # read from the buffer
    # print("Attempt to enable channel outputs")

    # A MEAS command sends 'CONF' followed by 'TRIG' and 'READ?'
    # agilentMM.write('CONF:CURR:DC 10, 0.001') # select 10 A range, 1mA resolution
    # agilentMM.write('TRIG:SOUR EXT; SLOP POS') # use positive slope as trigger for measurement
    # to take a subsequent reading:
    # print(agilentMM.write('INIT'))
    # print(agilentMM.write('FETC?'))

    # configure voltage lim (the max is 1000, but AC is 750Vrms)
    # agilentMM.write('CONF:VOLT:DC 10 0.001') # first configure DC
    # agilentMM.write('TRIG:SOUR EXT; SLOP POS') # use positive slope as trigger for measurement
    # print(agilentMM.write('INIT'))
    # print(agilentMM.write('FETC?'))

    # agilentMM.write('CONF:VOLT:AC 2 0.001') # ac measurement example 
    # agilentMM.write('SAMP:COUN 2')
    # agilentMM.write('READ?')
    '''

    print(" Channels Enabled.")

    print("attempt data collection")
    print(agilentMM.query('MEAS:VOLT:DC? 10,0.001')) # get the voltage in 10V range, 1mV resolution
    print(agilentMM.query('MEAS:CURR:AC? 1'))
    time.sleep(2)
    print(agilentMM.query('MEAS:VOLT:DC? 10,0.001')) # get the voltage in 10V range, 1mV resolution
    print(agilentMM.query('MEAS:CURR:AC? 1'))
    
    # for some reason this program does not co-operate using for loops
    while(duration - t*i >= 0):
        print(agilentMM.query('MEAS:VOLT:DC? 10,0.001')) # get the voltage in 10V range, 1mV resolution
        print(agilentMM.query('MEAS:CURR:AC? 1'))
        i += 1
        time.sleep(t)

    print("end of prog")

except(KeyboardInterrupt):
    print('Keyboard Interrupted execution!')

except:
    print('Timeout!')
time.sleep(3)
agilentMM.close()

