#Real-time Sensor Monitor
import network
import socket
import time
import utime
from machine import ADC, Pin
import json
import ntptime #NTP（ネットワーク時刻プロトコル）を利用して正確な時刻を取得

# Wi-Fi settings
SSID =  #YOUR NETWORK NAME
PASSWORD =  #YOUR NETWORK PASSWORD

# Sensor settings
sensor = machine.ADC(4) # sensor is temperature
led = Pin("LED", Pin.OUT)

# Data buffer
data_buffer = []
MAX_BUFFER_SIZE = 60

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('Waiting for connection...')
        time.sleep(1)
    
    if wlan.status() != 3:
        raise RuntimeError('Network connection failed')
    else:
        print('Connected')
        status = wlan.ifconfig()
        print('IP:', status[0])
        
        # NTPサーバーから時刻を取得
        ntptime.settime()
    return wlan

def read_sensor():
    raw = sensor.read_u16()
    voltage = raw * 3.3 / 65535
    temperature = 27 - (voltage - 0.706)/0.001721
    return round(temperature, 2)

def create_web_page():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sensor Monitor</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { 
                font-family: Arial; 
                margin: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .chart-container {
                width: 100%;
                height: 300px;
                position: relative;
                margin-bottom: 20px;
            }
            canvas {
                border: 1px solid #ddd;
                background-color: white;
                border-radius: 4px;
            }
            .value-list {
                height: 200px;
                overflow-y: auto;
                border: 1px solid #ddd;
                padding: 10px;
                margin-top: 20px;
                background-color: white;
                border-radius: 4px;
            }
            .current-value {
                font-size: 24px;
                font-weight: bold;
                color: #2196F3;
                text-align: center;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Raspberry pi pico W</h1>
            <h2>Real-time Sensor Monitor</h2>
            <div class="chart-container">
                <canvas id="chart"></canvas>
            </div>
            <div class="current-value">
                Current Value: <span id="current-value">--</span>
            </div>
            <h3>Last 60 Seconds Data:</h3>
            <div class="value-list" id="value-list"></div>
        </div>

        <script>
            function drawChart(ctx, data) {
                const width = ctx.canvas.width;
                const height = ctx.canvas.height;
                const padding = 40;
                
                ctx.clearRect(0, 0, width, height);
                
                if (data.length < 2) return;
                
                const values = data.map(d => d.value);
                let min = Math.min(...values);
                let max = Math.max(...values);
                const range = max - min;
                min -= range * 0.1;
                max += range * 0.1;
                
                ctx.strokeStyle = '#ddd';
                ctx.fillStyle = '#666';
                ctx.font = '12px Arial';
                ctx.textAlign = 'right';
                
                for (let i = 0; i <= 5; i++) {
                    const y = padding + (height - 2 * padding) * (1 - i / 5);
                    const value = min + (max - min) * (i / 5);
                    
                    ctx.beginPath();
                    ctx.moveTo(padding, y);
                    ctx.lineTo(width - padding, y);
                    ctx.stroke();
                    
                    ctx.fillText(value.toFixed(1) , padding - 5, y + 4);
                }
                
                ctx.beginPath();
                ctx.strokeStyle = '#2196F3';
                ctx.lineWidth = 2;
                
                data.forEach((point, i) => {
                    const x = padding + (width - 2 * padding) * (i / (data.length - 1));
                    const y = padding + (height - 2 * padding) * (1 - (point.value - min) / (max - min));
                    
                    if (i === 0) {
                        ctx.moveTo(x, y);
                    } else {
                        ctx.lineTo(x, y);
                    }
                });
                
                ctx.stroke();
            }

            function updateData() {
                fetch('/data')
                    .then(response => response.json())
                    .then(data => {
                        if (data.length > 0) {
                            document.getElementById('current-value').textContent = 
                                data[data.length-1].value + ' deg. C';
                        }
                        
                        const canvas = document.getElementById('chart');
                        const ctx = canvas.getContext('2d');
                        
                        const container = canvas.parentElement;
                        canvas.width = container.clientWidth;
                        canvas.height = container.clientHeight;
                        
                        drawChart(ctx, data);
                        
                        const list = document.getElementById('value-list');
                        list.innerHTML = data.map(d => 
                            `<div>Time: ${new Date(d.timestamp * 1000).toLocaleTimeString()},  Value: ${d.value } deg. C</div>`
                        ).reverse().join('');
                    });
            }
            
            window.addEventListener('resize', () => {
                const canvas = document.getElementById('chart');
                const container = canvas.parentElement;
                canvas.width = container.clientWidth;
                canvas.height = container.clientHeight;
                updateData();
            });
            
            setInterval(updateData, 1000);
            updateData();
        </script>
    </body>
    </html>
    """
    return html

def handle_request(request):
    if "GET /data" in request:
        response_data = json.dumps(data_buffer)
        return f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nConnection: close\r\n\r\n{response_data}"
    else:
        return f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n{create_web_page()}"

def main():
    try:
        wlan = connect_wifi()
    except Exception as e:
        print('Failed to connect to WiFi:', e)
        return

    try:
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(1)
    except Exception as e:
        print('Failed to create socket:', e)
        return

    last_sample_time = time.time()
    print('Server started')

    while True:
        try:
            current_time = time.time()
            if current_time - last_sample_time >= 1:
                # 現在時刻を取得
                #rtc_time = time.localtime()
                t = utime.localtime()
                rtc_time = str(t[0]) + str(t[1]) + str(t[2]) + str(t[3]) + str(t[4])

                # センサ値の取得
                value = read_sensor()
                data_buffer.append({
                    "timestamp": rtc_time,
                    "value": value
                })
                
                if len(data_buffer) > MAX_BUFFER_SIZE:
                    data_buffer.pop(0)
                
                last_sample_time = current_time
                print(f"Time: {rtc_time}, Temperature: {value} deg. C")

            cl, addr = s.accept()
            request = cl.recv(1024).decode()
            response = handle_request(request)
            cl.send(response.encode())
            cl.close()

        except Exception as e:
            print('Error in main loop:', e)
            time.sleep(1)
            continue
        
        except KeyboardInterrupt:
            print('Stopped by user')
            cl.close()

if __name__ == '__main__':
    try:
        main()
    finally:
        print("Execution finished")
