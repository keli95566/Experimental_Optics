close all
clear all

%M^2 Measurement
%---------------------------------------------

path_o=('G14');

%Calibration for basic offset
%bild_calibration = double(imread([path_o '\calibration\00.jpg'])); %add file-path
%if you have no calibration file use the line below
bild_calibration = zeros(1024,1280);

liste=dir('./4.3.2019 G14');
files={liste(~[liste.isdir]).name};
h=length(files);
number_pictures = 35;
radius_x = zeros(1,number_pictures);
radius_y = zeros(1,number_pictures);
disp(h);
disp(files{1});

for a=1:number_pictures
disp(num2str(a));
fileName = strcat('./4.3.2019 G14/',files{a});
bild = double(imread(fileName));
bild = bild - bild_calibration;

%Gray value offset
bild_offset = bild(1:100,end-99:end);
offset = sum(sum(bild_offset))/(10000);

%substract offset -> set background to zero
bild = bild - (offset+5);
bild_mod = bild >= 0;
bild = bild.*bild_mod;

%Number of rows(zeile) columns(spalte) 
zeile = length(bild(:,1));
spalte = length(bild(1,:));


%Estimation of center of gravity
Summe = sum(sum(bild));

vektor_aa = ( (1:zeile)'*ones(1,spalte) ).*bild;    % using matrices and their multiplication
vektor_bb = ( ones(1,zeile)'*(1:spalte) ).*bild;    % to speed up
center_y = round(sum(sum(vektor_aa))/Summe);
center_x = round(sum(sum(vektor_bb))/Summe);

% v_start = [0;0];  % old version, slow
% for aa = 1:zeile
%     for bb = 1:spalte
%         vektor = bild(aa,bb)*[bb;aa] + v_start;
%         v_start = vektor;
%     end
%     
% end
% 
% center_x = round(vektor(1,1)/Summe);
% center_y = round(vektor(2,1)/Summe);


%vectors for the fit
line_x = bild(center_y,:)';
line_y = bild(:,center_x)';

%initial values 

maxInten=max(line_x); %a1


zz_x = center_x; %b1 -> x
zz_y = center_y; %b1 -> y


width_x = 400; %1/e^2 - width c1
width_y = 400;


offset_x = 0;  %d1 - offset
offset_y = 0;  %d2 - offset


%Fit in horizonal direction (x)

x = 1:length(line_x);

%Fit-Optionen and Fittype 
s=fitoptions('method','NonlinearLeastSquares');
set(s, 'MaxIter', 1000,'MaxFunEvals',500);
g=fittype('a1*exp(-2*((x-b1)/c1)^2)','coefficients',{'a1','b1','c1'}, 'independent', 'x', 'options', s);
[para,gof2]=fit(x',line_x,g, 'StartPoint', [maxInten, zz_x, width_x]);
%Parameter Output
fitpara=[para.a1 para.b1 para.c1];
gauss_funktion_x = @(x) para.a1*exp(-2*((x-para.b1)./para.c1).^2);
%figure
% plot(x, gauss_funktion_x(x), x, line_x)

radius_x(a) = para.c1*5.2; %5.2µm pixel pitch
disp('Gaussian fit parameters output for x direction:');
disp(fitpara);




%Fit in horizonal direction (x)

y = 1:length(line_y);

%Fit-Optionen and Fittype
s_y=fitoptions('method','NonlinearLeastSquares');
set(s_y, 'MaxIter', 1000,'MaxFunEvals',500);
g_y=fittype('a2*exp(-2*((x-b2)/c2)^2)','coefficients',{'a2','b2','c2'}, 'independent', 'x', 'options', s_y);
[para_y,gof2_y]=fit(y',line_y',g_y, 'StartPoint', [maxInten, zz_y, width_y]);
%Parameter output
fitpara_y=[para_y.a2 para_y.b2 para_y.c2];
gauss_funktion_y = @(x) para_y.a2*exp(-2*((x-para_y.b2)./para_y.c2).^2);
%figure
% plot(x, gauss_funktion_y(x), x, line_x)
disp('Gaussian fit parameters output for y direction:');
disp(fitpara_y);
radius_y(a) = para_y.c2*5.2; %5.2µm pixel pitch


figure(1)
subplot(2,1,1)
plot(x, gauss_funktion_x(x), x, line_x)
xlabel('x [px]')
ylabel('Intensity [arb. units]')

subplot(2,1,2)
%iptsetpref('ImshowAxesVisible','on');
%imshow(bild,[], 'InitialMagnification',100)
imagesc(bild)
xlabel('x [px]')
ylabel('y [px]')
axis equal
colormap(jet)
colorbar

drawnow
end

disp('radius in x direction:');
disp(radius_x);
disp('radisu in y direction:');
disp(radius_y);



%laenge=length(maximum);

inkrement1 = 5; %in [mm]

inkrement2 = 10; %in [mm]

inkrement3 = 50; %in [mm]

%Hier die Bereiche eingeben in denen mit den jeweiligen Schrittweiten
%gegangen wurde
% Enter the step size and the intervals where these steps were applied.
position1 = (0:19)*inkrement1;
position2 = position1(end)+(1:10)*inkrement2;
position3 = position2(end)+(1:5)*inkrement3;


position = [position1, position2, position3];

radius_x = abs(radius_x);
radius_y = abs(radius_y);


figure(2)
plot(position, radius_x,'r', position, radius_y,'k')
xlabel('z [mm]')
ylabel('radius [µm]')
h = legend('x-direction (d = 0 µm)','y-direction (d = 0 µm)','Location','nw');
set(h,'Interpreter','none')


caustic();  % call program