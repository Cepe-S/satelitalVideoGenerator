import shutil
from errorManager import ErrorManager
from runner import Runner
from imageManager import ImageManager
import os

# TODO: agregar semáforo -> horas a las que no se pueden generar videos o semáforo para evitar que se 
#       lea el archivo mientras se está escribiendo

# TODO: agregar envío de problemas en tiempo real por mail

# TODO: terminar de definir el formato, tamaño y demás de los videos
# TODO: actualizar fondo
# TODO: agregar barra de tiempo (definir como va a ser)

# TODO: ver si es preferible que se modifique el tamaño de un mapa para que sea el mismo que el otro

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
    print("Descargando primeras imágenes")
    for satelite in satelites:
        w = ImageManager(satelite=satelite)
        w.downloadIntImages(24)

    # ejecuta el runner
    try:
        Runner().run()
    except Exception as e:
        ErrorManager.fatalError(e)

if __name__ == "__main__":
    main()


