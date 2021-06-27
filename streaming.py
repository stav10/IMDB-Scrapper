import ffmpeg_streaming
from ffmpeg_streaming import Formats, Bitrate, Representation, Size
import os
import time

# _480p = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
# _720p = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
# _1080p = Representation(Size(1920, 1080), Bitrate(4096 * 1024, 320 * 1024))


def create_m3u8(path, output_path):
    print(path)
    start_time = time.time()
    video = ffmpeg_streaming.input(path)
    hls = video.hls(Formats.h264())
    hls.auto_generate_representations()
    hls.output(f'{output_path}/hls.m3u8')
    print(time.time() - start_time)



