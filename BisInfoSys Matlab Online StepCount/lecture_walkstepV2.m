% 2022/12/5 歩数，歩行スピード，歩行軌道を描く
% 変数の値のクリア，図を一度すべて落とす
clear all; close all;

%３つの結果を１つの図に重ねて表示する場合
%保存したファイル名を指定
load 'sensorlog_20221205_184301walk2.mat'

%% Accelerationの表示
figure
plot(Acceleration.Timestamp,Acceleration.X, 'r')
hold on;
plot(Acceleration.Timestamp,Acceleration.Y, 'g')
plot(Acceleration.Timestamp,Acceleration.Z, 'b')
ylabel('Acc. X, y, z [m/s^2]')
xlabel('Time [s]')
legend('x','y','z')
grid on;

% ピーク検出 locs_peakにピーク時のインデックスが代入される
[peak,locs] = findpeaks(Acceleration.Z,'MinPeakHeight',12,'MinPeakDistance',2);           


%% ピーク検出結果図の表示
figure
plot(Acceleration.Timestamp,Acceleration.Z, 'b')
hold on; %図を上書きする
plot(Acceleration.Timestamp(locs), Acceleration.Z(locs),'rv','MarkerFaceColor','r');
grid on;

%% ピーク数のカウント
num =size(locs, 1); %歩数結果の表示 size関数を使用して変数の要素数を調べる．
X = ['歩数',num2str(num),'[歩]'];
disp(X)

%% 歩行速度の表示
figure
plot(Position.Timestamp,Position.speed, 'k')
hold on;
ylabel('speed [m/s]')
xlabel('Time [s]')
legend('speed')
grid on;

%%
v_max  = max(Position.speed); %最高速度
v_mean = mean(Position.speed); %平均値

X = ['最高速度 ',num2str(v_max),'[m/s]，平均速度', num2str(v_mean),'[m/s]'];
disp(X)

%%
% plot(Acceleration.Timestamp,Acceleration.Y, 'g')
% plot(Acceleration.Timestamp,Acceleration.Z, 'b')
% ylabel('Acc. X, y, z [m/s^2]')
% xlabel('Time [s]')
% legend('x','y','z')
% grid on;

%% 移動起動
% figure
% plot(Position.latitude, Position.longitude, 'k')
% hold on;
% % xlim([34 35])
% % ylim([132 133])
% ylabel('緯度')
% xlabel('経度')
% %legend('speed')
% grid on;
