#!/usr/bin/python
"""
This script will read the output from 'vcgencmd get_throttled'
and interpret it. The command return a hex value that represents
a binary value that is positional didactic.
Here is a chart:

111100000000000001010
||||             ||||_ under-voltage
||||             |||_ currently throttled
||||             ||_ arm frequency capped
||||             |_ soft temperature reached
||||_ under-voltage has occurred since last reboot
|||_ throttling has occurred since last reboot
||_ arm frequency capped has occurred since last reboot
|_ soft temperature reached since last reboot
"""
import subprocess
import argparse

# started adding argparse, but bailed
# DEFAULT_HEX_VALUE = hexval

# get the status from 'vcgencmd get_throttled'
output = subprocess.check_output(['vcgencmd','get_throttled'])
# output has a \n and is in binary, and has extra
# b'throttled=0x0'\n
hexval =(output.decode('UTF-8').split("=")[1].strip())
print(hexval)
# convert it to binary
intval = (bin(int(hexval,16))[2:].zfill(16))
print(intval)

# trying to do something static here, since I am working
# on a clean system.
hex_val = '0x8'

val_list = list(bin(int(hex_val,16))[2:].zfill(16))
print(f'val_list is: {val_list}')

'''
def main():
    # do this later, for now hard-code some hex vars
    parser = argparse.ArguementParser(
            description="Input test values")
    parser.add_argument(
            "--broker",
            default=DEFAULT_HEX_VALUE,
            type=str
# we can 
'''
int_list = list(intval)

print(int_list)
for i in range(16):
    # print(int_list.pop())
    try:
        if int_list.pop() == 1:
            print(f'index is {i}')
    except IndexError:
        pass



