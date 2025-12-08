% 3軸加速度情報から速度情報を算出するプログラム

% MATファイルを読み込む
% データの読み（計測したファイル名を指定）
load 'sensorlog_20211129_150053.mat'

% 変数名を取得
% varNames = fieldnames(data);
% disp('利用可能な変数:');
% disp(varNames);

% タイムスタンプと加速度データを取得
% ※必要に応じて変数名を変更してください
timestamp_raw = Acceleration.Timestamp;  
acc_x = Acceleration.X;      % X軸加速度
acc_y = Acceleration.Y;      % Y軸加速度
acc_z = Acceleration.Z;      % Z軸加速度

% タイムスタンプをdouble型に変換（duration型の場合は秒に変換）
if isduration(timestamp_raw)
    timestamp = seconds(timestamp_raw);
    fprintf('タイムスタンプをduration型から秒に変換しました\n');
%else
%    timestamp = double(timestamp_raw);
end

% ベクトルに変換
timestamp = timestamp(:);
acc_x = acc_x(:);
acc_y = acc_y(:);
acc_z = acc_z(:);

% データ長を確認
N = length(timestamp);
fprintf('データ点数: %d\n', N);

% 重力加速度の除去（静止時の平均値をオフセットとして除去）
% 最初の100点の平均を初期オフセットとして使用
offset_samples = min(100, N);
acc_x_offset = mean(acc_x(1:offset_samples));
acc_y_offset = mean(acc_y(1:offset_samples));
acc_z_offset = mean(acc_z(1:offset_samples)) - 9.81;  % Z軸は重力分を考慮

acc_x_corrected = acc_x - acc_x_offset;
acc_y_corrected = acc_y - acc_y_offset;
acc_z_corrected = acc_z - acc_z_offset;

% 速度の算出（台形積分法）
vel_x = zeros(N, 1);
vel_y = zeros(N, 1);
vel_z = zeros(N, 1);

for i = 2:N
    dt = timestamp(i) - timestamp(i-1);
    % dtがduration型の場合は秒に変換
    if isduration(dt)
        dt = seconds(dt);
    end
    vel_x(i) = vel_x(i-1) + (acc_x_corrected(i) + acc_x_corrected(i-1)) * dt / 2;
    vel_y(i) = vel_y(i-1) + (acc_y_corrected(i) + acc_y_corrected(i-1)) * dt / 2;
    vel_z(i) = vel_z(i-1) + (acc_z_corrected(i) + acc_z_corrected(i-1)) * dt / 2;
end

% 合成速度の算出
vel_magnitude = sqrt(vel_x.^2 + vel_y.^2 + vel_z.^2);

% 結果を表示
fprintf('\n===== 速度算出結果 =====\n');
fprintf('最大速度 (X軸): %.3f m/s\n', max(abs(vel_x)));
fprintf('最大速度 (Y軸): %.3f m/s\n', max(abs(vel_y)));
fprintf('最大速度 (Z軸): %.3f m/s\n', max(abs(vel_z)));
fprintf('最大合成速度: %.3f m/s\n', max(vel_magnitude));

% 結果をプロット
figure('Position', [100, 100, 1200, 800]);

% 加速度のプロット
subplot(2, 2, 1);
plot(timestamp, acc_x_corrected, 'r', 'LineWidth', 1.2); hold on;
plot(timestamp, acc_y_corrected, 'g', 'LineWidth', 1.2);
plot(timestamp, acc_z_corrected, 'b', 'LineWidth', 1.2);
grid on;
xlabel('時間 [秒]');
ylabel('加速度 [m/s²]');
title('3軸加速度（補正後）');
legend('X軸', 'Y軸', 'Z軸');

% 速度のプロット
subplot(2, 2, 2);
plot(timestamp, vel_x, 'r', 'LineWidth', 1.2); hold on;
plot(timestamp, vel_y, 'g', 'LineWidth', 1.2);
plot(timestamp, vel_z, 'b', 'LineWidth', 1.2);
grid on;
xlabel('時間 [秒]');
ylabel('速度 [m/s]');
title('3軸速度');
legend('X軸', 'Y軸', 'Z軸');

% 合成速度のプロット
subplot(2, 2, 3);
plot(timestamp, vel_magnitude, 'k', 'LineWidth', 1.5);
grid on;
xlabel('時間 [秒]');
ylabel('速度 [m/s]');
title('合成速度');

% 速度の軌跡（XY平面）
subplot(2, 2, 4);
plot(vel_x, vel_y, 'b.-', 'LineWidth', 1.2);
grid on;
xlabel('X軸速度 [m/s]');
ylabel('Y軸速度 [m/s]');
title('速度ベクトルの軌跡（XY平面）');
axis equal;

% 結果を保存
save('velocity_data.mat', 'timestamp', 'vel_x', 'vel_y', 'vel_z', 'vel_magnitude');
fprintf('\n速度データを velocity_data.mat に保存しました\n');