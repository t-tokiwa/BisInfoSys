% 変数や表示している図をクリアする処理
clear all; close all;

% データの読み（計測したファイル名を指定）
load 'sensorlog_20211129_150053.mat'

%Acceleration（加速度)の表示
figure
subplot(3,1,1)
plot(Acceleration.Timestamp,Acceleration.X, 'r')
ylabel('Acc. x [m/s^2]')
grid on;

subplot(3,1,2)
plot(Acceleration.Timestamp,Acceleration.Y, 'g')
ylabel('Acc. y [m/s^2]')
grid on;

subplot(3,1,3)
plot(Acceleration.Timestamp,Acceleration.Z, 'b')
ylabel('Acc. z [m/s^2]')
xlabel('Time [s]')
grid on;
