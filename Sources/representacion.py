import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import threading

NUM_FRAMES = 60
ANCHO_ESCENARIO = 100
ALTO_ESCENARIO = 40
NUM_HILOS = 4

frames = [None] * NUM_FRAMES
lock = threading.Lock()

# Objetos representados con 1s (nubes y piedras)
OBJETOS = {
    'nube': {
        'matriz': np.array([
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,1,1,1,0,0,0,0],
            [0,0,1,1,1,1,1,1,1,1,0,0],
            [0,1,1,1,1,1,1,1,1,1,1,0],
            [1,1,1,1,1,1,1,1,1,1,1,1]
        ]),
        'color': 0.8  # gris claro
    },
    'piedra': {
        'matriz': np.array([
            [0,0,0,0,0,0],
            [0,0,1,1,1,0],
            [1,1,1,1,1,1],
            [1,1,1,1,1,1]
        ]),
        'color': 0.3  # gris oscuro
    },
}

def crear_dinosaurio():
    return np.array([
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

def colocar_objeto(matriz, objeto, pos_y, pos_x, valor):
    alto, ancho = objeto.shape
    for y in range(alto):
        for x in range(ancho):
            if objeto[y, x] == 1:
                yy = pos_y + y
                xx = pos_x + x
                if 0 <= yy < ALTO_ESCENARIO and 0 <= xx < ANCHO_ESCENARIO:
                    matriz[yy, xx] = valor

def procesar_lote(inicio, fin):
    global frames
    for i in range(inicio, fin):
        matriz = np.zeros((ALTO_ESCENARIO, ANCHO_ESCENARIO))

        # Colocar nubes
        for x in range(0, ANCHO_ESCENARIO, 25):
            colocar_objeto(matriz, OBJETOS['nube']['matriz'], 2, x, OBJETOS['nube']['color'])

        # Colocar piedras
        for x in range(5, ANCHO_ESCENARIO, 30):
            pos_y = ALTO_ESCENARIO - 6
            colocar_objeto(matriz, OBJETOS['piedra']['matriz'], pos_y, x, OBJETOS['piedra']['color'])

        # Colocar dinosaurio (movimiento)
        dino = crear_dinosaurio()
        pos_x = (i * 2) % (ANCHO_ESCENARIO - dino.shape[1])
        pos_y = ALTO_ESCENARIO - dino.shape[0] - 1
        colocar_objeto(matriz, dino, pos_y, pos_x, 1.0)

        with lock:
            frames[i] = matriz

# Hilos
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

# Visualización con "pixeles visibles"
fig, ax = plt.subplots(figsize=(10, 5))
img = ax.imshow(frames[0], cmap='gray', vmin=0, vmax=1)
plt.title("Simulación Lógica Frame a Frame (Matriz)")
plt.grid(True, color='black', linewidth=0.5)
ax.set_xticks(np.arange(-0.5, ANCHO_ESCENARIO, 1), minor=True)
ax.set_yticks(np.arange(-0.5, ALTO_ESCENARIO, 1), minor=True)
ax.grid(which='minor', color='black', linestyle=':', linewidth=0.25)
ax.tick_params(which='both', bottom=False, left=False, labelbottom=False, labelleft=False)

def actualizar(i):
    img.set_array(frames[i % NUM_FRAMES])
    return [img]

ani = animation.FuncAnimation(fig, actualizar, frames=NUM_FRAMES, interval=100, blit=True)
plt.show()
