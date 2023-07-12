import os
from time import sleep
import requests
import datetime
from typing import List

from link import Link
from log import Log
from utilities import Util
from errorManager import ErrorManager
# se encarga de obtener las imagenes del satelite

bestTryOrder = [20, 21, 19, 22, 18, 23, 17, 24, 16, 25, 32, 15, 31, 14, 30, 13, 29, 12, 28, 11, 27, 10, 26, 9, 8, 7, 6, 5, 4, 3, 2, 1]

class ImageManager:

    satelite = ""

    def __init__(self, satelite: str):
        self.satelite = satelite
    
    def checkBuffer(self) -> bool:
        # se verifica que exista el directorio buffer
        if not os.path.exists("buffer"):
            os.makedirs("buffer")
            os.makedirs("buffer/ARG")
            os.makedirs("buffer/CEN")
            return False
        
        if not os.path.exists("buffer/ARG"):
            os.makedirs("buffer/ARG")
            return False
        
        if not os.path.exists("buffer/CEN"):
            os.makedirs("buffer/CEN")
            return False
        
        return True

    def isInBuffer(self, link: Link) -> bool:
        # se verifica que la imagen no se encuentre en el buffer
        for seg in bestTryOrder:
            link.setSecond(seg)
            if link.getFilename() in os.listdir("buffer/" + link.getFolder()):
                return True
        return False

    # descarga una imágen y devuelve su nombre
    def downloadImage(self, date: datetime.datetime) -> str:
        
        # se crea el link y se le agrega la fecha
        link = Link(satelite=self.satelite)
        link.setDate(Util.roundTime(date))
        
        # si la imagen ya se encuentra en el buffer, no se descarga
        if self.isInBuffer(link):
            return link.getFilename()

        # se intenta descargar la imagen
        request = requests.get(link.getFinalLink())

        i = 0
        # en el caso de que no se encuentre se cambian los segundos de la fecha del link
        while request.status_code == 404 and i < len(bestTryOrder):
            link.setSecond(bestTryOrder[i])
            request = requests.get(link.getFinalLink())
            i += 1

        # si se encuentra la imagen, se guarda en el buffer
        if request.status_code == 200:
            
            self.checkBuffer()

            # se genera el nombre del archivo
            filename = link.getFilename()
            with open("buffer/" + link.getFolder() + filename, 'wb') as f:
                f.write(request.content)
                f.close()
                
            Log.imageDownloaded(link.getFolder() + filename)
            return filename
        
        if request.status_code != 200:
            ErrorManager.manageDownloadError(link.getFinalLink(), request)
            return None
        

    # descarga la cantidad de imágenes especificadas   
    def downloadIntImages(self, amount:int):
        dates = Util.generateDates(amount)
        
        self.checkBuffer()

        for date in dates:
            self.downloadImage(date)

    # devuelve una lista de imágenes con las imágenes que se encuentran en el buffer
    def getImageList(self) -> List[str]:
        if not self.checkBuffer():
            return []
        return [os.path.join("buffer/" + self.satelite, archivo) for archivo in os.listdir("buffer/" + self.satelite)]

    # actualiza el buffer y maneja los errores
    def updateBuffer(self):
        tries = 0
        maxTries = 20
        imageDownloaded = self.downloadImage(Util.getLastAvailableDate())

        # si no se pudo descargar la imagen, se intenta hasta que se descargue o se llegue al máximo de intentos
        while not imageDownloaded and tries != maxTries:
            imageDownloaded = self.downloadImage(Util.getLastAvailableDate(), self.satelite)
            Log.bufferFailedDownloadTry(tries + 1)
            tries += 1
            sleep(10)
        
        # si se llega al máximo de intentos, se da por vencido
        if tries == maxTries:
            Log.bufferGaveUp()
            return

        # si se descargó la imagen, se borra la más vieja del buffer (si es que hay más de 24 imágenes)
        toRemove = "None"
        if tries < maxTries:
            if len(os.listdir("buffer/" + self.satelite)) > 24:
                toRemove = self.satelite + "/" + os.listdir("buffer/" + self.satelite)[0]
                os.remove("buffer/" + toRemove)
            Log.bufferUpdated(imageDownloaded, toRemove)

    # TODO: decidir si se va a usar
    # def securityCheck(self): 
    #     bufferLen = len(os.listdir("buffer"))
        
    #     if bufferLen == 24:
    #         return True
        
    #     if bufferLen < 24:
    #         # updatea todo el buffer
    #         return False
            
    #     if bufferLen > 24:
    #         # borra las imagenes de más
    #         return False


# w1 = ImageManager("CEN")
# w1.downloadIntImages(24)

# w2 = ImageManager("ARG")
# w2.downloadIntImages(24)

# print(requests.get("https://estaticos.smn.gob.ar/vmsr/satelite/TOP_C13_ARG_ALTA_20230628_182020Z.jpg"))