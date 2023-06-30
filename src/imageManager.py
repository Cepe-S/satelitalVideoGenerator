import os
from time import sleep
import requests
import datetime
from typing import List

from link import Link
from log import Log
from utilities import Util
# se encarga de obtener las imagenes del satelite

bestTryOrder = [21, 19, 22, 18, 23, 17, 24, 16, 25, 32, 15, 31, 14, 30, 13, 29, 12, 28, 11, 27, 10, 26, 9, 8, 7, 6, 5, 4, 3, 2, 1]

class ImageManager:

    def __init__(self):
        pass
    
    def downloadImage(self, date: datetime.datetime) -> str:
        
        # se crea el link y se le agrega la fecha
        link = Link()
        link.setDate(Util.roundTime(date))
        
        # si la imagen ya se encuentra en el buffer, no se descarga
        if link.getFilename() in os.listdir("buffer"):
            # TODO: solucionar el problema de que se descargue la misma imagen dos veces cuando los segundos no terminan en 20
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
            # se verifica que exista el directorio buffer
            if not os.path.exists("buffer"):
                os.makedirs("buffer")
            
            # se genera el nombre del archivo
            filename = link.getFilename()
            with open("buffer/" + filename, 'wb') as f:
                f.write(request.content)
                f.close()
                
            Log.imageDownloaded(filename)
            return filename
        
        # control de errores
        if request.status_code == 404:
            Log.imageNotFound(link.getFinalLink())
            return None
        
        if request.status_code == 403:
            Log.forbiddenAccess(link.getFinalLink())
            return None
        
        # si empieza en 5 es un error del servidor del servicio meteorológico
        if str(request.status_code)[0] == "5":
            Log.externalServerError(link.getFinalLink(), request.status_code)
            return None

        # de lo contrario
        if request.status_code not in [200, 404, 403, 500, 501, 502, 503, 504]:
            Log.unmanagedImageError(link.getFinalLink(), request.status_code)
            return None


    def downloadIntImages(self, amount:int):
        dates = Util.generateDates(amount)

        if not os.path.exists("buffer"):
            os.makedirs("buffer")

        for date in dates:
            self.downloadImage(date)

    def generateImageList(self, hours:int) -> List[str]:
        return 

    def updateBuffer(self):
        tries = 0
        maxTries = 20
        imageDownloaded = self.downloadImage(Util.getLastAvailableDate())

        # si no se pudo descargar la imagen, se intenta hasta que se descargue o se llegue al máximo de intentos
        while not imageDownloaded and tries != maxTries:
            imageDownloaded = self.downloadImage(Util.getLastAvailableDate())
            Log.bufferFailedDownloadTry(tries + 1)
            tries += 1
            sleep(10)
        
        # si se llega al máximo de intentos, se da por vencido
        if tries == maxTries:
            Log.bufferGaveUp()
            return

        # si se descargó la imagen, se borra la más vieja del buffer
        if tries < maxTries:
            toRemove = "buffer/" + os.listdir("buffer")[0]
            os.remove(toRemove)
            Log.bufferUpdated(imageDownloaded, toRemove)

    # TODO: decidir si se va a usar
    def securityCheck(self): 
        bufferLen = len(os.listdir("buffer"))
        
        if bufferLen == 24:
            return True
        
        if bufferLen < 24:
            # updatea todo el buffer
            return False
            
        if bufferLen > 24:
            # borra las imagenes de más
            return False


# w = ImageManager()
# w.getFromLastHours(5)
# print(w.generateImageList(5))
# print(requests.get("https://estaticos.smn.gob.ar/vmsr/satelite/TOP_C13_ARG_ALTA_20230628_182020Z.jpg"))