import smbus
import time
bus = smbus.SMBus(1)
bus.write_byte_data(0x5C, 0x20, 0x90)
data = bus.read_i2c_block_data(0x5C, 0x28 | 0x80, 3)
pressure = (data[2] * 65536 + data[1] * 256 + data[0]) / 4096.0
while(True):
    time.sleep(0.5)
    print ("Barometric Pressure is : %.2f hPa" %pressure) # гектопаскаль
    time.sleep(0.5)