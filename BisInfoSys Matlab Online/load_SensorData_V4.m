clear all; close all;
load 'sensorlog_20211129_150053.mat'

%Accelerationの表示
figure
plot(Acceleration.Timestamp,Acceleration.X, 'r')
hold on;
plot(Acceleration.Timestamp,Acceleration.Y, 'g')
plot(Acceleration.Timestamp,Acceleration.Z, 'b')
ylabel('Acc. x, y, z [m/s^2]')
xlabel('Time')
grid on;

%AngularVelocityの表示
figure
plot(AngularVelocity.Timestamp, AngularVelocity.X, 'r')
hold on;
plot(AngularVelocity.Timestamp,AngularVelocity.Y, 'g')
plot(AngularVelocity.Timestamp,AngularVelocity.Z, 'b')
ylabel('AngVel. x, y, z[rad/s]')
xlabel('Time')
grid on;

%MagneticFieldの表示
figure
plot(MagneticField.Timestamp, MagneticField.X, 'r')
hold on;
plot(MagneticField.Timestamp,MagneticField.Y, 'g')
plot(MagneticField.Timestamp,MagneticField.Z, 'b')
ylabel('Mag. x, y, z [uT]')
xlabel('Time')
grid on;

%Orientationの表示
figure
plot(Orientation.Timestamp, Orientation.X, 'r')
hold on;
plot(Orientation.Timestamp, Orientation.Y, 'g')
plot(Orientation.Timestamp, Orientation.Z, 'b')
ylabel('Orient. [°]')
xlabel('Time')
grid on;

%% Positionの表示
figure
plot(Position.Timestamp, Position.latitude, 'r')
hold on;
plot(Position.Timestamp, Position.course, 'g')
plot(Position.Timestamp, Position.speed, 'g')
ylabel('position [°]')
xlabel('Time')
grid on;