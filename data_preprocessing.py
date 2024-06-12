# Import Libraries
import pandas as pd
import numpy as np
import json
import re
import os
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')


######################################### HELPER FUNCTIONS #########################################
def read_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
                return data
            except json.JSONDecodeError:
                print("Error: File contains invalid JSON.")
                return None
    else:
        print(f"Error: File {file_path} does not exist.")
        return None

def print_json(data):
    if data is not None:
        print(json.dumps(data, indent=4))
    else:
        print("No data to print.")

# Function to remove stopwords
def remove_stopwords(text):
    if not isinstance(text, str):
        return text  # Return text that is not string
    words = text.split()  # Split text into words
    filtered_words = [word for word in words if word.lower() not in stop_words]  # Remove stopwords
    return ' '.join(filtered_words)  # Join the words back into text

# Function remove punctuation (.&,)
def remove_punctuation(text):
    # Remove punctuation and replace it with space
    cleaned_text = re.sub(r'[.,]', ' ', text)
    # Remove any double spaces that may have been created
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text


def remove_non_alpha(text):
    # Function to substitute ordinal numbers back into text
    cleaned_text = re.sub(r'\b1st\b', 'first', text)
    cleaned_text = re.sub(r'\b2nd\b', 'second', cleaned_text)
    cleaned_text = re.sub(r'\b3rd\b', 'third', cleaned_text)
    cleaned_text = re.sub(r'\b1\b', 'one', cleaned_text)
    cleaned_text = re.sub(r'\b2\b', 'two', cleaned_text)
    cleaned_text = re.sub(r'\b3\b', 'three', cleaned_text)
    cleaned_text = re.sub(r'\b4\b', 'four', cleaned_text)
    cleaned_text = re.sub(r'\b5\b', 'five', cleaned_text)
    cleaned_text = re.sub(r'\b6\b', 'six', cleaned_text)
    cleaned_text = re.sub(r'\b7\b', 'seven', cleaned_text)
    cleaned_text = re.sub(r'\b8\b', 'eight', cleaned_text)
    cleaned_text = re.sub(r'\b9\b', 'nine', cleaned_text)
    cleaned_text = re.sub(r'\b10\b', 'ten', cleaned_text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    # Function to remove characters other than letters and spaces
    cleaned_text = re.sub(r'[^a-zA-Z\s]', '', cleaned_text)
    return cleaned_text

# Replacement dictionary
replacements = {
    r'\bcg\b': 'capgemini',
    r'\bnanipulstive\b':'manipulative',
    r'\bharashful\b':'harshful',
    r'\bcanspeak\b':'can speak',
    r'\bsallery\b':'salary',
    r'\bemloyees\b':'employees',
    r'\bharashment\b':'harassment',
    r'\bsallery\b':'salary',

}

# Function to replace words according to a replacement list
def replace_words(text, replacements):
    for old_word, new_word in replacements.items():
        text = re.sub(old_word, new_word, text)
    return text

## -- LEMMATIZATION -- ##
def custom_lemmatization(text, exclude_words=[]):
    lemmatizer = WordNetLemmatizer()
    words = text.split()
    lemmatized_words = [lemmatizer.lemmatize(word) if word.lower() not in exclude_words else word for word in words]
    lemmatized_text = ' '.join(lemmatized_words)
    return lemmatized_text

######################################### START DATA PREPROCESSING #########################################

def processing(file_path):
    ## DATA READ AND CONVERSION TO DATAFRAME ##
    # Example usage
    data = read_json(file_path)

    # Normalize the nested JSON
    df = pd.json_normalize(data['content'])

    ## DATA PREPROCESSING ##
    ## -- LOWERCASE -- ##
    df_processed = df.copy()
    df_processed['user_responses_cleaned'] = df['content'].apply(lambda x: x.lower() if isinstance(x, str) else x)

    ## -- STOP WORDS -- ##
    stop_words = set(stopwords.words('english'))
    df_processed['user_responses_cleaned'] = df_processed['content'].astype(str).apply(remove_stopwords)

    ## -- REMOVE PUNCTUATION -- ##
    df_processed['user_responses_cleaned'] = df_processed['content'].apply(remove_punctuation)


    ## -- REMOVE OTHER PUNCTUATION -- ##
    df_processed['user_responses_cleaned'] = df_processed['content'].apply(remove_non_alpha)

    ## -- SLANG WORDS -- ##
    df_processed['user_responses_cleaned'] = df_processed['content'].apply(lambda x: replace_words(x, replacements))

    ## -- LEMMATIZATOIN -- ##
    df_processed['user_responses_cleaned'] = df_processed['content'].apply(custom_lemmatization)
    
    return df_processed