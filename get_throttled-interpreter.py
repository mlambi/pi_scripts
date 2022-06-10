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

# setting this up backward
# popping from the list will start with the last item
message_list = [
        'under-voltage',
        'currently throttled',
        'arm frequency capped',
        'soft temperature reached',
        'no message',
        'no message',
        'no message',
        'no message',
        'no message',
        'no message',
        'no message',
        'no message',
        'no message',
        'no message',
        'no message',
        'no message',
        'no message',
        'under-voltage has occurred since last reboot',
        'throttling has occurred since last reboot',
        'arm frequency capped ahs occurred since last reboot',
        'soft temperature reached since last reboot'
        ]

for i in range(len(message_list)):
    print(message_list[i])

# get the status from 'vcgencmd get_throttled'
output = subprocess.check_output(['vcgencmd','get_throttled'])
# output has a \n and is in binary, and has extra
# b'throttled=0x0'\n
hexval =(output.decode('UTF-8').split("=")[1].strip())
# enter a custom hex value below for testing or comment out
hexval = '0x8000'
print(hexval)
# convert it to binary
intval = (bin(int(hexval,16))[2:].zfill(16))
print(intval)

# next we assign the binary value to a list
int_list = list(intval)
print(int_list)

return_message = []


for i in range(len(message_list)):
    # print(int_list.pop()) # don't do this is will pop a value off the list
    popVal = int(int_list.pop())
    print(f'popVal is : {popVal} and type is {type(popVal)}')
    if popVal == 1:
        # print(f'index is {i} and the return message is: {return_message[i]}')
        print(f'index is {i}')
        print(message_list[i])
        # return_message.append(message_list[i])
    else:
        print(f'no message returned from: {popVal}')


print(return_message)
