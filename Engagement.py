import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from numpy.core.multiarray import datetime_data
import glob
import pylsl
import time

meng_values = []
def esperar_texto():
    # Crear un objeto de entrada para el canal "LSL_triggers"
    print("Resolving Stream")
    canales = pylsl.resolve_stream('name', 'test_triggers')
    entrada = pylsl.StreamInlet(canales[0])

    print("Esperando texto desde otro programa...")

    while True:
        # Esperar la llegada de datos
        muestras, _ = entrada.pull_sample()

        # Obtener el texto recibido
        texto = muestras[0]

        # Mostrar el texto en la consola
        print("Texto recibido: " + texto)

        if texto == 'end_session:videomod2':
            time.sleep(5)
            print('ok')
            ejecutar()

def ejecutar():
    csv_files = glob.glob('participants/*/*.csv')
    meng_values = []  # Lista para almacenar los valores de MENG

    for i in range(0, len(csv_files), 2):
        # Leer los archivos CSV correspondientes
        file1 = csv_files[i]
        file2 = csv_files[i+1]
        ddata1 = pd.read_csv(file1)
        ddata2 = pd.read_csv(file2)


        for column in ddata1.columns[1:41]:
            ddata1[column] = ddata1[column].apply(lambda x: float(x))

        ddata1 = ddata1.drop(["Alpha.3", "Alpha.4", "Alpha.5", "Alpha.6", "Alpha.7", "Beta.3", "Beta.4", "Beta.5", "Gamma", "Gamma.1", "Gamma.2", "Gamma.5", "Gamma.6", "Gamma.7", "Delta", "Delta.1", "Delta.2", "Delta.3", "Delta.4", "Delta.5", "Delta.6", "Delta.7", "Theta.3", "Theta.4", "Theta.5"], axis=1)
        # Realizar el cálculo y actualizar la columna "AEng"
        ddata1["AEng"] = (ddata1["Gamma.3"] + ddata1["Gamma.4"]) / 2
        ddata1["VEng"] = (((ddata1["Beta.6"] + ddata1["Theta.6"]) / 2) + ((ddata1["Beta.7"] + ddata1["Theta.7"]) / 2)) / 2
        ddata1["CEng"] = ddata1['Beta'] / (ddata1['Alpha'] + ddata1['Theta'])
        ddata1['CEng.1'] = ddata1['Beta.1'] / (ddata1['Alpha.1'] + ddata1['Theta.1'])
        ddata1['CEng.2'] = ddata1['Beta.2'] / (ddata1['Alpha.2'] + ddata1['Theta.2'])
        ddata1['CogEng'] = (ddata1['CEng'] + ddata1['CEng.1'] + ddata1['CEng.2']) / 3

        # Realizar el cálculo y actualizar normalizar los valores de engagement
        ddata1["AEngN"] = (ddata1["AEng"] - ddata1["AEng"].min()) / (ddata1["AEng"].max() - ddata1["AEng"].min())
        ddata1["VEngN"] = (ddata1["VEng"] - ddata1["VEng"].min()) / (ddata1["VEng"].max() - ddata1["VEng"].min())
        ddata1["CogEngN"] = (ddata1["CogEng"] - ddata1["CogEng"].min()) / (ddata1["CogEng"].max() - ddata1["CogEng"].min())

        # Aplicar promedios móviles
        ventana = 8
        ddata1['AEngP'] = ddata1['AEng'].rolling(ventana, min_periods=5).mean()
        ddata1['CogEngP'] = ddata1['CogEng'].rolling(ventana, min_periods=5).mean()
        ddata1['VEngP'] = ddata1['VEng'].rolling(ventana, min_periods=5).mean()
        ddata1 = ddata1.dropna()

        # Realizar el cálculo y actualizar normalizar los valores de engagement
        ddata1["AEngPN"] = (ddata1["AEngP"] - ddata1["AEngP"].min()) / (ddata1["AEngP"].max() - ddata1["AEngP"].min())
        ddata1["VEngPN"] = (ddata1["VEngP"] - ddata1["VEngP"].min()) / (ddata1["VEngP"].max() - ddata1["VEngP"].min())
        ddata1["CogEngPN"] = (ddata1["CogEngP"] - ddata1["CogEngP"].min()) / (ddata1["CogEngP"].max() - ddata1["CogEngP"].min())

        # Calcular desviaciones estándar y medias.
        SAE = 1.5 * np.std(ddata1['AEngP'])
        MAE = np.mean(ddata1['AEngP'])
        SVE = 1.5 * np.std(ddata1['VEngP'])
        MVE = np.mean(ddata1['VEngP'])
        SCE = 1.5 * np.std(ddata1['CogEngP'])
        MCE = np.mean(ddata1['CogEngP'])
        SAEN = 1.5 * np.std(ddata1['AEngPN'])
        MAEN = np.mean(ddata1['AEngPN'])
        SVEN = 1.5 * np.std(ddata1['VEngPN'])
        MVEN = np.mean(ddata1['VEngPN'])
        SCEN = 1.5 * np.std(ddata1['CogEngPN'])
        MCEN = np.mean(ddata1['CogEngPN'])
        MENG1 = ((MAEN + MVEN + MCEN) / 3)
        print('engagement1', MENG1)

        for column in ddata2.columns[1:41]:
            ddata2[column] = ddata2[column].apply(lambda x: float(x))

        ddata2 = ddata2.drop(["Alpha.3", "Alpha.4", "Alpha.5", "Alpha.6", "Alpha.7", "Beta.3", "Beta.4", "Beta.5", "Gamma", "Gamma.1", "Gamma.2", "Gamma.5", "Gamma.6", "Gamma.7", "Delta", "Delta.1", "Delta.2", "Delta.3", "Delta.4", "Delta.5", "Delta.6", "Delta.7", "Theta.3", "Theta.4", "Theta.5"], axis=1)
        # Realizar el cálculo y actualizar la columna "AEng"
        ddata2["AEng"] = (ddata2["Gamma.3"] + ddata2["Gamma.4"]) / 2
        ddata2["VEng"] = (((ddata2["Beta.6"] + ddata2["Theta.6"]) / 2) + ((ddata2["Beta.7"] + ddata2["Theta.7"]) / 2)) / 2
        
        ddata2["CEng"] = ddata2['Beta'] / (ddata2['Alpha'] + ddata2['Theta'])
        ddata2['CEng.1'] = ddata2['Beta.1'] / (ddata2['Alpha.1'] + ddata2['Theta.1'])
        ddata2['CEng.2'] = ddata2['Beta.2'] / (ddata2['Alpha.2'] + ddata2['Theta.2'])
        ddata2['CogEng'] = (ddata2['CEng'] + ddata2['CEng.1'] + ddata2['CEng.2']) / 3

        # Realizar el cálculo y actualizar normalizar los valores de engagement
        ddata2["AEngN"] = (ddata2["AEng"] - ddata2["AEng"].min()) / (ddata2["AEng"].max() - ddata2["AEng"].min())
        ddata2["VEngN"] = (ddata2["VEng"] - ddata2["VEng"].min()) / (ddata2["VEng"].max() - ddata2["VEng"].min())
        ddata2["CogEngN"] = (ddata2["CogEng"] - ddata2["CogEng"].min()) / (ddata2["CogEng"].max() - ddata2["CogEng"].min())

        # Aplicar promedios móviles
        ventana = 8
        ddata2['AEngP'] = ddata2['AEng'].rolling(ventana, min_periods=5).mean()
        ddata2['CogEngP'] = ddata2['CogEng'].rolling(ventana, min_periods=5).mean()
        ddata2['VEngP'] = ddata2['VEng'].rolling(ventana, min_periods=5).mean()
        ddata2 = ddata2.dropna()

        # Realizar el cálculo y actualizar normalizar los valores de engagement
        ddata2["AEngPN"] = (ddata2["AEngP"] - ddata2["AEngP"].min()) / (ddata2["AEngP"].max() - ddata2["AEngP"].min())
        ddata2["VEngPN"] = (ddata2["VEngP"] - ddata2["VEngP"].min()) / (ddata2["VEngP"].max() - ddata2["VEngP"].min())
        ddata2["CogEngPN"] = (ddata2["CogEngP"] - ddata2["CogEngP"].min()) / (ddata2["CogEngP"].max() - ddata2["CogEngP"].min())

        # Calcular desviaciones estándar y medias.
        SAE2 = 1.5 * np.std(ddata2['AEngP'])
        MAE2 = np.mean(ddata2['AEngP'])
        SVE2 = 1.5 * np.std(ddata2['VEngP'])
        MVE2 = np.mean(ddata2['VEngP'])
        SCE2 = 1.5 * np.std(ddata2['CogEngP'])
        MCE2 = np.mean(ddata2['CogEngP'])
        SAEN2 = 1.5 * np.std(ddata2['AEngPN'])
        MAEN2 = np.mean(ddata2['AEngPN'])
        SVEN2 = 1.5 * np.std(ddata2['VEngPN'])
        MVEN2 = np.mean(ddata2['VEngPN'])
        SCEN2 = 1.5 * np.std(ddata2['CogEngPN'])
        MCEN2 = np.mean(ddata2['CogEngPN'])
        MENG2 = ((MAEN2 + MVEN2 + MCEN2) / 3)



        print(SAEN2,MAEN2,SVEN2,MVEN2,SCEN2,MCEN2)
        print('promedio:engagement2',MENG2)

        #print (ddata)
        #print (file)
        #meng_values.append(MENG)
        meng_values.append((MENG1, MENG2))

    if len(meng_values) == 2:
        if meng_values[0][0] < meng_values[0][1]:
            print("El primer valor de MENG es menor en la comparación 1.")
        elif meng_values[0][0] > meng_values[0][1]:
            print("El segundo valor de MENG es menor en la comparación 1.")
        else:
            print("Ambos valores de MENG son iguales en la comparación 1.")

        if meng_values[1][0] < meng_values[1][1]:
            print("El primer valor de MENG es menor en la comparación 2.")
        elif meng_values[1][0] > meng_values[1][1]:
            print("El segundo valor de MENG es menor en la comparación 2.")
        else:
            print("Ambos valores de MENG son iguales en la comparación 2.")
    else:
        print("Se necesitan exactamente dos pares de archivos CSV para la comparación.")
esperar_texto()