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

        satelites = ["CEN", "ARG"]
        generator = VideoGenerator()
        imagers = []
        for satelite in satelites:
            imagers.append(ImageManager(satelite))
        print("Running")
        sched = bs()
        for i in range(7, 58, 10):
            @sched.scheduled_job('cron', minute=str(i))
            def job():
                image_lists = []
                for imager in imagers:
                    imager.updateBuffer()
                    image_lists.append(imager.getImageList())

                generator.imagesToVideo(image_lists=image_lists)

        sched.start()

# Runner().run()
