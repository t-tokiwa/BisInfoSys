#The on-board LED on Raspberry Pi Pico W
from machine import Pin
import utime

led = Pin('LED', Pin.OUT)
t_d = 1 #点滅時間の設定

for i in range(3):
    led.on() # LED on
    # t_ d [s] holding 
    utime.sleep(t_d) # hold time[s]

    led.off() # LED off
    utime.sleep(t_d) # hold time[s]