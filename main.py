import os

from moviepy.editor import VideoFileClip, concatenate_videoclips

from gtts import gTTS

from urllib.request import urlretrieve

from PIL import Image, ImageDraw, ImageFont

# Load environment variables

API_KEY = os.getenv("API_KEY")

VIDEO_URL = os.getenv("VIDEO_URL")

BACKGROUND_IMAGE_URL = os.getenv("BACKGROUND_IMAGE_URL")

COMMENTS = os.getenv("COMMENTS")

def text_to_mp3():

    # Convert text to audio

    audio_clips = []

    for comment in COMMENTS.split(",")[:10]:

        tts = gTTS(comment, lang="en")

        tts.save("audio/{}.mp3".format(comment[:5]))

        audio_clips.append(VideoFileClip("audio/{}.mp3".format(comment[:5])))

    final_audio_clip = concatenate_videoclips(audio_clips)

    final_audio_clip.write_videofile("audio/final.mp4")

    return len(audio_clips), final_audio_clip.duration, len(audio_clips), ["image1.jpg", "image2.jpg", "image3.jpg"]

def download_background():

    # Download background image

    urlretrieve(BACKGROUND_IMAGE_URL, "background.jpg")

def create_text_image(text):

    # Create image with text

    img = Image.new('RGB', (1280, 720), color=(73, 109, 137))

    fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)

    d = ImageDraw.Draw(img)

    d.text((10, 10), text, font=fnt, fill=(255, 255, 0))

    return img

def final_video(num_comments, images):

    # Create final video

    video_clips = []

    for i in range(num_comments):

        img = Image.open(images[i % 3])

        text_img = create_text_image(COMMENTS.split(",")[i])

        img.paste(text_img, (0, 0))

        img.save("temp/{}.jpg".format(i))

        video_clip = VideoFileClip("temp/{}.jpg".format(i)).set_duration(5)

        video_clips.append(video_clip)

    final_clip = concatenate_videoclips(video_clips)

    background_clip = VideoFileClip("background.jpg").resize((1280, 720)).set_duration(final_clip.duration)

    final_clip = final_clip.set_position(("center", "center"))

    final_clip_with_background = concatenate_videoclips([background_clip, final_clip])

    final_clip_with_background.write_videofile("final_video.mp4")

    return final_clip_with_background

n, length, number_of_comments, final_images = text_to_mp3()

download_background()

final_video = final_video(number_of_comments, final_images)

