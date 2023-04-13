# Tarano-video-
1. Fan.py:-
 
 Python script that uses the Wikipedia API to fetch content and images related to a fandom page. The get_fanobject function fetches the content of the page, filters out unnecessary lines at the beginning, and splits the remaining content into a list of sentences. It also allows the user to add an introduction to the content. The get_pictures function fetches the images related to the page, filters them to include only JPG and PNG files, and prompts the user to select the images they would like to use in the video. The function returns the number of selected images and their indices in the original list of images. Both functions use the os module to fetch environment variables with the title of the fandom page and the introduction to the content. The script also uses the requests and json modules to make API requests and parse the response. The webbrowser module is imported but not used in the script.

2.Finalvideo.py:-

 a Python script that creates a video by combining multiple image and audio clips. Here is an overview of what the script does:

It sets up the dimensions of the video and imports necessary libraries.
It opens a background video clip and crops it to the desired dimensions.
It loads audio clips and adds 0.5 seconds of silence between each clip.
It concatenates all the audio clips and fades them in and out.
It adds the concatenated audio to the background video clip.
It loads and prepares the first image to be displayed in the video.
It creates an image with the title of the video and appends it to the list of image clips.
For each remaining image clip, it loads the image, resizes it, and appends it to the list of image clips.
It concatenates all the image clips and centers them on the background video clip.
It creates the final video by overlaying the image and audio clips onto the background video clip and exporting it.
