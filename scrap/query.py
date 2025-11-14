import pyvisa

try:
    rm = pyvisa.ResourceManager(r'C:\WINDOWS\system32\visa64.dll')
    print("Resource Manager: ")
    print(rm)
    print("\nList all resources: ")
    print(rm.list_resources())
    print()

except:
    print("error")