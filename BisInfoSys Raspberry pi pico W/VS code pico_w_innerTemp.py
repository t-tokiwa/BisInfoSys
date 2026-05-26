import serial
import matplotlib
#matplotlibでグラフを表示するための仕組み（バックエンド）を指定
#GUIライブラリTkのウィンドウ上にmatplotlibグラフを描く」
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
from collections import deque
import random
import time
import numpy as np

#シリアル通信のポート設定
PORT = "COM4"      # 自分のPicoのCOM番号に変更
BAUDRATE = 115200

ser = serial.Serial(PORT, BAUDRATE, timeout=1)

time_data = deque(maxlen=100)
raw_data = deque(maxlen=100)
noise_data = deque(maxlen=100)
smooth_data = deque(maxlen=100)

#移動平均の点数
# 値を大きくする：滑らかになるが変化が遅れる
# 値を小さくする：滑らかさは減るが反応が早い

window_size = 10

#plotのインタラクティブモード
plt.ion()

fig, ax = plt.subplots()

line_raw, = ax.plot([], [], label="Raw temperature")
#line_noise, = ax.plot([], [], label="Temperature + random noise")
line_smooth, = ax.plot([], [], label="Smoothed data")

ax.set_xlabel("Time (s)")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Real-time Temperature Data from Raspberry Pi Pico")
ax.legend()
ax.grid(True)

plt.show()

start_time = time.time()

try:
    while True:
        line = ser.readline().decode().strip()

        if line:
            temp = float(line)

            #noise = random.uniform(-0.5, 0.5)
            #temp_noise = temp + noise
            temp_noise = temp

            t = time.time() - start_time

            time_data.append(t)
            raw_data.append(temp)
            #noise_data.append(temp_noise)

            if len(raw_data) >= window_size:
                smooth_value = np.mean(list(raw_data)[-window_size:])
            else:
                smooth_value = temp_noise

            smooth_data.append(smooth_value)

            line_raw.set_data(time_data, raw_data)
            #line_noise.set_data(time_data, noise_data)
            line_smooth.set_data(time_data, smooth_data)

            ax.relim()
            ax.autoscale_view()

            #計測間隔．数字を大きくすると計測間隔が長くなる
            plt.pause(0.05)

except KeyboardInterrupt:
    print("終了します")

except Exception as e:
    print("Error:", e)

finally:
    ser.close()