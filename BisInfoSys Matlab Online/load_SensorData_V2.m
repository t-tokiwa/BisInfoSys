% 変数や表示している図をクリアする処理
clear all; close all;

% データの読み（計測したファイル名を指定）
load 'sensorlog_20211129_150053.mat'

%Acceleration（加速度)の表示
figure
plot(Acceleration.Timestamp,Acceleration.X, 'r')
hold on;
plot(Acceleration.Timestamp,Acceleration.Y, 'g')
plot(Acceleration.Timestamp,Acceleration.Z, 'b')
ylabel('Acc. X, y, z [m/s^2]')
xlabel('Time [s]')
grid on;
