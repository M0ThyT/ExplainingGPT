import pandas as pd
import numpy as np

def get_api_key(personal = True):
    """
    Returns the path to the api key file.
    Choose between personal and professional api key.

    """
    base_path = "/Users/tim/Documents/DS projects/Open AI/API Keys/"
    if personal:
        path = base_path + "personal.txt"
    else:
        path = base_path + "css.txt"
    
    print(path)
    with open(path, "r") as f:
        api_key = f.read()

    
    return api_key





