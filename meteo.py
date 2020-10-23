import gpioexp
import time
import smbus
bus = smbus.SMBus(1)
exp = gpioexp.gpioexp()

bus.write_byte_data(0x5C, 0x20, 0x90)
data = bus.read_i2c_block_data(0x5C, 0x28 | 0x80, 3)
pressure = (data[2] * 65536 + data[1] * 256 + data[0])*0.750064 / 4096.0 #1 гектопаскаль = 0.750064 миллиметра ртутного столба

def light_read(pin):
    RES_DIVIDER = 10000
    MULT_VALUE = 32017200
    POW_VALUE = 1.5832
    SAMPLE_TIMES = 32
    ADC_VALUE_MAX = 1024
    sensorADC = 0
    sensorRatio = 0
    sensorResistance = 0
    for i in range(SAMPLE_TIMES):
        sensorADC += exp.analogRead(pin)
        i += 1
    sensorRatio = ADC_VALUE_MAX / (sensorADC - 1)
    sensorResistance = RES_DIVIDER / sensorRatio
    _sensorLight = int((MULT_VALUE / pow(sensorResistance, POW_VALUE)) / 230)
    return(_sensorLight)

while (True):
    time.sleep(0.5)
    light = light_read(0)-34
    if light<300:
        print("Освещённость: ", light, "lm - ниже нормы")
    if 300<=light<=600:
        print("Освещённость: ", light, "lm - норма")
    if light>600:
        print("Освещённость: ", light, "lm - выше нормы")
    if pressure<747:
        print("Атмосферное давение: ", pressure, "mm Hg - ниже нормы")
    if 747<=pressure<=749:
        print("Атмосферное давение: ", pressure, "mm Hg - норма")
    if pressure>749:
        print("Атмосферное давение : ", pressure, "mm Hg - выше нормы")
    time.sleep(0.5)