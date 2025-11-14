import matplotlib.pyplot as plt 
import pyvisa as visa
import numpy as n
import time, csv

# variable definitions
windows = True

Vout = 0.0
time_idx = 0        # counter of current sample being processed
num_times = 20      # total number of samples to run
sampleDelay = 0.25   # delay between samples

# can translate the code to use testing time and number of points.
# sampleTimeHR = 1 # total time to run testing (hrs)
# sampleTimeMIN = 0
# sampleTimeSEC = 0
# sampleTimeTOT = sampleTimeHR*60*60 + sampleTimeMIN*60 + sampleTimeSEC
# sampleDelay = sampleTimeTOT/num_times
# --- #

if(windows):
    rm = visa.ResourceManager(r'C:\WINDOWS\system32\visa64.dll') # replace this with the windows location
else:
     rm = visa.ResourceManager(r'C:\WINDOWS\system32\visa64.dll') # replace this with the linux location

print(rm)
print(rm.list_resources('TCPIP0::?*'))

try:
    '''Connect to the instruments'''
    meter =  rm.open_resource('TCPIP0::192.168.0.252::5025::SOCKET')
    supply = rm.open_resource('TCPIP0::192.168.0.251::5025::SOCKET')
 

    ''' Set up the digital multimeter and supply IO configuration'''
    meter.timeout = 10000
    supply.timeout = 10000  

    # Define string terminations
    meter.write_termination = '\n'
    meter.read_termination = '\n'
    supply.write_termination = '\n'
    supply.read_termination = '\n'

    # Set string terminations
    print('\nVISA termination string (write) set to newline: ASCII ',
          ord(meter.write_termination))
    print('VISA termination string (read) set to newline: ASCII ',
          ord(meter.read_termination))
    print('\nVISA termination string (write) set to newline: ASCII ',
          ord(supply.write_termination))
    print('VISA termination string (read) set to newline: ASCII ',
          ord(supply.read_termination))

    # Get the ID info of the digital multimeter and supply
    print('meter ID string:\n  ', meter.query('*IDN?'), flush=True)
    print('supply ID string:\n  ', supply.query('*IDN?'), flush=True)
    
    # setting dmm voltage limits
    supply.write('VOLT:PROT 6, (@1)') # overvoltage protection
    print(supply.query('VOLT:PROT? (@1)'))
    supply.write('VOLT 5, (@1)') # voltage level of measurement
    print(supply.query('VOLT? (@1)'))

    # setting dmm current limits  
    supply.write('CURR 0.1, (@1)') # Set current limit
    print(supply.query('CURR? (@1)'))

    # Be sure to connect the power supply to the LM335 as shown above.
     
    meter.write('CONF:VOLT: DC') # set DC output

    # Set the number of datalogger measurements
    times = n.linspace(1,num_times,num_times) # generate a evenly spaced sequence of num_times numbers between [1, num_times]
    v = [0]*num_times                         # store the battery voltages

    # sample the voltages
    for i in times:
        Vout = meter.query('MEAS:VOLT:DC?') # get the battery voltage
        print(Vout)                         
        v[time_idx] = (float(Vout))         
        time.sleep(sampleDelay)             
        time_idx = time_idx + 1             

    # Plot the resulting temperatures
    plt.plot(times, v, label='N/A')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Voltage vs Time')
    plt.legend()
    plt.show()

except(KeyboardInterrupt):
    print('Keyboard Interrupted execution!')
    