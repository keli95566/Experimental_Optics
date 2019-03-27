close all;
clear all;

I = imread('223_more_exposure_polarizer.png');
imshow(I)
%G = rgb2gray(I);
x = [0, 1024]; y = [521,521];
xline = [x(1), x(2)]; yline = [y(1),y(2)];
ylabel('intensity');title('Haidinger Rings With Polarizer, degree 223')
improfile(I, xline, yline);
