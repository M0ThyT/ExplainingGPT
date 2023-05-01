import pandas as pd
import openai
import numpy as np
import random
import re

#doesn't work yet
def get_api_key(personal = True):
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
    
    
    #print("API key added")
    if personal:
        print("Personal API key")
    else:
        print("CSS API key")
    return api_key



def create_condition(stimulus, explanations, key):
    '''Function that creates a list of list for the desired condition. 
    Conditions are: Without Neuro Science Short
                    Without Neuro Science Long
                    With Neuro Science Short
                    With Neuro Science Long
    Additionally, it also returns a list of booleans indicating whether the 
    good explanation was picked for each'''
    explanations_good = explanations[key + " Good"]
    explanations_bad = explanations[key + " Bad"]
    #create random list of booleans of length 3
    good_explanation_indication = random.choice([True, False])
    #generate random int between 0 and 2
    random_int = random.randint(0,2)
    stim = stimulus[random_int]

    #create empty list of lists
    list_of_1 = []
    #populate list with either good or bad explanations in condition

    #uf true add good explanation
    if good_explanation_indication:
        list_of_1.append([stim, explanations_good[random_int]])
    #else add bad explanation
    else:
        list_of_1.append([stim, explanations_bad[random_int]])

    
    return list_of_1, good_explanation_indication, random_int


def create_condition_multi(stimulus, explanations, key):
    '''Function that creates a list of list for the desired condition. 
    Conditions are: Without Neuro Science Short
                    Without Neuro Science Long
                    With Neuro Science Short
                    With Neuro Science Long
    Additionally, it also returns a list of booleans indicating whether the 
    good explanation was picked for each'''
    explanations_good = explanations[key + " Good"]
    explanations_bad = explanations[key + " Bad"]
    #create random list of booleans of length 3
    good_explanation_indication = [random.choice([True, False]) for i in range(3)]

    #create empty list of lists
    list_of_list = []
    #populate list with either good or bad explanations in condition
    for i in range(3):
        #uf true add good explanation
        if good_explanation_indication[i]:
            list_of_list.append([stimulus[i], explanations_good[i]])
        #else add bad explanation
        else:
            list_of_list.append([stimulus[i], explanations_bad[i]])

    
    return list_of_list, good_explanation_indication


def prompt_creator(stimulus_answer_list):
    '''Function that creates a prompt for the openAI API where all three scenarios with the right answer are included'''
    prompt = '#####Phenomenon#####: ' + stimulus_answer_list[0][0] +  ' #####Explanation#####: ' + stimulus_answer_list[0][1] + '\n'

    return prompt


def prompt_creator_multi(stimulus_answer_list):
    '''Function that creates a prompt for the openAI API where all three scenarios with the right answer are included'''
    prompt = '' #initialize prompt

    #loop over list
    for elm in stimulus_answer_list: 
        prompt = prompt + ' Phenomenon: ' + elm[0] +  ' Explanation: ' + elm[1] + '\n'

    return prompt[1:] #get rid of first empty space


def clean_output(x):
    '''Takes output of GPT as input and returns a list of 3 integers'''
    x = x.split(',')
    #take out all characters other than numbers and +,-
    for i in range(len(x)):
        x[i] = re.sub("[^0-9-+]", "", x[i])
    #convert to int
    for i in range(len(x)):
        x[i] = int(x[i])
    return x


