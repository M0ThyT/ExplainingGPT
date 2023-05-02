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

#################################Functions experiment 2#############################################
def make_condition_exp2(stimulus, explanations_s2):
    '''
    Function that creates the condition and collects the data for the experiment.
    Returns a list where teh first element is the stimulus, the second the good explanation, and the third the bad explanation.
    also returns the condition and the number of the stimulus and whether the good explanation should be first or not
    '''
    #Conditions
    possible_conditions = ['With', 'Without', 'Mixed']
    #pick one random condition
    condition = random.choice(possible_conditions)

    #pick number from 0 - 2
    num_stimulus = random.randint(0,2)

    #pick boolean of whether the good explanation is first or not
    good_first = random.choice([True, False])

    #make a list with 1) stimulus 2) good explanation 3) bad explanation
    if condition == 'With':
        condition_list = [stimulus[num_stimulus], explanations_s2['With Neuroscience Short Good'][num_stimulus], explanations_s2['With Neuroscience Short Bad'][num_stimulus]]
    elif condition == 'Without':
        condition_list = [stimulus[num_stimulus], explanations_s2['Without Neuroscience Short Good'][num_stimulus], explanations_s2['Without Neuroscience Short Bad'][num_stimulus]]
    elif condition == 'Mixed':
        condition_list = [stimulus[num_stimulus], explanations_s2['Without Neuroscience Short Good'][num_stimulus], explanations_s2['With Neuroscience Short Bad'][num_stimulus]]
    else:
        print('Error: condition not found')

    return condition_list, condition, num_stimulus, good_first


def create_prompt_exp2(condition_list, good_first):
    '''
    Takes as input the condition list and whether the good explanation should be first or not.
    This is the output from make_condition_exp2. Retunrs a prompt as a string ready to be fead to GPT
    '''
    #prompt always starts with phenomenon
    prompt = '#####Phenomenon#####:\n' + condition_list[0] + '\n#####Explanation 1#####:\n'
    #then check and add whether good or bad explanation comes first
    if good_first:
        prompt = prompt + condition_list[1] + '\n#####Explanation 2#####:\n' + condition_list[2]
    else:
        prompt = prompt + condition_list[2] + '\n#####Explanation 2#####:\n' + condition_list[1]
    
    return prompt


#################################Functions experiment 3#############################################
def make_condition_exp3(stimulus, explanations):
    '''
    Creates the condition for experiment 3, and returns the chosen stimulus, explanation, condition, and whether the explanation is good or bad
    whether the explanation contains jargon or not, and whether the explanation contains neuro science or not, and what stimulus number was chosen
    '''
    #create condition
    conditions = ['Simple Neuro Science Good', 'Simple Neuro Science Bad', 'Neuro Science and Jargon Good', 'Neuro Science and Jargon Bad', 'Without Neuro Science Good', 'Without Neuro Science Bad']
    condition = random.choice(conditions)

    #create neuro science, jargon and good variable
    #if the split condition is equal to Good, then the good_bad variable is 1, else it is 0
    if condition == 'Simple Neuro Science Good' or condition == 'Neuro Science and Jargon Good' or condition == 'Without Neuro Science Good':
        answer_good = 1
    else:
        answer_good = 0

    ##jargon
    if condition == 'Neuro Science and Jargon Good' or condition == 'Neuro Science and Jargon Bad':
        jargon = 1
    else:
        jargon = 0

    #neuro science
    if condition == 'Simple Neuro Science Good' or condition == 'Simple Neuro Science Bad' or condition == 'Neuro Science and Jargon Good' or condition == 'Neuro Science and Jargon Bad':
        neuro = 1
    else:
        neuro = 0

    #generate a random number between 0 and 2
    stimulus_number = random.randint(0,2)

    #get relevant material
    stimulus_x = stimulus[stimulus_number]
    explanation_x = explanations[condition][stimulus_number]


    return stimulus_x, explanation_x, condition, answer_good, jargon, neuro, stimulus_number


def create_prompt_exp3(stimulus_x, explanation_x):
    '''
    Creates Prompt for GPT input for experiment 3
    '''
    #prompt always starts with phenomenon
    prompt = '#####Phenomenon#####: ' + stimulus_x  + ' #####Explanation#####: ' + explanation_x 

   
    return prompt