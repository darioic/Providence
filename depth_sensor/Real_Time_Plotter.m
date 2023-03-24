close all;
delete(instrfind({'Port'},{'COM7'})); 

% configurar la conexión serial
s = serial('COM7', 'BaudRate', 115200);
fopen(s);

tiempo_total = input("Ingresa el tiempo de medición (s) : ");
intervalo = input("Ingrese el intervalo de tiempo entre mediciones (s) : ");

i = 1;
% incia un contador con reloj
tic; 
% bucle para leer y plotear los datos en tiempo real
%toc devuelve el tiempo transcurrido desde el tic
while toc < tiempo_total
    
    t(i) = toc;
    % leer los datos del sensor
    distancia(i) = fscanf(s, '%d')
    % plotear los puntos en tiempo real
    plot(t(:), distancia(:), 'r'),xlabel("Tiempo [seg]"), ylabel("Distancia [cm]"); drawnow  
    i = i + 1;
    pause(intervalo)
end

% cerrar la conexión serial
fclose(s);
delete(s);
clear s;