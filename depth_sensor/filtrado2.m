clear all;
close all;
delete(instrfind({'Port'},{'COM7'})); 

% configurar la conexión serial
s = serial('COM7', 'BaudRate', 115200);
fopen(s);

%tiempo_total = input("Ingresa el tiempo de medición (s) : ");
% parametros iniciales
i = 1;
tic; 
windowSize = 2;
fs = 0.5;

% Crear la figura
figure;

% Crear las líneas de la gráfica
line1 = plot(0, 0, 'r');
hold on;
line2 = plot(0, 0, 'g');
line3 = plot(0, 0, 'b');

% Configurar etiquetas y título
xlabel("Tiempo [seg]");
ylabel("Distancia [cm]");
legend('Distancia', 'No Spurious', 'Sigma','Location', 'northwest');
title("Grafica en Tiempo Real");

% bucle para leer y plotear los datos en tiempo real
while true %toc < tiempo_total
      
    t(i) = toc;
    % leer los datos del sensor
    distancia(i) = fscanf(s, '%d');
    moving_average = movmean(distancia, windowSize);
    sigma = minus(distancia, moving_average);
    sigma_num = peak2peak(sigma);
    %muestreamos el audio cada dos segundos aqui
    if i > 1
        if (distancia(i) >= moving_average(i) + sigma_num/100) || (distancia(i) <= moving_average(i) - sigma_num/100)
       
            no_sporious(i) = NaN;%no_sporious(i-1);
        else
            no_sporious(i) = distancia(i);
        
        end
    else
        no_sporious(i) = distancia(i);
    end

    % Actualizar los datos de la gráfica en tiempo real
    set(line1, 'XData', t(1:i), 'YData', distancia(1:i));
    set(line2, 'XData', t(1:i), 'YData', no_sporious(1:i));
    set(line3, 'XData', t(1:i), 'YData', sigma(1:i));
    %set(gca,'Color','k')
    drawnow;  % Actualizar la figura en tiempo real
    %play_distance_audio(distancia(i));%acuerdate de poner no_sporious(i));
    i = i + 1;

end