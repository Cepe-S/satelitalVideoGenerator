import os
from apscheduler.schedulers.blocking import BlockingScheduler as bs

from log import Log
from imageManager import ImageManager
from videoGenerator import VideoGenerator

class Runner:

    def __init__(self) -> None:
        Log.runnerStarted()
        pass

    def run(self) -> None:

        # crea el imageManager para cada satélite
        satelites = ["ARG", "CEN"] # en el orden en el que estarán en el video
        imagers = [ImageManager(i) for i in satelites]

        generator = VideoGenerator()

        print("Running")

        sched = bs()
        for i in range(7, 58, 10):
            @sched.scheduled_job('cron', minute=str(i))
            def job():
                image_lists = []
                for imager in imagers:
                    imager.updateBuffer()
                    image_lists.append(imager.getImageList())

                generator.imagesToVideo(image_lists, 2)

        sched.start()

# Runner().run()
