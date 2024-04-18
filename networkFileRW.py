#!/usr/bin/env python3
#Lab8.Output.py
#Austin Cramer
#April 3rd, 2024
#Update routers and switches;
#read equipment from a file, write updates & errors to file

import json

#Constants for file names
EQUIP_R_FILE = "equip_r.txt"
EQUIP_S_FILE = "equip_s.txt"
UPDATED_FILE = "updated.txt"
INVALID_FILE = "invalid.txt"

#Prompt constants
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"

#Getting valid device
def getValidDevice(routers, switches):
    validDevice = False
    while not validDevice:
        device = input(UPDATE + QUIT).lower()
        if device in routers.keys() or device in switches.keys() or device == 'x':
            return device
        else:
            print("That device is not in the network inventory.")

#Getting valid IP address
def getValidIP(invalidIPCount, invalidIPAddresses):
    validIP = False
    while not validIP:
        ipAddress = input(NEW_IP)
        octets = ipAddress.split('.')
        for byte in octets:
            byte = int(byte)
            if byte < 0 or byte > 255:
                invalidIPCount += 1
                invalidIPAddresses.append(ipAddress)
                print(SORRY)
                break
        else:
            return ipAddress, invalidIPCount

def main():
    try:
        
        with open(EQUIP_R_FILE, 'r') as f:
            routers = json.load(f)

        with open(EQUIP_S_FILE, 'r') as f:
            switches = json.load(f)

    except ImportError:
        print("Error: JSON module not found.")
        return
    except FileNotFoundError:
        print("Error: File not found.")
        return

    
    updated = {}
    invalidIPAddresses = []
    devicesUpdatedCount = 0
    invalidIPCount = 0
    quitNow = False

    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")
    for router, ipa in routers.items(): 
        print("\t" + router + "\t\t" + ipa)
    for switch, ipa in switches.items():
        print("\t" + switch + "\t\t" + ipa)

    while not quitNow:
        device = getValidDevice(routers, switches)

        if device == 'x':
            quitNow = True
            break

        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)

        if 'r' in device:
            routers[device] = ipAddress 
        else:
            switches[device] = ipAddress

        devicesUpdatedCount += 1
        updated[device] = ipAddress
        print(device, "was updated; the new IP address is", ipAddress)

    print("\nSummary:")
    print("Number of devices updated:", devicesUpdatedCount)

    #Write updated dictionary to a new file
    with open(UPDATED_FILE, 'w') as f:
        json.dump(updated, f, indent=4)

    print("\nNumber of invalid addresses attempted:", invalidIPCount)

    #Write invalid addresses to a new file
    with open(INVALID_FILE, 'w') as f:
        for address in invalidIPAddresses:
            f.write(address + '\n')

if __name__ == "__main__":
    main()





