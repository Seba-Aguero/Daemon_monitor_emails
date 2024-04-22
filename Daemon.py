import os
import re
import time

CARPETA_COMPARTIDA = "/home/debian/Documentos/Compartida"
ARCHIVO_EXPRESION_REGULAR = "/home/debian/Documentos/Daemon/Config/expresion_regular.txt"

def leer_archivo(archivo):
    data = None
    try:
        with open(archivo, 'r') as f:
            data = [line.strip() for line in f.readlines()]
            f.close()
    except FileNotFoundError:
        print(f"No se encontró el archivo {archivo}.")
    return data

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
    expresion_regular = leer_archivo(ARCHIVO_EXPRESION_REGULAR)[0]

    while True:
        try:
            # Iterar sobre los archivos en la carpeta compartida
            for archivo in os.listdir(CARPETA_COMPARTIDA):
                ruta_archivo = os.path.join(CARPETA_COMPARTIDA, archivo)

                # Verificar si el archivo es nuevo y cumple con la expresión regular
                if os.path.isfile(ruta_archivo) and re.match(expresion_regular, archivo):
                    print(f"Nuevo archivo encontrado: {archivo}. Enviando correo electrónico...")
                    # Enviar correo electrónico a cada destinatario
                    # Agregar el archivo a la lista de archivos procesados
                    # Escribir el nombre del archivo en el archivo de nombres procesados

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