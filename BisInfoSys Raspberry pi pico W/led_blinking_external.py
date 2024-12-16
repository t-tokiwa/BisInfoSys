from machine import Pin
import utime

led = Pin(0, Pin.OUT)
t_d = 1

for i in range (3):
    # LED on 
    led.value(1)
    # t_d [s] holding
    utime.sleep(t_d)
        
    # LED off 
    led.value(0)
    # t_d [s] holding
    utime.sleep(t_d)
    