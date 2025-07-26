import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Matriz del dinosaurio y color verde
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
])
color = [85, 124, 0]  

def movimiento(frame):
    d = dino.copy()
    d[14:16, (4,5) if frame%2 else (7,8)] = 0 
    img_rgb = np.ones((*d.shape, 3)) * 255 
    img_rgb[d == 1] = color  # Aplicar color verde
    img.set_array(img_rgb.astype(np.uint8))
    return [img]

# Mostrar animación
fig, ax = plt.subplots()
img = ax.imshow(np.ones((*dino.shape, 3)))  # Inicializar
plt.axis('off')
ani = animation.FuncAnimation(fig, movimiento, frames=10, interval=300, blit=True)
plt.show()