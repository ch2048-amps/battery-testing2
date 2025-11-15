import subprocess
import os

valid1 = False
valid2 = False
valid3 = False

totalT = 0
Ton_Toff = 0
sampleT = 0

# run the other files
try:
    
    while (not valid1 or (int(totalT) <= 0)):
        print('Minutes to run test for (int): ')
        totalT = input().strip()
        valid1 = totalT.isnumeric()

        if(not valid1 or (int(totalT) <= 0)):
            print('Enter a valid integer')

        print("\n")
    
    while (not valid2 or (int(Ton_Toff) <= 0)):
        print('Minutes for Ton and Toff (int): ')
        Ton_Toff = input().strip()
        valid2 = totalT.isnumeric()

        if(not valid1 or (int(Ton_Toff) <= 0)):
            print('Enter a valid integer')

        print("\n")

    while(not valid3 or (int(sampleT) <= 0)):
        print('Seconds between samples (int): ')
        sampleT = input().strip()
        valid3 = sampleT.isnumeric()

        if(not valid2 or (int(sampleT) <= 0)):
            print('Enter a valid integer')

        print("\n")

    print("arguments: ")
    print(f"totalT: ", totalT)
    print(f"Ton_Toff: ", Ton_Toff)
    print(f"sampleT: ", sampleT)

    totalT = str(int(totalT)*60)
    Ton_Toff = str(int(Ton_Toff)*60)
    sampleT = str(int(sampleT))

    if(valid1 and valid2):
        subprocess.Popen(["python", "keithleyPS.py", totalT, Ton_Toff])

        subprocess.Popen(["python", "keithleyEL.py", totalT, sampleT])

        subprocess.Popen(["python", "agilentMM.py", totalT, sampleT])

except subprocess.CallProcessError as e:
    print(f"Command failed with return code {e.returncode}")

except KeyboardInterrupt:
    print("keyboard interrupt detected")