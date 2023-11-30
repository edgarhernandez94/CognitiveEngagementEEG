import pylsl
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

def conectar_stream_lsl(nombre_stream):
    streams = pylsl.resolve_stream('name', nombre_stream)
    return pylsl.StreamInlet(streams[0])

def calcular_cognitive_engagement(df_real_time):
    betas = df_real_time.iloc[:, 3::5].mean(axis=1)
    alphas = df_real_time.iloc[:, 2::5].mean(axis=1)
    thetas = df_real_time.iloc[:, 1::5].mean(axis=1)
    df_real_time['CEng'] = betas / (alphas + thetas)
    return df_real_time

def procesar_datos_en_tiempo_real(stream_inlet, tiempo_de_procesamiento=60):
    tiempo_final = time.time() + tiempo_de_procesamiento
    columnas = ['Canal' + str(i) for i in range(1, 41)]
    df_real_time = pd.DataFrame(columns=columnas)

    plt.ion()  # Activa el modo interactivo de Matplotlib
    fig, ax = plt.subplots()
    ax.set_xlabel('Muestras')
    ax.set_ylabel('Cognitive Engagement')
    ax.set_title('Cognitive Engagement en Tiempo Real')

    while time.time() < tiempo_final:
        muestras, timestamp = stream_inlet.pull_sample()
        if muestras:
            df_muestra = pd.DataFrame([muestras], columns=columnas)
            df_real_time = pd.concat([df_real_time, df_muestra], ignore_index=True)
            df_real_time = calcular_cognitive_engagement(df_real_time)

            # Actualizar el gráfico
            ax.clear()
            ax.plot(df_real_time['CEng'])
            plt.pause(0.1)  # Pausa breve para actualizar el gráfico

    plt.ioff()  # Desactiva el modo interactivo
    return df_real_time

# Conectar al stream LSL
stream_inlet = conectar_stream_lsl("AURA_Power_Power")

# Procesar los datos en tiempo real durante 60 segundos
df_datos_en_tiempo_real = procesar_datos_en_tiempo_real(stream_inlet, 60)
