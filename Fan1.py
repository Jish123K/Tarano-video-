import wikipedia

import requests

import json

import os

from dotenv import load_dotenv

import webbrowser

def get_fanobject():

    load_dotenv()

    content = {}

    fanobject_chosen = wikipedia.page(title=os.getenv("PROMPT"))

    fanobject_body = fanobject_chosen.content

    fanobject_body_split = fanobject_body.split("\n")

    del fanobject_body_split[0]

    if len(fanobject_body_split) < 40:

        j = fanobject_body_split

    else:

        j = fanobject_body_split[:40]

    for i in range(len(j)):

        print(f"{i}: {fanobject_body_split[i]}")

    unnecesary = input(

        "Please provide the number of the unnecessary lines in the beginning: ")

    if not unnecesary == "":

        unnecesary = unnecesary.split(",")

        unnecesary = [int(x) for x in unnecesary]

        for i in range(len(unnecesary)):

            del j[int(unnecesary[i])]

            unnecesary = [x-1 for x in unnecesary]

    j = " ".join(j)

    j = j.split('. ')

    del j[len(j)-1]

    if not os.getenv("INTRO") == "":

        j.insert(0, os.getenv("INTRO"))

    for i in range(len(j)):

        print(f"{i}: {j[i]}")

    try:

        content["body"] = j

        content["elements"] = len(j)

    except AttributeError as e:

        pass

    return content

def get_pictures():

    load_dotenv()

    fanobject_chosen = wikipedia.page(title=os.getenv("PROMPT"))

    # get page ID for API requests

    page_id = fanobject_chosen.pageid

    # make API request for page images

    api_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=images&pageids={page_id}"

    response = requests.get(api_url)

    data = json.loads(response.text)

    image_info = data["query"]["pages"][str(page_id)]["images"]

    

    # filter image URLs to only include JPG and PNG files

    images = []

    for image in image_info:

        if image["title"].lower().endswith(".jpg") or image["title"].lower().endswith(".png"):

            images.append(image["title"])

    if len(images) < 40:

        j = images

    else:

        j = images[:40]

    

    for i in range(len(j)):

        print(f"{i}: {j[i]}")

    chosen_pictures = input(

        f"Please choose the pictures you would like to use in the video and write their numbers here, comma separated (e.g.: 0,3,4,6): ")

    chosen_pictures = chosen_pictures.split(",")

    final_images = []

    for i in range(len(chosen_pictures)):

        final_images.append(images[int(chosen_pictures[i])])

    n = len(chosen_pictures)

    return n, chosen_pictures

