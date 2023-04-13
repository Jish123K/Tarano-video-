import os

import pathlib

import subprocess

import tempfile

import urllib.parse

import requests

from dotenv import load_dotenv

from PIL import Image

from mutagen.mp3 import MP3

def text_to_mp3():

    print("Welcome to TheHudek's FandomVideoGenerator")

    load_dotenv()

    length_limit = float(os.getenv("LENGHT"))

    png_dir = pathlib.Path("png")

    mp3_dir = pathlib.Path("mp3")

    png_dir.mkdir(exist_ok=True)

    mp3_dir.mkdir(exist_ok=True)

    images = []

    prompts = []

    fanobject = get_fanobject()

    for i, prompt in enumerate(fanobject["body"]):

        if i >= len(get_pictures()[1]) or sum(image.duration for image in images) > length_limit:

            break

        print(f"Printing {i}/{len(fanobject['body'])}, which is {prompt}")

        # Generate PNG image using Pillow

        image_path = png_dir / f"{i}.png"

        with Image.new("RGBA", (1280, 720), (255, 255, 255, 255)) as img:

            img.show()

            img.save(str(image_path), "PNG")

        # Generate MP3 using subprocess and Google Text-to-Speech API

        with tempfile.NamedTemporaryFile(suffix=".mp3") as f:

            text = urllib.parse.quote(prompt)

            subprocess.run(

                [

                    "curl",

                    "-o",

                    f.name,

                    "-G",

                    "--data-urlencode",

                    f"q={text}",

                    "-H",

                    "Content-Type: application/json",

                    "-H",

                    f"Authorization: Bearer {os.getenv('GOOGLE_CLOUD_TOKEN')}",

                    "https://texttospeech.googleapis.com/v1/text:synthesize",

                ],

                check=True,

            )

            mp3_path = mp3_dir / f"{i}.mp3"

            mp3_path.write_bytes(f.read())

        # Add generated image and MP3 to lists

        images.append(Image.open(image_path))

        prompts.append(mp3_path)

    total_length = sum(MP3(prompt).info.length for prompt in prompts)

    print(f"Pictures: {len(images)}, Length: {total_length}, Prompts: {len(prompts)}")

    return len(images), total_length, len(prompts), images

