import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import threading
import random
from PIL import Image

NUM_FRAMES = 120
ANCHO_ESCENARIO = 100
ALTO_ESCENARIO = 40
NUM_HILOS = 4

frames = [np.zeros((ALTO_ESCENARIO, ANCHO_ESCENARIO, 3), dtype=np) for _ in range(NUM_FRAMES)]
lock = threading.Lock()

OBJETOS = {
    'nube': {
        'matriz': np.array([
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,1,1,1,0,0,0,0],
            [0,0,1,1,1,1,1,1,1,1,0,0],
            [0,1,1,1,1,1,1,1,1,1,1,0],
            [1,1,1,1,1,1,1,1,1,1,1,1]
        ]),
        'color': [222, 255, 251]
    },
    'piedra': {
        'matriz': np.array([
            [0,0,0,0,0,0],
            [0,0,1,1,1,0],
            [1,1,1,1,1,1],
            [1,1,1,1,1,1]
        ]),
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
        pos_y = 0 if tipo == 'nube' else ALTO_ESCENARIO - obj['matriz'].shape[0] - 2 
        fondo = colocar_objeto(fondo, obj['matriz'], pos_y, pos_x, obj['color'])
    return fondo

ESCENARIO_FIJO = crear_escenario_fondo()

def crear_dinosaurio(mover_izq, mover_der):
    dino = np.array([
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,1,1,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,1,0,0,0,0],
        [0,0,0,1,1,1,1,1,0,1,1,1,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,1,0,0],
        [0,0,0,0,1,1,1,1,1,1,0,0,0,0],
        [0,0,0,0,0,1,1,1,1,0,0,0,0,0],
        [0,1,0,0,0,1,1,1,1,0,0,0,0,0],
        [0,1,1,0,1,1,1,1,1,1,0,0,0,0],
        [0,1,1,0,1,1,1,1,1,1,1,1,0,0],
        [0,0,1,1,1,1,1,1,1,1,0,1,0,0],
        [0,0,1,1,1,1,1,1,1,1,0,0,0,0],
        [0,0,0,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,1,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ])

    if mover_izq:
        dino[14:16, 4:6] = 0
    if mover_der:
        dino[14:16, 7:9] = 0
    return dino

def procesar_lote(inicio, fin):
    for i in range(inicio, fin):
        mover_izq = (i % 2 == 0)
        escenario = np.copy(ESCENARIO_FIJO)
        dino = crear_dinosaurio(mover_izq, not mover_izq)
        color = [85, 124, 0]
        pos_x = (i * 2) % (ANCHO_ESCENARIO - dino.shape[1])
        pos_y = ALTO_ESCENARIO - dino.shape[0] - 1  
        escenario = colocar_objeto(escenario, dino, pos_y, pos_x, color)
        with lock:
            frames[i] = escenario
            

hilos = []
frame_por_hilo = NUM_FRAMES // NUM_HILOS

for i in range(NUM_HILOS):
    inicio = i * frame_por_hilo
    fin = (i + 1) * frame_por_hilo if i != NUM_HILOS - 1 else NUM_FRAMES
    hilo = threading.Thread(target=procesar_lote, args=(inicio, fin))
    hilos.append(hilo)
    hilo.start()

for hilo in hilos:
    hilo.join()

fig = plt.figure(figsize=(10, 5))
img = plt.imshow(frames[0], animated=True)
plt.axis('off')

def actualizar(i):
    img.set_array(frames[i % NUM_FRAMES])
    return [img]

ani = animation.FuncAnimation( 
    fig, actualizar, frames=NUM_FRAMES, interval=100, blit=True
)

plt.tight_layout()
plt.show()
