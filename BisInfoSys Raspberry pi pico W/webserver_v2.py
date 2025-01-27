import time
import network
import socket
import machine
from machine import Pin

# LEDの設定
led = machine.Pin("LED", machine.Pin.OUT)
ledState = 'LED State Unknown'

# 内部温度取得関数
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

def readtemperature():
    reading = sensor_temp.read_u16() * conversion_factor
    temperature = 27 - (reading - 0.706)/0.001721
    return str(temperature)

# Aボタンの状態変数の初期化
val_A = 0
temp = ""

# 起動開始でLED点灯
led.value(1)

# 実験室環境のWi-FiのSSIDとパスワード設定
ssid =  #YOUR NETWORK NAME
password =  #YOUR NETWORK PASSWORD


# ネットワーク接続
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# HTML
html = """<!DOCTYPE html><html lang="ja">
<head>
    <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
    <style>html { font-family: sans-serif; display: inline-block; margin: 0px auto; text-align: center;}
.buttonA { background-color: #ffffff; border: 2px solid #000000;; color: black; padding: 15px 64px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
.buttonB { background-color: #ffffff; border: 2px solid #000000;; color: black; padding: 15px 64px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; }
text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
    </style>
</head>
    <body>
        <center><h1>Raspberry Pi Pico W controller</h1></center><br><br>
        <form><center>
            <center>
                <button class="buttonA" name="job" value="A" type="submit">LED 点灯・消灯</button><br><br>
            <center>
                <button class="buttonB" name="job" value="B" type="submit">温度センサー値取得</button>
        </form>
        <br><br>
        <p>%s<p>
    </body>
</html>
"""

# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)
    
# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )


# Wait for connect or fail
# Handle connection error
# 起動が完了したらLED消灯
led.value(0)

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
#ソケットの再利用を許可する設定
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
s.bind(addr)
s.listen(1)

# Listen for connections, serve client
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print("request:")
        #print(request)
        request = str(request)
        # LEDボタン処理. requestの文字列の中に文字列job=Aが入っている位置
        # 含まれている場合は文字列の位置．含まれていない場合は-1
        led_on = request.find('job=A') 
        temp_on = request.find('job=B')
        
        #print( 'LED = ' + str(led_on))
        #print( 'TEMP = ' + str(temp_on))
        
        if led_on == 8:
            if val_A == 0:
                led.value(1) # LED 点灯
                val_A = 1
            else:
                led.value(0) # LED 消灯
                val_A = 0
            
            print("led on")
            
        if temp_on == 8:
            print("temp on")
            #温度を取得 関数readtemperature()の呼び出し
            temp = readtemperature()
        
        ledState = "LED OFF:" if led.value() == 0 else "LED ON:" # a compact if-else statement    
        
        # web上へ出力する値（LEDの状態と温度）
        stateis = ledState + " : " + temp + "℃"
        response = html % stateis
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
        
    except OSError as e:
        cl.close()
        led.off()
        print('connection closed')
        
    except KeyboardInterrupt:
        cl.close()
        led.off()
        print('Program interrupted by user')
        break

cl.close()  # ソケットを閉じる
