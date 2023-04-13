import os

import re

import webbrowser

import requests_html

import mwclient

from dotenv import load_dotenv

def get_fanobject():

    load_dotenv()

    site = mwclient.Site(os.getenv("WIKI"))

    page = site.pages[os.getenv("PROMPT")]

    content = {

        "body": [],

        "elements": 0,

    }

    for line in page.text().split("\n"):

        if not line.startswith("="):

            content["body"].append(line)

    if not os.getenv("INTRO") == "":

        content["body"].insert(0, os.getenv("INTRO"))

    content["elements"] = len(content["body"])

    return content

def get_pictures():

    load_dotenv()

    session = requests_html.HTMLSession()

    response = session.get(f"https://{os.getenv('WIKI')}/wiki/{os.getenv('PROMPT')}")

    response.html.render()

    images = []

    for image in response.html.find("img"):

        link = image.attrs.get("src", None) or image.attrs.get("data-src", None)

        if link and not link.startswith("data"):

            link = re.sub(r"\?.*", "", link)

            if link not in images:

                images.append(link)

    dir = "png/"

    for f in os.listdir(dir):

        os.remove(os.path.join(dir, f))

    for i, image in enumerate(images):

        response = requests.get(image)

        if response.status_code == 200:

            with open(f"png/{i}.jpg", "wb") as f:

                f.write(response.content)

    path = "png"

    webbrowser.open(path)

    chosen_pictures = input(

        "From the newly opened window, please choose the pictures you would like to use in the video and write them here in order, comma separated (e.g.: 0,3,4,6): "

    )

    chosen_pictures = chosen_pictures.split(",")

    final_images = [images[int(i)] for i in chosen_pictures]

    n = len(chosen_pictures)

    return n, chosen_pictures

