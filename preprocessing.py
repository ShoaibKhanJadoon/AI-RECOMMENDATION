import pandas as pd
from data_fetching import Fetch_Data 
import spacy
from spacy.lang.en.stop_words import STOP_WORDS

nlp = spacy.load("en_core_web_sm")
data=Fetch_Data()

def clean_and_extract_tags(text):
    doc = nlp(text.lower())
    tags = [token.text for token in doc if token.text.isalnum() and token.text not in STOP_WORDS]
    return ', '.join(tags)

def get_processed_data():
    global data 
    df = pd.json_normalize(data)

    columns_to_extract_tags_from = ['name', 'category.name', 'description', 'color.name', 'size.name']
    
    for column in columns_to_extract_tags_from:
        df[column] = df[column].apply(clean_and_extract_tags)

    df['tags'] = df[columns_to_extract_tags_from].apply(lambda row: ', '.join(row), axis=1)

    return df  # Return the processed DataFrame



