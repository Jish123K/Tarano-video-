# Tarano-video-
 Fan.py:-
 
 Python script that uses the Wikipedia API to fetch content and images related to a fandom page. The get_fanobject function fetches the content of the page, filters out unnecessary lines at the beginning, and splits the remaining content into a list of sentences. It also allows the user to add an introduction to the content. The get_pictures function fetches the images related to the page, filters them to include only JPG and PNG files, and prompts the user to select the images they would like to use in the video. The function returns the number of selected images and their indices in the original list of images. Both functions use the os module to fetch environment variables with the title of the fandom page and the introduction to the content. The script also uses the requests and json modules to make API requests and parse the response. The webbrowser module is imported but not used in the script.

