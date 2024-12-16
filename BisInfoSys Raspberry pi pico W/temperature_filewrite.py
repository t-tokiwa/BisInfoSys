from machine import Pin
import utime

file = open('out_temps.txt', 'w')

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)
t = 0

for i in range(10):
    #read_u16関数で16ビットのADCの値を読み込み
    #センサから取得した値(0-65536)を電圧に換算
    reading = sensor_temp.read_u16() * conversion_factor
    # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC ch.
    # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree. 
    temperature = 27 - (reading - 0.706)/0.001721
    print(f' time: {i}, temperature: {temperature}')
    file.write(str(i) + ' , ' + str(temperature) +'\n')
    #計測間隔を1 sに指定する
    utime.sleep(1)

file.close()
