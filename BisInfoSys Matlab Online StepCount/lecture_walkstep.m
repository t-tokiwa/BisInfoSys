% 2022/12/5 歩数をカウントするためのプログラム例
% 変数の値のクリア，図を一度すべて落とす
clear all; close all;

%保存したファイル名を指定
load 'sensorlog_20221205_141613.mat'

%Accelerationの表示
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
[peak,locs] = findpeaks(Acceleration.Z,'MinPeakHeight',20,'MinPeakDistance',10);           

%% ピーク検出結果図の表示
figure
plot(Acceleration.Timestamp,Acceleration.Z, 'b')
hold on; %図を上書きする
plot(Acceleration.Timestamp(locs), Acceleration.Z(locs),'rv','MarkerFaceColor','r');

%% ピーク数のカウント
num =size(locs, 1); %歩数結果の表示 size関数を使用して変数の要素数を調べる．
% 第2引数は,行数もしくは列数を指定する 1は行数，２は列数
% 文字列を定義してその文字列を結果として表示する
X = ['歩数',num2str(num),'[歩]'];
disp(X)