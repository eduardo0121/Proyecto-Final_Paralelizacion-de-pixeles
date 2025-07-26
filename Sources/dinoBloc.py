import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import threading
import random

NUM_FRAMES = 60
ANCHO_ESCENARIO = 50
ALTO_ESCENARIO = 20
NUM_HILOS = 4


frames = [np.zeros((ALTO_ESCENARIO, ANCHO_ESCENARIO)) for _ in range(NUM_FRAMES)]
lock = threading.Lock()

OBJETOS = {
    'nube': {
        'matriz': np.array([
            [0,0,0,1,1,0,0],
            [0,1,1,1,1,1,0],
            [1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0]
        ], dtype=np.float32),
        'min_altura': 0,
        'max_altura': 3  
    },
    
    'piedra': {
        'matriz': np.array([
            [0,0,0,0,0,0],
            [0,0,1,1,1,0],
            [1,1,1,1,1,1],
            [1,1,1,1,1,1]
          
        ], dtype=np.float32),
        'min_altura': ALTO_ESCENARIO-7, 
        'max_altura': ALTO_ESCENARIO-0
    },
    
}

def crear_escenario_fondo():
    fondo = np.zeros((ALTO_ESCENARIO, ANCHO_ESCENARIO), dtype=np.float32)
    fondo[-1:, :] = 1  # Línea del suelo

    for x in range(0, ANCHO_ESCENARIO, 15):  
        tipo = random.choice(list(OBJETOS.keys()))
        obj_data = OBJETOS[tipo]
        obj = obj_data['matriz']
        obj_altura = obj.shape[0]

        pos_x = min(x, ANCHO_ESCENARIO - obj.shape[1])


        if tipo == 'nube':
            pos_y = 0  
        elif tipo == 'piedra' or tipo == 'arbol':
            pos_y = ALTO_ESCENARIO - obj_altura - 1 

        if pos_y + obj_altura <= ALTO_ESCENARIO:
            area = fondo[pos_y:pos_y+obj_altura, pos_x:pos_x+obj.shape[1]]
            fondo[pos_y:pos_y+obj_altura, pos_x:pos_x+obj.shape[1]] = np.maximum(area, obj)

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
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ], dtype=np.float32)

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

        pos_x = (i * 2) % (ANCHO_ESCENARIO - dino.shape[1])
        pos_y = 3
        
        area = escenario[pos_y:pos_y+dino.shape[0], pos_x:pos_x+dino.shape[1]]
        escenario[pos_y:pos_y+dino.shape[0], pos_x:pos_x+dino.shape[1]] = np.maximum(area, dino)

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
img = plt.imshow(frames[0], cmap='binary', vmin=0, vmax=1, animated=True)
plt.axis('off')

def actualizar(i):
    img.set_array(frames[i % NUM_FRAMES])
    return [img]

ani = animation.FuncAnimation(
    fig, actualizar, frames=NUM_FRAMES, interval=100, blit=True
)

plt.tight_layout()
plt.show()