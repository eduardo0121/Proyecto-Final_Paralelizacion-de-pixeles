import numpy as np
import matplotlib.pyplot as plt

nube = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,1,1,1,0,0,0,0,0],
    [0,0,0,1,1,1,1,1,1,1,1,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
])

imagen_rgb = np.ones((*nube.shape, 3)) * 255  
imagen_rgb[nube == 1] = [222, 255, 251]       

plt.imshow(imagen_rgb.astype(np.uint8))
plt.axis('off')
plt.show()