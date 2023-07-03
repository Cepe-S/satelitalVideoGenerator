import shutil
from errorManager import ErrorManager
from runner import Runner
from imageManager import ImageManager
import os

from videoGenerator import VideoGenerator

# TODO: agregar barra de tiempo
# TODO: agregar semáforo -> horas a las que no se pueden generar videos o semáforo para evitar que se 
#       lea el archivo mientras se está escribiendo
# TODO: terminar de definir el formato, tamaño y demás de los videos
# TODO: agregar vista central de satelite
# TODO: agregar envío de problemas en tiempo real por mail
# TODO: actualizar fondo
# TODO: sacar parte de arriba de la imagen?
# TODO: agregar donde esta mar del plata?


def main():

    # cambia el directorio de trabajo al directorio del programa
    separador = os.path.sep
    dir_actual = os.path.dirname(os.path.abspath(__file__))
    os.chdir(separador.join(dir_actual.split(separador)[:-1]))
    
    # si existe la carpeta buffer la vacía
    if os.path.exists("buffer"):
        shutil.rmtree("buffer")

    satelites = ["CEN", "ARG"]

    # descarga las primeras 24 imágenes de todos los satélites
    for satelite in satelites:
        w = ImageManager(satelite=satelite)
        w.downloadIntImages(24)

    # ejecuta el runner
    try:
        Runner().run()
    except Exception as e:
        ErrorManager.fatalError(e)

main()
