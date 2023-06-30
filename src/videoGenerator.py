from moviepy.editor import ImageSequenceClip
from typing import List

class VideoGenerator:

    def __init__(self):
        pass

    def generate(self, image_list:List[str], video_name:str):
        clip = ImageSequenceClip(image_list, fps=1)
        clip.write_videofile(video_name + ".mp4", audio=False, codec="mpeg4", bitrate="5000k")
