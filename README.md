# TP1-SL-Daemon

Este proyecto consiste en un daemon diseñado para monitorear una carpeta compartida, la cual en este caso está sincronizada con Dropbox, en busca de nuevos archivos que cumplan con ciertas condiciones específicas en sus nombres. Cuando se detecta un archivo nuevo que cumple con los criterios establecidos, se envía automáticamente un correo electrónico notificando su detección. Por otro lado, si un archivo recién agregado no cumple con las condiciones establecidas, será eliminado de la carpeta compartida, y también se enviará una notificación por correo electrónico informando sobre esta acción. En ambos casos, se mantiene un registro detallado de las acciones realizadas en un archivo de registro.


## Requisitos previos

• Python 3.x

• Acceso a Internet para enviar correos electrónicos (SMTP).

• Permisos de lectura y escritura en la carpeta compartida, en el archivo de configuración del daemon y en el archivo de registro.


## Instalación
• Cloná este repositorio en tu máquina local:

    git clone https://github.com/Seba-Aguero/TP1-SL-Daemon.git

• Asegurate de tener los archivos de configuración necesarios (mail.txt, horarios_suspension.txt, expresion_regular.txt) en el directorio Config.

• Adaptá los archivos de configuración según tus necesidades.


## Uso

Nota: Adaptá las rutas a las que correspondan en tu PC.

### Ejecución manual:

Ejecutá el daemon con el siguiente comando:

    python3 daemon.py

El daemon comenzará a monitorear la carpeta compartida y enviará correos electrónicos cuando se detecten nuevos archivos.


### Inicio automático al arrancar:

Creá en el directorio '/etc/systemd/system/' el archivo 'tp1_sl_daemon.service' con el siguiente contenido:

    [Unit]
    Description=TP1-SL-Daemon
    After=network.target

    [Service]
    User=debian
    WorkingDirectory=/home/debian/Documentos/Daemon
    ExecStart=/usr/bin/python3 daemon.py

    [Install]
    WantedBy=multi-user.target


Ejecutá los siguientes comandos:

    sudo systemctl daemon-reload

    sudo systemctl enable tp1_sl_daemon.service

    sudo systemctl start tp1_sl_daemon.service


Para verificar que el daemon esté funcionando correctamente:

    sudo systemctl status tp1_sl_daemon.service


Para detener el daemon:

    sudo systemctl stop tp1_sl_daemon.service


Para reiniciarlo:

    sudo systemctl restart tp1_sl_daemon.service


## Configuración

• mail.txt: Archivo que contiene la dirección de correo electrónico a la que se enviarán las notificaciones.

• horarios_suspension.txt: Archivo que contiene los horarios en los que el daemon estará en modo de suspensión temporal.

• expresion_regular.txt: Archivo que contiene la expresión regular que deben cumplir los nombres de los archivos para ser admitidos.


## Archivos de registro

El daemon registra sus acciones en un archivo de registro llamado tp1-daemon.log, ubicado en /var/log. Este archivo contiene un registro de las detecciones de nuevos archivos y eliminaciones de archivos no válidos.


