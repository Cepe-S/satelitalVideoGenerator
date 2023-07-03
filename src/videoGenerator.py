import json
from moviepy.editor import ImageSequenceClip, CompositeVideoClip, concatenate
from moviepy.video import fx
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

        # crea con video con las imágenes
        images_len = len(image_list)

        sequence = ImageSequenceClip(image_list, durations=[duration] * images_len, fps=self.fps)
        # sequence = self.addProgressBar(sequence) TODO
        return sequence


    def joinSequences(self, video_list:List[ImageSequenceClip]) -> ImageSequenceClip:
        return concatenate(video_list)

    def generateFinalVideo(self, sequence: ImageSequenceClip, total_frames: int, video_name: str):
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
    def imagesToVideo(self, image_lists: List[List[str]]):
        sequences = []

        # devuelve la cantidad de frames totales sumando la cantidad de imágenes
        total_frames = sum(len(sublista) for sublista in image_lists)

        for image_list in image_lists:
            sequences.append(self.generateImageSequence(image_list))

        final_sequence = self.joinSequences(sequences)

        final_sequence = final_sequence.set_position(("center", "center"))
        final_sequence = final_sequence.resize(self.mapResizeRatio)

        self.generateFinalVideo(final_sequence, total_frames, "video")



# from imageManager import ImageManager

# v = VideoGenerator()
# iARG = ImageManager(satelite="ARG")
# iCEN = ImageManager(satelite="CEN")

# v.imagesToVideo([iARG.getImageList(), iCEN.getImageList()])

        

        # centra la secuencia de imágenes y lo hace mas chico

        # fusiona el video con el fondo # TODO: el fondo no es de 1920x1080        
    
        # final_clip = CompositeVideoClip([background_clip, image_sequence], size=background_clip.size)