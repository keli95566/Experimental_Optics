%Caustic fit 

% You only need to run "M2_main_program.m" once. When all variables are in
% workspace you can play around with "caustic.m" without calling "M2_main_program.m"
% again.

% Here, you can manipulate the data for the M2 measurement. You can for example
% exclude values that do not fit. Usually the range would be "(1:35)" or just
% use "(:)".
fit_radius = radius_x(1:35); % change here between "radius_x" and "radius_y" for different axis
position_n = position(1:35);   % position in z direction

%initial values for fit
w0_init = min(fit_radius)*1e-6; % a3 - beam waist

M2_init = 1.2; % b3

%c3
zr_init = 20*1e-3; %z-shift


if sum(size(fit_radius) ~= size(position_n))
    error('The size or dimension of fit_radius and position_n is not equal');
end

%Fit-Options and fittype
s=fitoptions('method','NonlinearLeastSquares');
set(s, 'MaxIter', 1000,'MaxFunEvals',1000);
g=fittype('sqrt(a3^2 + b3^2*(0.6328e-6)^2/3.141^2/a3^2*(z-c3)^2)','coefficients',{'a3', 'b3','c3'}, 'independent', 'z', 'options', s);
[para,gof2]=fit(((position_n)*1e-3)',(fit_radius*1e-6)',g, 'StartPoint', [w0_init, M2_init, zr_init]);

%Parameter output
fitpara_caustic_x=[para.a3 para.b3 para.c3];
disp(['w_0 = ' num2str(para.a3*1e6) ' µm']);
disp(['z_0 = ' num2str(para.c3*1e3) ' mm']);
caustic_diff = @(z) sqrt(para.a3^2 + para.b3^2*0.6328e-6^2/pi^2./para.a3^2.*(z-para.c3).^2);


figure(3)
plot(position_n-fitpara_caustic_x(3)*1e3,fit_radius,'xk', ...
    position_n-fitpara_caustic_x(3)*1e3,caustic_diff((position_n)*1e-3)*1e6,'r', ...
    'MarkerSize', 8, 'LineWidth', 1.2)
xlabel('Position z [mm]')
ylabel('Beam radius [µm]')
h = legend('Caustic in x-direction','Caustic-fit','Location','nw');
set(h,'Interpreter','none')
grid on


M2 = para.b3;
disp(['Calculated M2 = ' num2str(M2)]);