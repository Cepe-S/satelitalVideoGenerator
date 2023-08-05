from datetime import datetime
from typing import List
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

def getDate() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def enviar_emails(contenido: str):
    with open("emails.json", "r") as file:

        for destinatario in json.load(file):
            enviar_email(destinatario, contenido)

def enviar_email(destinatario, contenido):
    # Configurar los detalles del servidor SMTP de Gmail
    servidor_smtp = "smtp.gmail.com"
    puerto_smtp = 587
    correo_emisor = "santicepeda03@gmail.com"
    contraseña_emisor = "wzwmnjvfjywojewy"

    # Crear el mensaje
    mensaje = MIMEMultipart()
    mensaje["From"] = correo_emisor
    mensaje["To"] = destinatario
    mensaje["Subject"] = "ERROR EN EL SISTEMA DE GENERACION DE VIDEOS DE MAPAS SATELITALES"

    # Agregar el contenido del mensaje
    mensaje.attach(MIMEText(contenido, "plain"))

    # Establecer la conexión con el servidor SMTP
    servidor = smtplib.SMTP(servidor_smtp, puerto_smtp)
    servidor.starttls()

    # Iniciar sesión en la cuenta de correo emisor
    servidor.login(correo_emisor, contraseña_emisor)

    # Enviar el mensaje
    servidor.sendmail(correo_emisor, destinatario, mensaje.as_string())

    # Cerrar la conexión con el servidor SMTP
    servidor.quit()


class Log:

    codes = {0: "success", 1: "warning", 2: "error"}
    log_file = "log.txt"

    def __init__(self):
        pass

    def write(message: str, code: int):
        with open(Log.log_file, 'a') as file:
            file.write(f"{getDate()} [{Log.codes[code]}] {message}\n")
        if code == 2:
            # envia un mail
            enviar_emails(message)

    def runnerStarted():
        Log.write("Runner started", 0)


    def imageDownloaded(file: str):
        Log.write(f"Image \"{file}\" downloaded", 0)

    def imageDeleted(file: str):
        Log.write(f"Image \"{file}\" deleted", 0)

    def imageNotFound(file: str):
        Log.write(f"Image \"{file}\" not found", 1)

    def forbiddenAccess(link: str):
        Log.write(f"Forbidden access to image {link}", 2)

    def externalServerError(link: str, code: int):
        Log.write(f"External server error in image \"{link}\" with code {code}", 2)

    def unmanagedImageError(file: str, code: int):
        Log.write(f"Unmanaged image error in image \"{file}\" with code {code}", 2)



    def bufferUpdated(newFile: str, oldFile: str):
        Log.write(f"Buffer updated. New file: \"{newFile}\". Old file: \"{oldFile}\"", 0)

    def bufferFailedDownloadTry(tryNumber: int):
        Log.write(f"Image download try number {tryNumber} failed", 1)

    def bufferGaveUp(image: str):
        Log.write(f"Buffer gave up, image \"{image}\" is missing", 2)


    def videoRenderingStarted():
        Log.write("Rendering started", 0)
    
    def videoUpdated():
        Log.write("Video updated", 0)

    def videoRenderingError(e: Exception):
        Log.write(f"Video rendering error: {e}", 2)

    def shutdown():
        Log.write("Runner shutdown", 0)

