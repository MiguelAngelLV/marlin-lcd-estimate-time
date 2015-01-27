#Script para añadir tiempo restante al gcode

Pequeño script y plugin para Cura que modifica el gcode añadiendo la instrucción `M117` indicando el tiempo restante aunque no esté conectado al PC, solo con la pantalla y la SD.

El script necesita la aceleración de los ejes. Así mismo, hay que añadir un _factor de ajuste_, por defecto de **1.2**

En las pruebas, el resultado ha sido bastante preciso, pero podría variar en otras impresoras y velocidades.

La separación entre horas y minutos usa un punto ".", al colocar dos puntos ":" el mensaje se corta. 

Se puede usar en Slic3r usando el script normal.