import smbus
import time
bus = smbus.SMBus(1)
while(True):
    time.sleep(0.5)
    bus.write_byte_data(0x5C, 0x20, 0x90)
    data = bus.read_i2c_block_data(0x5C, 0x28 | 0x80, 3)
    pressure = (data[2] * 65536 + data[1] * 256 + data[0])*0.750064 / 4096.0 #1 гектопаскаль = 0.750064 миллиметра ртутного столба
    if pressure<747:
        print("Атмосферное давение: ", pressure, "mm Hg - ниже нормы")
    if 747<=pressure<=749:
        print("Атмосферное давение: ", pressure, "mm Hg - норма")
    if pressure>749:
        print("Атмосферное давение: ", pressure, "mm Hg - выше нормы")
    time.sleep(0.5)