#!/usr/bin/python

import smbus
import math
import time

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)


bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

conditionMode = False
conditionCount = 0

while True:
    time.sleep(0.1)

    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)

    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    if conditionMode == False or conditionCount >= 15:
        print "RAZ"
        x_base = accel_xout
        y_base = accel_yout
        z_base = accel_zout
        conditionMode = True
        conditionCount = 0

    if x_base + 2000 <= accel_xout:
        print "1"
        conditionCount = conditionCount + 1

    elif x_base - 2000 >= accel_xout:
        print "2"
        conditionCount = conditionCount + 1

    elif y_base + 2000 <= accel_yout:
        print "3"
        conditionCount = conditionCount + 1

    elif y_base - 2000 >= accel_yout:
        print "4"
        conditionCount = conditionCount + 1

    elif z_base + 2000 <= accel_zout:
        print "5"
        conditionCount = conditionCount + 1

    elif z_base - 2000 >= accel_zout:
        print "6"
        conditionCount = conditionCount + 1

    time.sleep(0.5)








