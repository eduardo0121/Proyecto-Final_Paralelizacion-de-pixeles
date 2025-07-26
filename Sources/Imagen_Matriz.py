import numpy as np
from PIL import Image

ANCHO_ESCENARIO = 100
ALTO_ESCENARIO = 40


fondo_imagen = Image.open("imagen.jpg").resize((ANCHO_ESCENARIO, ALTO_ESCENARIO))
FONDO_RGB = np.array(fondo_imagen)

with open("matriz_fondo.txt", "w") as archivo:
    archivo.write("Matriz FONDO_RGB (forma: {}):\n\n".format(FONDO_RGB.shape))
    for fila in FONDO_RGB:
        archivo.write("[")  
        for pixel in fila:
            archivo.write("[{:3d} {:3d} {:3d}] ".format(*pixel))  # Formato: [R G B]
        archivo.write("]\n") 