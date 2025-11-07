import pyvisa
import time

rm = pyvisa.ResourceManager(r'C:\WINDOWS\system32\visa64.dll')
print(rm)
print(rm.list_resources('TCPIP0::?*'))

try:
    '''connect to instrument'''
    keithley = rm.open_resource("GPIB::12")
    keithley.write("*rst; status:preset; *cls")

    '''timeout'''
    keithley.timeout = 10000 # 10s

    # Define string terminations
    keithley.write_termination = '\n'
    keithley.read_termination = '\n'
   
    # Set string terminations
    print('\nVISA termination string (write) set to newline: ASCII ',
          ord(keithley.write_termination))
    print('VISA termination string (read) set to newline: ASCII ',
          ord(keithley.read_termination))

    # Get the ID info of the power supply
    print('supply ID string:\n  ', keithley.query('*IDN?'), flush=True)

    # Code goes here
    # Do basic setup for the power supply
    keithley.write('VOLT:PROT 6, (@1)') # Set overvoltage protection
    print(keithley.query('VOLT:PROT? (@1)'))
    keithley.write('VOLT 3.7, (@1)') # Set voltage level
    print(keithley.query('VOLT? (@1)'))
    keithley.write('CURR 2.5, (@1)') # Set current limit
    print(keithley.query('CURR? (@1)'))
    
    ''' Turn the output on, wait 5 seconds, then turn it off'''
    keithley.write('OUTP 1, (@1)')
    time.sleep(5)
    keithley.write('OUTP 0, (@1)')
    
except(KeyboardInterrupt):
    print('Keyboard Interrupted execution!')

except:
    print('Timeout!')
time.sleep(3)
keithley.close()

