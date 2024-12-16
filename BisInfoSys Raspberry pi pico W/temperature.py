from machine import Pin
import utime

#温度センサーはADCの4チャネルに接続されているので、引数として’4’を指定
sensor_temp = machine.ADC(4)
#ADCは16bitの値で返ってきます。つまり、2の16乗=65536で、0から始まるので電圧3.3Vを65535で割ります
#１目盛り辺りの電圧（換算係数）を計算
conversion_factor = 3.3 / (65535)

while True:
    #read_u16関数で16ビットのADCの値を読み込み
    #センサから取得した値(0-65536)を電圧に換算
    reading = sensor_temp.read_u16() * conversion_factor
    
    # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC ch.
    # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree. 
    temperature = 27 - (reading - 0.706)/0.001721
    print(temperature)
    #計測間隔を1 sに指定する
    utime.sleep(1)
