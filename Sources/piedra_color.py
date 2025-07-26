import numpy as np
import matplotlib.pyplot as plt

piedra = np.array([                            
    [0,0,0,0,0,0,0,0],
    [0,0,0,1,1,1,0,0],
    [0,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,0],
    [0,0,0,0,0,0,0,0]
])
imagen_rgb = np.ones((*piedra.shape, 3)) * 255 
imagen_rgb[piedra == 1] = [100, 100, 100]   
   
plt.imshow(imagen_rgb.astype(np.uint8))
plt.axis('off')
plt.show()