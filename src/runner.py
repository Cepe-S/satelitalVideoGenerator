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

        imager = ImageManager()
        generator = VideoGenerator()
        print("Running")
        sched = bs()
        for i in range(7, 58, 10):
            @sched.scheduled_job('cron', minute=str(i))
            def job():
                imager.updateBuffer()
                generator.generate(image_list=[os.path.join("buffer", archivo) for archivo in os.listdir("buffer")], video_name="video")

        sched.start()

# Runner().run()
