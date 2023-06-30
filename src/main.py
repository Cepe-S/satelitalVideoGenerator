from runner import Runner
from imageManager import ImageManager

# TODO: agregar barra de tiempo
# TODO: agregar semáforo -> horas a las que no se pueden generar videos o semáforo para evitar que 
# TODO: preguntarle a chicho si quiere agregar la vista de sudamerica 
# TODO: terminar de definir el formato, tamaño y demás de los videos

def main():
    w = ImageManager()
    w.downloadIntImages(24)

    Runner().run()

main()