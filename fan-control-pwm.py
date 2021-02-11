# this is an example of pwm originally for an led
# I tested this with a fan and it works
# but sounds a little funny.  I did it at the cli

import RPi.GPIO as GPIO
from time import sleep

fanpin = 13				# PWM pin connected to the fan
GPIO.setwarnings(False)			# disable warnings
# GPIO.setmode(GPIO.BOARD)		# set pin numbering system
GPIO.setup(fanpin,GPIO.OUT)
pi_pwm = GPIO.PWM(fanpin,1000)		#create PWM instance with frequency
pi_pwm.start(0)				#start PWM of required Duty Cycle 
while True:
    for duty in range(0,101,1):
        pi_pwm.ChangeDutyCycle(duty) #provide duty cycle in the range 0-100
        sleep(0.01)
    sleep(0.5)
    
    for duty in range(100,-1,-1):
        pi_pwm.ChangeDutyCycle(duty)
        sleep(0.01)
    sleep(0.5)
