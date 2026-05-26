from machine import ADC
import time

sensor_temp = ADC(4)
conversion_factor = 3.3 / 65535

while True:
    reading = sensor_temp.read_u16()
    voltage = reading * conversion_factor
    temperature = 27 - (voltage - 0.706) / 0.001721

    #シリアル通信でデータを送る場合print()関数を利用します
    print(temperature)
    time.sleep(0.2)