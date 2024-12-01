% 保存している変数をクリア，表示している図をクリア
clear all; close all;

% データの読み（計測したファイル名を指定）
load 'sensorlog_20211129_150053.mat'

%% Accelerationの図示(一つの図に表示する場合）
figure
plot(Acceleration.Timestamp,Acceleration.X, 'r')
hold on;
plot(Acceleration.Timestamp,Acceleration.Y, 'g')
plot(Acceleration.Timestamp,Acceleration.Z, 'b')
ylabel('Acc. X, y, z [m/s^2]')
xlabel('Time [s]')
grid on;


% %Accelerationの表示
% figure
% subplot(3,1,1)
% plot(Acceleration.Timestamp,Acceleration.X, 'r')
% ylabel('Acc. X [m/s^2]')
% grid on;
% subplot(3,1,2)
% plot(Acceleration.Timestamp,Acceleration.Y, 'g')
% ylabel('Acc. Y [m/s^2]')
% grid on;
% subplot(3,1,3)
% plot(Acceleration.Timestamp,Acceleration.Z, 'b')
% ylabel('Acc. Z [m/s^2]')
% xlabel('Time [s]')
% grid on;
% 
% %AngularVelocityの表示
% figure
% subplot(3,1,1)
% plot(AngularVelocity.Timestamp, AngularVelocity.X, 'r')
% ylabel('AngVel. X [m/s^2]')
% subplot(3,1,2)
% plot(AngularVelocity.Timestamp,AngularVelocity.Y, 'g')
% ylabel('AngVel. Y [m/s^2]')
% subplot(3,1,3)
% plot(AngularVelocity.Timestamp,AngularVelocity.Z, 'b')
% ylabel('AngVel. Z [m/s^2]')
% xlabel('Time [s]')
% 
% %MagneticFieldの表示
% figure
% subplot(3,1,1)
% plot(MagneticField.Timestamp, MagneticField.X, 'r')
% ylabel('Mag. X [m/s^2]')
% subplot(3,1,2)
% plot(MagneticField.Timestamp,MagneticField.Y, 'g')
% ylabel('Mag. Y [m/s^2]')
% subplot(3,1,3)
% plot(MagneticField.Timestamp,MagneticField.Z, 'b')
% ylabel('Mag. Z [m/s^2]')
% xlabel('Time [s]')
% 
% %Orientationの表示
% figure
% subplot(3,1,1)
% plot(Orientation.Timestamp, Orientation.X, 'r')
% ylabel('Orient. X [m/s^2]')
% subplot(3,1,2)
% plot(Orientation.Timestamp, Orientation.Y, 'g')
% ylabel('Orient. Y [m/s^2]')
% subplot(3,1,3)
% plot(Orientation.Timestamp, Orientation.Z, 'b')
% ylabel('Orient. Z [m/s^2]')
% xlabel('Time [s]')
% 
% %% Positionの表示
% figure
% subplot(3,1,1)
% plot(Position.Timestamp, Position.latitude, 'r')
% ylabel('latitude []')
% subplot(3,1,2)
% plot(Position.Timestamp, Position.course, 'g')
% ylabel('course []')
% subplot(3,1,3)
% plot(Position.Timestamp, Position.speed, 'g')
% ylabel('speed [m/s^2]')
% xlabel('Time [s]')