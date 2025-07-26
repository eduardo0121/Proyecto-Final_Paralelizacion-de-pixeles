import numpy as np
from PIL import Image
import matplotlib.pyplot as plt  

ANCHO_ESCENARIO = 100
ALTO_ESCENARIO = 40

fondo_imagen = Image.open("imagen.jpg").resize((ANCHO_ESCENARIO, ALTO_ESCENARIO))

FONDO_RGB = np.array(fondo_imagen)

plt.imshow(FONDO_RGB)
plt.axis('off')  
plt.show()
