import os

import random

from dotenv import load_dotenv

from pathlib import Path

from pytube import YouTube

from moviepy.editor import VideoFileClip

from moviepy.video.fx.all import crop

def download_video(link, filename):

    if not os.path.exists(filename):

        YouTube(link).streams.filter(res="720p").first().download(filename=filename)

def download_audio(link, filename):

    if not os.path.exists(filename):

        YouTube(link).streams.filter(only_audio=True).first().download(filename=filename)

def get_start_and_end_times(video_length, clip_length):

    start_time = random.uniform(0, clip_length - video_length)

    end_time = start_time + video_length

    return start_time, end_time

def chop_video(video_length):

    load_dotenv()

    download_video(os.getenv("BACKGROUND_LINK"), "background.mp4")

    download_audio(os.getenv("AUDIO_LINK"), "audio.mp3")

    clip_duration = VideoFileClip("background.mp4").duration

    start_time, end_time = get_start_and_end_times(video_length, clip_duration)

    

    clip = VideoFileClip("background.mp4").subclip(start_time, end_time)

    cropped_clip = crop(clip, width=1280, height=720, x_center=640, y_center=360)

    cropped_clip.write_videofile("clip.mp4", fps=30)

    os.system(f"ffmpeg -i audio.mp3 -ss {start_time} -to {end_time} -c copy audio_clip.mp3")

if __name__ == "__main__":

    chop_video(10)

