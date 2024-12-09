% 2022/12/5 歩数をカウントするためのプログラム例
% 変数の値のクリア，図を一度すべて落とす
clear all; close all;

%保存したファイル名を指定
load 'sensorlog_20221205_141613.mat'

x = Acceleration.X;
y = Acceleration.Y;
z = Acceleration.Z;

%各時点における XYZ 加速度ベクトルをスカラー値に変換
%デバイスの向きにかかわらず、歩行中に要した歩数など、加速度全体における大きな変化を検出できます。
mag = sqrt(sum(x.^2 + y.^2 + z.^2, 2));
%加速度の大きさの平均がゼロでないことを示しています。データから平均値を減算すると、重力のような一定の影響が除去されます。
magNoG = mag - mean(mag);

%Accelerationの表示
figure
plot(Acceleration.Timestamp, magNoG);
xlabel('Time (s)');
ylabel('Acceleration (m/s^2)');
grid on; 

minPeakHeight = std(magNoG);
%ピーク検出
[pks,locs] = findpeaks(magNoG,'MINPEAKHEIGHT',minPeakHeight);

%% ピーク検出結果図の表示
%figure
hold on; %上の図に上書きする
plot(Acceleration.Timestamp(locs), magNoG(locs),'rv','MarkerFaceColor','r');

%% ピーク数のカウント
num =size(locs, 1); %歩数結果の表示 size関数を使用して変数の要素数を調べる．
% 第2引数は,行数もしくは列数を指定する 1は行数，２は列数
% 文字列を定義してその文字列を結果として表示する
X = ['歩数',num2str(num),'[歩]'];
disp(X)