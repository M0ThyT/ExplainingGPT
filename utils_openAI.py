import pandas as pd
import openai
import numpy as np

#doesn't work yet
def set_api_key(personal = True):
    """
    Sets the openAI the api key file.
    Choose between personal and professional api key.

    """
    base_path = "/Users/tim/Documents/DS projects/Open AI/API Keys/"
    if personal:
        path = base_path + "personal.txt"
    else:
        path = base_path + "css.txt"
    
    
    with open(path, "r") as f:
        api_key = f.read()
    
    #add key to openai
    openai.api_key = api_key
    #print("API key added")
    if personal:
        print("Personal API key added")
    else:
        print("CSS API key added")

    
    





