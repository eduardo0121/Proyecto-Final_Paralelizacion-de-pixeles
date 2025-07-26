import numpy as np
from PIL import Image
import re

ARCHIVO_TXT = "matriz_fondo.txt"
ANCHO_ESCENARIO = 100
ALTO_ESCENARIO = 40

def leer_matriz_desde_txt(archivo):
    with open(archivo, 'r') as f:
        lineas = f.readlines()
    
    # Saltar encabezados (líneas que no empiezan con '[')
    filas = []
    for linea in lineas:
        if not linea.strip().startswith('['):
            continue
        
        # Limpiar línea: quitar corchetes externos y espacios
        linea_limpia = linea.strip()[1:-1].strip()
        
        # Extraer píxeles con expresión regular mejorada
        pixeles = re.findall(r'\[\s*(\d+)\s+(\d+)\s+(\d+)\s*\]', linea_limpia)
        fila = []
        for r, g, b in pixeles:
            fila.append([int(r), int(g), int(b)])
        
        filas.append(fila)
    
    return np.array(filas, dtype=np.uint8)

if __name__ == "__main__":
    try:
        matriz_reconstruida = leer_matriz_desde_txt(ARCHIVO_TXT)
        print("Forma de la matriz reconstruida:", matriz_reconstruida.shape)
        
        if matriz_reconstruida.size > 0:
            imagen = Image.fromarray(matriz_reconstruida)
            imagen.show()
            imagen.save("imagen_reconstruida.jpg")
            print("¡Imagen reconstruida exitosamente!")
        else:
            print("Error: No se pudo reconstruir la matriz. Verifica el archivo TXT.")
    except Exception as e:
        print(f"Error: {str(e)}")