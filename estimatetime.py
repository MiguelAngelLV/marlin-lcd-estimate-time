#Name: Estimate Time 
#Info: Show estimated time of accomplishment
#Depend: GCode
#Type: postprocess
#Param: corfactor(float:1.2) Correction factor
#Param: accel(float:30000) Accel of axis (mm/s2)
#Param: message(str:Restante    ) Message 

import re
import math

time  = 0.
maxspeed = 3000
speed = 3000
accel = accel * 60

x = 0.
y = 0.
z = 0.



def showTime(time, actual):
  global message
  time = time - actual + 1
  return message + "{0:02d}.{1:02d}".format(time / 60, time % 60)


def getTime(line):
  
  global x, y, z, speed, accel, maxspeed

  #Calculamos la velocidad maxima
  if "F" in line:
	  maxspeed = float(re.search('F([+\-]*[0-9]+\.?[0-9]*)', line).group(1))

  #Si hay Z, la optenemos
  if "Z" in line:
    mz = float(re.search('Z([+\-]*[0-9]+\.?[0-9]*)', line).group(1))
  else:
    mz = z

  m = re.search('X([+\-]*[0-9]+\.?[0-9]*) Y([+\-]*[0-9]+\.?[0-9]*)', line)


  #Comprobamos si hay X e Y
  if (m == None):
	  mx = x
	  my = y
  else :
	  mx = float(m.group(1))
	  my = float(m.group(2))


  #Calculamos la distancia a recorrer
  dist = math.sqrt(math.pow(mx-x, 2) + math.pow(my-y, 2) + math.pow(mz - z, 2))

  #Ponemos los valores actuales como los anteriores
  x = mx
  y = my
  z = mz

  #Si la velocidad actual es mayor a la maxima, bajamos a la maxima
  if (speed > maxspeed):
    speed = maxspeed
    
    
  #Si la velocidad actual es igual a la maxima, calculamos el tiempo directamente  
  if (speed == maxspeed):  
    return dist / speed
      

  #Si la velocidad es menor, calculamos el aumento segun la aceleracion
	
  #Diferencia de velocidad
  dx = maxspeed - speed

  #Tiempo para alcanzar la velocidad maxima
  timeMS = dx / accel

  #Distancia para alcanzar la velocidad maxima
  distMS = (dx / 2 + speed) * timeMS


  #Si la distancia es menor a la necesaria para obtener la velocidad maxima, usamos la 
  #formula de aceleracion, tiempo y distancia 

  if (dist < distMS):
	#Es una ecuacion de segundo grado para obtener el tiempo en recorrer la distancia total
	#con una velocidad incial y una aceleracion
	time = (-speed + math.sqrt(math.pow(speed, 2) - 4 * accel/2 * - dist)) / accel
	#Como sabemos el tiempo, sabemos cuanto aumentaremos la velocidad y que no llegara a ser la maxima
	#por el calculo anterior al IF
	speed = speed + time * accel
	return time


  #Hemos alcanzado la velocidad maxima
  speed = maxspeed;

  #El tiempo total es el que tardamos en alcanzar la velocidad maxima 
  #y el que tardemos en recorrer la distancia sobrante tras alcanzar la velocidad maxima
  return timeMS + (dist - distMS) / speed




with open(filename, "r") as f:
  lines = f.readlines()


for line in lines:
  if line.startswith("G1 ") or line.startswith("G2 ") or line.startswith("G0 "):
      time += getTime(line) * corfactor;


time = int(time)

lasttime   = 0
actualtime = 0

with open(filename, "w") as f:
  
  for line in lines:
    if line.startswith("G1 ") or line.startswith("G2 ") or line.startswith("G0 "):
      actualtime += getTime(line)*corfactor
      #Cada minuto actualizamos el mensaje
      if (actualtime > lasttime):
	lasttime += 1
	f.write("M117 " + showTime(time, lasttime) + "\n" )
      
    if not line.startswith("M117"): 
      f.write(line)
    