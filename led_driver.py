#!/usr/bin/env python3

import RPi.GPIO as GPIO

class Led_Driver:
    def __init__(self, pin, frequency=100):
        self.pin = pin
        self.frequency = frequency
        self.duty = 0
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin,GPIO.OUT)
        self.pwm_out = GPIO.PWM(self.pin,self.frequency)
        self.pwm_out.start(0)
	  
    def on(self, duty=100):
        self.pwm_out.ChangeDutyCycle(duty)
        self.duty = duty

    def off(self):
        self.pwm_out.ChangeDutyCycle(0)
        self.duty = 0
		
    def change_frequency(self, frequency):
        self.pwm_out.ChangeFrequency(frequency)
        self.frequency = frequency 

    def __str__(self):
        outstr = f"Pin = {self.pin}\n"
        outstr += f"Frequency = {self.frequency}\n"
        outstr += f"Duty = {self.duty}\n"
        return outstr


if __name__ == '__main__':
    bcm_pin = 18
    freq = 100
    led = Led_Driver(bcm_pin, freq)
    input("Initialized, Hit a Key for 100% Duty Cycle: ")
    led.on(100)
    print(led)
    input("Hit a Key for 75% Duty Cycle: ")
    led.on(75)
    print(led)
    input("Hit a Key for 50% Duty Cycle: ")
    led.on(50)
    print(led)
    input("Hit a Key to change Frequency to 5 Hz with 50% duty cycle: ")
    led.change_frequency(5)
    print(led)
    input("Hit a Key to change back to 100 Hz with 50% duty cycle: ")
    led.change_frequency(100)
    print(led)
    input("Hit a Key for 25% Duty Cycle: ")
    led.on(25)
    print(led)
    input("Hit a Key for 0% Duty Cycle: ")
    led.off()
    print(led)
    input("Hit a Key to exit ")

