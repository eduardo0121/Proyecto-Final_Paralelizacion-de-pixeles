![Image](https://github.com/user-attachments/assets/fc282593-eb86-4a64-b694-a8d313c39c4f)
# Proyecto de Animación por Paralelización de Píxeles


Una implementación en Python para la generación de animaciones suaves mediante procesamiento paralelo de píxeles utilizando threading, NumPy y Matplotlib.

## 🛠️ Características

- 🦕 **Animación de Dinosaurio**: Animación compuesta por 120 fotogramas con un sprite de dinosaurio caminando.
- ⚡ **Procesamiento Paralelo**: Uso de 4 hilos para generar los frames de manera eficiente.
- 🖼️ **Composición Dinámica de Escenario**: Escenario animado con nubes y rocas colocadas aleatoriamente.
- 🔒 **Operaciones Seguras entre Hilos**: Sincronización correcta utilizando threading.Lock.
- 📊 **Visualización**: Reproducción de la animación en tiempo real usando Matplotlib.

## 🧱 Tecnologías Utilizadas

    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    import numpy as np
    import threading
    import random
    from PIL import Image

## 📁 Estructura del Proyecto

    /Sources: Archivos fuente Python
    /Img: Representaciones visuales
    /Docs: Documentacion tecnica

## 🚀 Instalación y Ejecución

1. Clona el repositorio:

    git clone https://github.com/eduardo0121/Proyecto-Final_Paralelizacion-de-pixeles.git

2. Instala las dependencias necesarias:

    pip install numpy pillow matplotlib

3. Ejecuta la animación:

    python Sources/EscenarioFinal.py

## 🔍 Detalles Clave de Implementación

### 🔄 Generación Paralela de Fotogramas

    NUM_HILOS = 4  # Usando 4 hilos
    frames = [np.zeros((ALTO_ESCENARIO, ANCHO_ESCENARIO, 3)) for _ in range(NUM_FRAMES)]
    lock = threading.Lock()  # Sincronización entre hilos

### 🧩 Gráficos Basados en Matrices

    # Ejemplo de definición de objeto
    OBJETOS = {
        'nube': {
            'matriz': np.array([...]),  # Matriz binaria
            'color': [222, 255, 251]    # Valores RGB
        }
    }

### 🎞️ Bucle de Animación

    ani = animation.FuncAnimation(
        fig, actualizar, frames=NUM_FRAMES, interval=100, blit=True
    )

## 📈 Métricas de Rendimiento

| Métrica              | Valor     |
|----------------------|-----------|
| Fotogramas totales   | 120       |
| Hilos utilizados     | 4         |
| Tiempo de generación | ~X segundos* |

> * El tiempo real puede variar según el hardware utilizado.
