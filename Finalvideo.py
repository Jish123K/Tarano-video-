import cv2

import numpy as np

import os

import math

from pydub import AudioSegment

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

def final_video(number_of_clips, final_images):

    length: int = 0

    background_clip = cv2.VideoCapture("clip.mp4")

    background_clip.set(cv2.CAP_PROP_POS_FRAMES, 100) # Crop the video

    background_clip = background_clip.read()[1][:, 1167:2247]

    audio_clips = []

    silence = AudioSegment.silent(duration=500) # 0.5 sec silence

    for i in range(0, number_of_clips):

        audio_clips.append(AudioSegment.from_file(f"mp3/{i}.mp3"))

        length += audio_clips[-1].duration_seconds

        audio_clips.append(silence)

        length += silence.duration_seconds

    audio_concat = AudioSegment.empty()

    for audio in audio_clips:

        audio_concat += audio

    audio = AudioSegment.from_file("audio.mp3")

    start_time, end_time = get_start_and_end_times(

        length, audio.duration_seconds)

    audio = audio[start_time*1000:end_time*1000].fade(to_gain=-40.0, start=0, end=100) # Fade in and out

    audio = audio.overlay(audio_concat)

    audio.export("clip_audio.mp3", format="mp3", bitrate="192k")

    image_clips = []

    print(f"Appending title.png")

    firstimg = Image.open(f"png/{final_images[0]}.jpg")

    nsize: list = list(firstimg.size)

    nsize[1] = int(nsize[1]*1.2)

    width, height = tuple(nsize)

    nsize = math.prod((width, height))

    img = Image.new("RGBA", (width, height), color="white")

    font_url = "https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Black.ttf?raw=true"

    font_size = int(width/len((os.getenv("PROMPT")).replace("_", " ")))

    with requests.get(font_url, allow_redirects=True) as r:

        subtitle_font = ImageFont.truetype(io.BytesIO(r.content), size=font_size)

    img.putalpha(0)

    img.paste(firstimg, (0, int(height-height/1.2)))

    draw = ImageDraw.Draw(img)

    title = (os.getenv("PROMPT")).replace("_", " ")

    _, _, w, h = draw.textbbox((0, 0), title, font=subtitle_font)

    draw.text(((width-w)/2, ((height/2)-((height/2)/1.2))), title, font=subtitle_font,

              stroke_width=2, fill="white", stroke_fill="black")

    img.save("png/title.png")

    img.close()

    firstimg.close()

    image_clips.append(

        cv2.cvtColor(np.array(Image.open(f"png/title.png")), cv2.COLOR_RGB2BGR)

        .resize((W - 75, H))

        .set_duration(audio_clips[0].duration_seconds+0.5)

        .set_pos("center")

    )

    del final_images[0]

    print(final_images)

    k: int = 2

    for i in range(0, number_of_clips-1):

        if os.path.exists(f"png/{final_images[i]
].jpg") and not os.path.exists(f"png/{final_images[i]}.png"):

im = Image.open(f"png/{final_images[i]}.jpg")

im.save(f"png/{final_images[i]}.png")

image_clips.append(

ImageClip(f"png/{final_images[i]}.png")

.set_duration(audio_clips[k].duration+audio_clips[k+1].duration)

.set_position("center")

.resize(width=W - 75)

)

im.close()

print(

f"Appending Image {final_images[i]} with lenght {audio_clips[k].duration} and {audio_clips[k+1].duration}")

k += 2

image_concat = concatenate_videoclips(

image_clips, method="compose").set_position(("center", "center"))

image_concat.audio = AudioFileClip("clip_audio.mp3")

final = CompositeVideoClip(

[background_clip, image_concat])

final.write_videofile("final.mp4", fps=30, ffmpeg_params=[

"-vcodec", "h264_nvenc"], audio_codec="aac", audio_bitrate="192k")

final.close()
