# encoding: utf-8 

# Images.py
# Este código va orientado a la toma de imágenes de video mediante la librería open cv en Python...
# Genera un número finito de imagenes en la carpeta enumerandolas del 1 al final de la toma de datos
# Para finalizar la toma de datos pulsa la tecla Q minúscula "q"

# Programador Sergio Luis Beleño Díaz
# 12.feb.2020

#Para empezar se importa la librería de Open cv para visión Artificial

import cv2
from scipy import ndimage

# Asignamos la cámara ingresando cv2.VideoCapture(0)
# Si quiere asignar una segunda cámara externa puede usar cv2.VideoCapture(1)
cap = cv2.VideoCapture('B10.mp4')

formato = '.jpg'
name = 17516
tipo = 'RD_RD'

# Toma parámetros de captura de la cámara
[rec, camara] = cap.read()

while(rec == 1):

	# Toma parámetros de captura de la cámara
	[rec, camara] = cap.read()
	name = name + 1 # Contador de imagenes tomadas

	# Muestra la imagen tomada en una ventana
	if (rec ==1):


		#cv2.imshow('Captura', camara)
		file = str(tipo) + str(name) + formato

		# rotation angle in degree
		camara = cv2.resize(camara, None, fx = 0.7, fy= 0.7)
		camara = camara[20:520, 100:600]
		camara = ndimage.rotate(camara, -90)
		camara = camara[10:490, 10:490]
		# Reescala la imagen
		camara = cv2.resize(camara, (416,416))

		cv2.imshow('Camara',camara)

		if name%4 == 0:
			# Guarda la imagen tomada
			cv2.imwrite('Train/6_DefectiveRed_can/'+file,camara)
			contador_de_retardo = 0

		print("Imagen numero: " + str(name))

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
