from datetime import datetime
from typing import List

def getDate() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class Log:

    codes = {0: "success", 1: "warning", 2: "error"}
    log_file = "log.txt"

    def __init__(self):
        pass

    def write(message: str, code: int):
        with open(Log.log_file, 'a') as file:
            file.write(f"{getDate()} [{Log.codes[code]}] {message}\n")


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


    def shutdown():
        Log.write("Runner shutdown", 0)

