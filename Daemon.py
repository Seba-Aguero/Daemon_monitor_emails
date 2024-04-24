#!/debian/bin/env python3

import os
import smtplib
from email.mime.text import MIMEText
import re
import time
from datetime import datetime, time as time2

ARCHIVO_CARPETA_COMPARTIDA = "./Config/carpeta_compartida.txt"
ARCHIVO_MAIL = "./Config/mail.txt"
ARCHIVO_HORARIOS = "./Config/horarios_suspension.txt"
ARCHIVO_EXPRESION_REGULAR = "./Config/expresion_regular.txt"
ARCHIVO_NOMBRES_PROCESADOS = "./nombres_procesados.txt"
ARCHIVO_LOG = "/var/log/tp1-daemon.log"

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

# Función para enviar correo electrónico
def enviar_correo(destinatario, asunto, cuerpo):
    try:
        servidor_smtp = smtplib.SMTP('smtp.office365.com', 587)
        servidor_smtp.starttls()
        servidor_smtp.login('tp1daemon@hotmail.com', 'daemonSLtp1')
        mensaje = MIMEText(cuerpo)
        mensaje['From'] = 'tp1daemon@hotmail.com'
        mensaje['Subject'] = asunto
        mensaje['To'] = destinatario
        servidor_smtp.send_message(mensaje)
        print("Se envió correo a: ", destinatario)
        servidor_smtp.quit()
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Función para eliminar un archivo
def eliminar_archivo(archivo):
    try:
        os.remove(archivo)
        print(f"Archivo {archivo} eliminado correctamente.")
    except FileNotFoundError:
        print(f"El archivo {archivo} no existe.")
    except Exception as e:
        print(f"Error al eliminar el archivo {archivo}: {e}")

# Función para escribir en un archivo
def escribir_en_archivo(ubicacion, texto):
    with open(ubicacion, 'a') as f:
        f.write(texto + '\n')

def escribir_log(cuerpo):
    fecha_formateada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensaje = fecha_formateada + " - " + cuerpo
    escribir_en_archivo(ARCHIVO_LOG, mensaje)

# Función para monitorear la carpeta compartida
def main():
    carpeta_compartida = leer_archivo(ARCHIVO_CARPETA_COMPARTIDA)[0]
    mail = leer_archivo(ARCHIVO_MAIL)[0]
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
            for archivo in os.listdir(carpeta_compartida):
                ruta_archivo = os.path.join(carpeta_compartida, archivo)

                # Verificar si el archivo es nuevo y cumple con la expresión regular
                if os.path.isfile(ruta_archivo) and (archivo not in nombres_procesados) and re.match(expresion_regular, archivo):
                    print(f"Nuevo archivo encontrado: {archivo}. Enviando correo electrónico...")
                    # Enviar correo electrónico a cada destinatario
                    asunto = f"Nuevo archivo: {archivo}"
                    cuerpo = f"Se ha encontrado un nuevo archivo en la carpeta compartida: {archivo}."
                    enviar_correo(mail, asunto, cuerpo)
                    # Agregar el archivo a la lista de archivos procesados
                    nombres_procesados.append(archivo)
                    # Escribir el nombre del archivo en el archivo de nombres procesados
                    escribir_en_archivo(ARCHIVO_NOMBRES_PROCESADOS, archivo)
                    # Log
                    escribir_log(cuerpo)

                # Verificar si el archivo cumple con la expresión regular
                if expresion_regular and not re.match(expresion_regular, archivo):
                    print(f"El archivo {archivo} no cumple con la expresión regular. Eliminando...")
                    # Eliminar el archivo
                    os.remove(ruta_archivo)
                    # Enviar correo electrónico a cada destinatario
                    asunto = f"Archivo no válido: {archivo}"
                    cuerpo = f"El archivo {archivo} no cumple con la expresión regular y ha sido eliminado."
                    enviar_correo(mail, asunto, cuerpo)
                    # Log
                    escribir_log(cuerpo)

            # Dormir durante un intervalo de tiempo antes de verificar nuevamente (por ejemplo, 5 segundos)
            time.sleep(5)

        except Exception as e:
            print(f"Error en el monitoreo de la carpeta compartida: {e}")

# Llamada a la función de monitoreo de la carpeta compartida
if __name__ == "__main__":
    main()