import os
import re
import time
from datetime import datetime, time as time2

CARPETA_COMPARTIDA = "/home/debian/Documentos/Compartida"
ARCHIVO_HORARIOS = "/home/debian/Documentos/Daemon/Config/horarios_suspension.txt"
ARCHIVO_EXPRESION_REGULAR = "/home/debian/Documentos/Daemon/Config/expresion_regular.txt"
ARCHIVO_NOMBRES_PROCESADOS = "/home/debian/Documentos/Daemon/nombres_procesados.txt"

def leer_archivo(archivo):
    data = None
    try:
        with open(archivo, 'r') as f:
            data = [line.strip() for line in f.readlines()]
            f.close()
    except FileNotFoundError:
        print(f"No se encontró el archivo {archivo}.")
    return data

# Función para leer la configuración de suspensión temporal desde un archivo
def leer_horarios_suspension(archivo):
    horarios_suspension = []
    try:
        with open(ARCHIVO_HORARIOS, 'r') as f:
            for linea in f:
                horas, minutos = map(int, linea.strip().split(':'))  # Dividir la línea en horas y minutos
                horario = time2(horas, minutos)
                horarios_suspension.append(horario)
    except FileNotFoundError:
        print(f"No se encontró el archivo {archivo}.")
    return horarios_suspension

# Función para eliminar un archivo
def eliminar_archivo(archivo):
    try:
        os.remove(archivo)
        print(f"Archivo {archivo} eliminado correctamente.")
    except FileNotFoundError:
        print(f"El archivo {archivo} no existe.")
    except Exception as e:
        print(f"Error al eliminar el archivo {archivo}: {e}")

# Función para monitorear la carpeta compartida
def main():
    # Leer el correo electrónico y la expresión regular desde los archivos de configuración
    horarios_suspension = leer_horarios_suspension(ARCHIVO_HORARIOS)
    expresion_regular = leer_archivo(ARCHIVO_EXPRESION_REGULAR)[0]
    nombres_procesados = leer_archivo(ARCHIVO_NOMBRES_PROCESADOS)
    print("Nombres ya procesados: ", nombres_procesados)

    while True:
        try:
            # Lógica para suspensión temporal
            hora_actual = datetime.now().time()
            if horarios_suspension[0] <= hora_actual <= horarios_suspension[1]:
                print("El daemon está en modo de suspensión temporal.")
                time.sleep(60)  # Dormir por un minuto antes de verificar nuevamente
                continue
            # Iterar sobre los archivos en la carpeta compartida
            for archivo in os.listdir(CARPETA_COMPARTIDA):
                ruta_archivo = os.path.join(CARPETA_COMPARTIDA, archivo)

                # Verificar si el archivo es nuevo y cumple con la expresión regular
                if os.path.isfile(ruta_archivo) and (archivo not in nombres_procesados) and re.match(expresion_regular, archivo):
                    print(f"Nuevo archivo encontrado: {archivo}. Enviando correo electrónico...")
                    # Enviar correo electrónico a cada destinatario
                    # Agregar el archivo a la lista de archivos procesados
                    nombres_procesados.append(archivo)
                    # Escribir el nombre del archivo en el archivo de nombres procesados
                    with open(ARCHIVO_NOMBRES_PROCESADOS, 'a') as f:
                        f.write(archivo + '\n')

                # Verificar si el archivo cumple con la expresión regular
                if expresion_regular and not re.match(expresion_regular, archivo):
                    print(f"El archivo {archivo} no cumple con la expresión regular. Eliminando...")
                    # Eliminar el archivo
                    os.remove(ruta_archivo)
                    # Enviar correo electrónico a cada destinatario

            # Dormir durante un intervalo de tiempo antes de verificar nuevamente (por ejemplo, 5 segundos)
            time.sleep(5)

        except Exception as e:
            print(f"Error en el monitoreo de la carpeta compartida: {e}")

# Llamada a la función de monitoreo de la carpeta compartida
if __name__ == "__main__":
    main()