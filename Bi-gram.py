#name = payam amanat

import pandas as pd
import numpy as np
from collections import defaultdict
import re 

# import mikonim dataset
df = pd.read_csv('esme file.txt')

#age bekhaim clean konim va emoji delete konim 
def clean_emoji(tx):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols 
                           u"\U0001F680-\U0001F6FF"  # transport 
                           u"\U0001F1E0-\U0001F1FF"  # flags 
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    
    return emoji_pattern.sub(r'', tx)
def text_cleaner(tx):
    
    text = re.sub(r"won\'t", "would not", tx)
    text = re.sub(r"im", "i am", tx)
    text = re.sub(r"Im", "I am", tx)
    text = re.sub(r"can\'t", "can not", text)
    text = re.sub(r"don\'t", "do not", text)
    text = re.sub(r"shouldn\'t", "should not", text)
    text = re.sub(r"needn\'t", "need not", text)
    text = re.sub(r"hasn\'t", "has not", text)
    text = re.sub(r"haven\'t", "have not", text)
    text = re.sub(r"weren\'t", "were not", text)
    text = re.sub(r"mightn\'t", "might not", text)
    text = re.sub(r"didn\'t", "did not", text)
    text = re.sub(r"n\'t", " not", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'s", " is", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'t", " not", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'m", " am", text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub(r'[^a-zA-Z0-9\!\?\.\@]',' ' , text)
    text = re.sub(r'[!]+' , '!' , text)
    text = re.sub(r'[?]+' , '?' , text)
    text = re.sub(r'[.]+' , '.' , text)
    text = re.sub(r'[@]+' , '@' , text)
    text = re.sub(r'unk' , ' ' , text)
    text = re.sub('\n', '', text)
    text = text.lower()
    text = re.sub(r'[ ]+' , ' ' , text)
    
    return text


def build_conditional_probabilities(corpus):


	tokenized_string = corpus.split()
	previous_word = ""
	dictionnary = defaultdict(list)

	for current_word in tokenized_string:
		if previous_word != "":
			dictionnary[previous_word].append(current_word)
		previous_word = current_word
		


	for key in dictionnary.keys():
		next_words = dictionnary[key]
		unique_words = set(next_words) # removes duplicated
		nb_words = len(next_words)
		probabilities_given_key = {}
		for unique_word in unique_words:
			probabilities_given_key[unique_word] = \
				float(next_words.count(unique_word)) / nb_words
		dictionnary[key] = probabilities_given_key

	return dictionnary


def bigram_next_word_predictor(conditional_probabilities, current, next_candidate):

	if conditional_probabilities.has_key(current):
		if conditional_probabilities[current].has_key(next_candidate):
			return conditional_probabilities[current][next_candidate]


	return 0.0
#Har matni bekhaim inja test mikonim
corpus = " For example , how old are "


conditional_probabilities = build_conditional_probabilities(corpus)

#be first and second mitonim har 2 kalame ro pishbini konim 
assert bigram_next_word_predictor(conditional_probabilities, "first word", "second word") == 0.75
assert bigram_next_word_predictor(conditional_probabilities, "first word", "second word") == 0.25
assert bigram_next_word_predictor(conditional_probabilities, "fisrt word", "second word") == 0.0