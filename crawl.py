import requests
import re
import urllib.request
from bs4 import BeautifulSoup
from collections import deque
from html.parser import HTMLParser
from urllib.parse import urlparse
import os
import pandas as pd
import tiktoken
import numpy as np

#from openai.embeddings_utils import distances_from_embeddings, cosine_similarity

def crawl(url):
    # Parse the URL and get the domain
    local_domain = urlparse(url).netloc

    if not os.path.exists("text/"):
            os.mkdir("text/")

    #if not os.path.exists("text/"+local_domain+"/"):
    #        os.mkdir("text/" + local_domain + "/")

    # Create a directory to store the csv files
    if not os.path.exists("processed"):
            os.mkdir("processed")

    # Replace any special characters in the path with underscores
    cut_url = url[8:]
    path = cut_url.split("/")[-1]
    if len(path)> 25:
          path = path[:25]
    file_path= re.sub(r'[^\w\s-]', '-', path)
    # Construct the full file name with the directory and file extension
    file_name = f"text/{local_domain+file_path}.txt"
    print(url)
    with open(file_name, "w", encoding="UTF-8") as f:

        # Get the text from the URL using BeautifulSoup
        try:
              
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
        except:
            print("Unable to parse page " + url + " due to an error")
            return

        # Get the text but remove the tags
        text = soup.get_text()
        text += "\n URL of this webpage is: " + url

        # If the crawler gets to a page that requires JavaScript, it will stop the crawl
        if ("You need to enable JavaScript to run this app." in text):
            print("Unable to parse page " + url + " due to JavaScript being required")
        
        # Otherwise, write the text to the file in the text directory
        f.write(text)
        

df = pd.read_csv("history.csv")
urls = list(df["url"])
for index, url in enumerate(urls):
    crawl(url)
    print(index, "******************************************")
    if index == 100:
         break