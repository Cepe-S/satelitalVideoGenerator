=== En el archivo configuration.json se encuentran las configuaciones del video ===

- fps: corresponden a la cantidad de frames por segundo que se desean en el mapa
- bitrate: corresponde a la calidad del video, a mayor bitrate mejor calidad pero mayor peso

- codec: corresponde al codec de video
- extension: corresponde a la extension del video (utilizar extensiones compatibles con el codec)

Extension	  ->  Codec
mp4	        ->  libx264 or mpeg4  ->  (tiene compresión)
avi         ->  rawvideo          ->  (no tiene compresión)
ogg	        ->  libvorbis    
webm	      ->  libvpx

- width: ancho del video
- height: alto del video
- mapResizeRatio: cuanto se reduce el tamaño del mapa para que entre en el video

- threads: cantidad de núcleos que se utilizan para la creación del video (si tarda mucho se puede aumentar)
