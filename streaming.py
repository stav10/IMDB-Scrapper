import ffmpeg_streaming
from ffmpeg_streaming import Formats
import os


def create_m3u8(path, output_path):
    print(os.path.isfile(path))
    video = ffmpeg_streaming.input(path)
    hls = video.hls(Formats.h264())
    hls.auto_generate_representations()
    hls.output(f'{output_path}/hls.m3u8')



