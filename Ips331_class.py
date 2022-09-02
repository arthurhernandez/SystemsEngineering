
#!/usr/bin/env python3

import smbus
import sys
import numpy
import time

class lps331:
    ''' allows connection from Raspberry pi to I2C connected lps331 '''

    def __init__(self,raspberry_pi_i2c_port=1):
        self.i2c_port_number = raspberry_pi_i2c_port
        self.bus = smbus.SMBus(self.i2c_port_number)
        self.address = self.find_sensor()
        if (self.address == 0):
            print("Error: could not read from sensor at i2c address 0x5d")
            sys.exit()
        self.enable_sensor()
        
    def find_sensor(self):
        ''' read the whoami byte from i2c address 0x5d and confirm to be 0xbb '''
        # Return the address if found (0x5d) and 0 if not found
        
        # @@@@ Your Code Here @@@@ 
        data = self.bus.read_byte_data(0x5d,0x0f)
        if (data == 0xbb):
            return(0x5d);
        else:
            return(0);
            return(-1);   # if the sensor was not located on either bus, return -1

    def i2c_address(self):
        return(self.address)

    def sample_once(self):
        ''' Cause the sensor to sample one time '''
        # @@@@ Your Code Here @@@@
        #ctrl_reg2 = self.bus.read_byte_data(0x5d,0x21)
        self.bus.write_byte_data(self.address,0x21,0x01)
        time.sleep(.1)
        #ctrl_reg2 = self.bus.read_byte_data(0x5d,0x21)
        return
        
    def read_temperature(self):
        ''' Sample, read temperature registers, and convert to inhg ''' 
        tempC = 0
	# @@@@ Your Code Here @@@@
        self.sample_once()
        temp_l = self.bus.read_byte_data(self.address,0x2b)
        temp_h = self.bus.read_byte_data(self.address,0x2c)
        hex = (temp_h<<8) | temp_l
        hex = numpy.int16(hex)
        tempC = 42.5 + hex / 480
        return(tempC)

    def read_pressure(self):
        ''' Sample, read pressure registers, and convert to inhg ''' 
        press_inhg = 0
        
        # @@@@ Your Code Here @@@@ 
        self.sample_once()
        press_xl = self.bus.read_byte_data(self.address,0x28)
        press_l = self.bus.read_byte_data(self.address,0x29)
        press_h= self.bus.read_byte_data(self.address,0x2a)
        press = (press_h<<16) | (press_l<<8) | press_xl
        press = numpy.int32(press)
        press_inhg = (press/4096) / 33.864

        return(press_inhg)

    def enable_sensor(self):
        ''' Turn on sensor in control register 1'''

        # @@@@ Your Code Here @@@@ 
        ctrl_reg1 = self.bus.read_byte_data(self.address,0x20)
        self.bus.write_byte_data(self.address,0x20,0x80)
        return

    def disable_sensor(self):
        ''' Turn off sensor in control register 1 '''
        # @@@@ Your Code Here @@@@
        self.bus.write_byte_data(self.address,0x20,0x0)
        return
    def close(self):
        ''' Disable the sensor and close connection to i2c port '''
        self.disable_sensor()
        self.bus.close()
       
if  __name__ == "__main__":
    sensor = lps331(1)
    print("Temperature = %0.2f Deg C "%(sensor.read_temperature()))
    print("Pressure = %0.2f inHg"%(sensor.read_pressure()))
    sensor.close()

