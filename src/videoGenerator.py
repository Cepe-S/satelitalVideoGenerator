import json
from moviepy.editor import ImageSequenceClip, CompositeVideoClip, concatenate
from moviepy.video import fx
import cv2
from typing import List

from log import Log


class VideoGenerator:

    def __init__(self):
        config = {}
        with open("configuration.json", "r") as file:
            config = json.load(file)
        self.fps = config['fps']
        self.bitrate = config['bitrate']
        self.codec = config['codec']
        self.width = config['width']
        self.height = config['height']
        self.mapResizeRatio = config['mapResizeRatio']
        self.extension = config['extension']
        self.threads = config['threads']
        self.background = "src/resources/background.jpg"
        self.duration = 1
    
    # def addProgressBar(self, sequence: ImageSequenceClip) -> ImageSequenceClip:
    #     return fx.all.sequence(sequence, [fx.all.time_mirror, fx.all.time_symmetrize])

    def generateImageSequence(self, image_list:List[str]) -> ImageSequenceClip:
        duration = 1 # TODO: ver como implementar esto

        images_len = len(image_list)

        sequence = ImageSequenceClip(image_list, durations=[duration] * images_len, fps=self.fps)
        # sequence = self.addProgressBar(sequence) TODO
        return sequence

    def joinSequences(self, video_list:List[ImageSequenceClip]) -> ImageSequenceClip:
        # sacando el método compose se modifica el tamaño de la segunda secuencia para igualarse
        return concatenate(video_list, method="compose") 



    def increase_fps_video(self, video_path: str, increased_fps: int) -> None:
        # Load the original video using OpenCV
        original_video = cv2.VideoCapture(video_path)

        # Get the original video's fps
        original_fps = original_video.get(cv2.CAP_PROP_FPS)

        # Create a VideoWriter for the increased fps video
        codec = cv2.VideoWriter_fourcc(*"mp4v")
        increased_fps_video = cv2.VideoWriter(video_path, codec, increased_fps,
                                            (int(original_video.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                            int(original_video.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        # Read and write each frame from the original video
        while original_video.isOpened():
            ret, frame = original_video.read()
            if not ret:
                break

            # Write the original frame to the increased fps video
            increased_fps_video.write(frame)

            # Create and write the fake frames
            fake_frames = int(increased_fps / original_fps) - 1
            for i in range(fake_frames):
                increased_fps_video.write(frame)

        # Release the resources
        original_video.release()
        increased_fps_video.release()

    def generateFinalVideo(self, sequence: ImageSequenceClip, total_frames: int, video_name: str):

        sequence.duration = total_frames 

        # crea el fondo como una secuencia de imágenes con la misma cantidad de frames que la secuencia de imágenes
        background_clip = ImageSequenceClip([self.background] * total_frames, durations=[self.duration] * total_frames, 
                                            fps=self.fps)
        
        # une el fondo con la secuencia de imágenes
        final_clip = CompositeVideoClip([background_clip, sequence], size=(self.width, self.height))

        Log.videoRenderingStarted()
        # renderiza el video
        final_clip.write_videofile(video_name + self.extension, audio=False, codec=self.codec, 
                                   bitrate=self.bitrate, threads=self.threads)
        Log.videoUpdated()

    # globaliza todas las funciones
    def imagesToVideo(self, image_lists: List[List[str]], repeats: int):
        # devuelve la cantidad de frames totales sumando la cantidad de imágenes
        total_frames = sum(len(sublista) for sublista in image_lists) * repeats

        sequences = []
        # genera una secuencia de imágenes para cada satélite y las guarda en una lista
        for image_list in image_lists:
            image_sequence = self.generateImageSequence(image_list)
            for _ in range(repeats):
                sequences.append(image_sequence)

        # une todas las secuencias de imágenes de los distintos satélites
        final_sequence = self.joinSequences(sequences)

        # centra la secuencia de imágenes y lo hace mas chico
        final_sequence = final_sequence.set_position(("center", "center"))
        final_sequence = final_sequence.resize(self.mapResizeRatio)

        self.generateFinalVideo(final_sequence, total_frames, "video")



# from imageManager import ImageManager

# v = VideoGenerator()
# iARG = ImageManager(satelite="ARG")
# iCEN = ImageManager(satelite="CEN")

# v.imagesToVideo([iARG.getImageList(), iCEN.getImageList()], 2)
# v.increase_fps_video("video.mp4", 30)