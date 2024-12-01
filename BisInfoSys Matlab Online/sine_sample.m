% sin wave
t = 0:0.01:10; %start:0, dt=0.01, end:10
T = 5;
y = sin(2*pi*t/T);

%figure
figure
plot(t, y);
grid on;
% label of figure
xlabel('x data') % x label
ylabel('y data') % y label