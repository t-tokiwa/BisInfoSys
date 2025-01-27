import time
import network
import socket
import machine

# 実験室環境のWi-FiのSSIDとパスワード設定
ssid =  #YOUR NETWORK NAME
password =  #YOUR NETWORK PASSWORD


# ネットワーク接続
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# HTML
html = """<!DOCTYPE html>
<html>
    <head> <title>Pico W</title> </head>
    <body> <h1>Pico W</h1><br>
            <h3>Connection confirmed<h3><br>
            <h3>Hiroshima City University</h3>
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

#---------------------------------------------
# Open socket
# ポート 80 はデフォルトで HTTP サーバー用
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
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(html)
        cl.close()
        
    except OSError as e:
        cl.close()
        print('connection closed')
        
    except KeyboardInterrupt:
        cl.close()
        print('Program interrupted by user')
        break

cl.close()