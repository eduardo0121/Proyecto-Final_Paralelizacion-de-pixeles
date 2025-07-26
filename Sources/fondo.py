import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random

ANCHO_ESCENARIO = 100
ALTO_ESCENARIO = 40

OBJETOS = {
    'nube': {
        'matriz': np.array([
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,1,1,1,0,0,0,0],
            [0,0,1,1,1,1,1,1,1,1,0,0],
            [0,1,1,1,1,1,1,1,1,1,1,0],
            [1,1,1,1,1,1,1,1,1,1,1,1]
        ], dtype=np.float32),
        'color': [222, 255, 251]
    },
    'piedra': {
        'matriz': np.array([
            [0,0,0,0,0,0],
            [0,0,1,1,1,0],
            [1,1,1,1,1,1],
            [1,1,1,1,1,1]
        ], dtype=np.float32),
        'color': [100, 100, 100]
    },
}

fondo_imagen = Image.open("imagen.jpg").resize((ANCHO_ESCENARIO, ALTO_ESCENARIO))
FONDO_RGB = np.array(fondo_imagen)

def colocar_objeto(imagen, matriz, pos_y, pos_x, color):
    alto, ancho = matriz.shape
    for y in range(alto):
        for x in range(ancho):
            if matriz[y, x] > 0:
                if 0 <= pos_y + y < imagen.shape[0] and 0 <= pos_x + x < imagen.shape[1]:
                    imagen[pos_y + y, pos_x + x] = color
    return imagen

def crear_escenario_fondo():
    fondo = np.copy(FONDO_RGB)
    for x in range(0, ANCHO_ESCENARIO, 15):
        tipo = random.choice(list(OBJETOS.keys()))
        obj = OBJETOS[tipo]
        pos_x = min(x, ANCHO_ESCENARIO - obj['matriz'].shape[1])
        pos_y = 0 if tipo == 'nube' else ALTO_ESCENARIO - obj['matriz'].shape[0] - 1
        fondo = colocar_objeto(fondo, obj['matriz'], pos_y, pos_x, obj['color'])
    return fondo

# Generar y mostrar el suelo con objetos
ESCENARIO = crear_escenario_fondo()

plt.imshow(ESCENARIO)
plt.axis('off')
plt.show()
