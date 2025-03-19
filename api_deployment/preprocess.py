
import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import joblib
import pickle


def clean_preprocess(text,date_source_text,name_text):
    cleaned_text = clean_text(text)
    date = extract_date(date_source_text)
    source = extract_source(date_source_text)

    ## Flatten Mapping 
    with open('category_mapping.pkl', 'rb') as f:
        category_mapping = pickle.load(f)
    
    flat_category_map = {name: category for category, names in category_mapping.items() for name in names}
    # Assign categories to 'person' 
    category_map = lambda x: flat_category_map.get(x, "Other")
    category = category_map(name_text)

    # Load the dictionary changing category to category num (.pkl file)
    with open('category_num_mapping.pkl', 'rb') as file:
        cat_num_dict = pickle.load(file)

    category_num =  cat_num_dict[category]

    # Load the dictionary changing source to source num (.pkl file)
    with open('source_num_mapping.pkl', 'rb') as file:
        source_num_dict = pickle.load(file)
    
    source_num =  source_num_dict[source]

    # Single Data
    single_data = [date, source_num, category_num, text]
    single_df = pd.DataFrame([single_data], columns=['extracted_date', 'source_mapped', 'category_num', 'clean_statement'])
    # Load preprocessing function
    with open('preprocessor.pkl', 'rb') as file:
        preprocessor = pickle.load(file)
        
    ## preprocess single data
    preprocessed_single_data = preprocessor.transform(pd.DataFrame(single_df))

    return preprocessed_single_data




def clean_text(text):
    lemmatizer = WordNetLemmatizer()
    if pd.isna(text):  
        return ""
    text = text.lower()
    text = re.sub(r'\d+', '', text)  
    text = re.sub(r'[^\w\s]', '', text)  
    text = text.strip()
    tokens = word_tokenize(text)  
    tokens = [word for word in tokens if word not in stopwords.words('english')]  
    tokens = [lemmatizer.lemmatize(word) for word in tokens]  
    return ' '.join(tokens) 


def extract_date(whereabout):
    # Use regex to find date in the format like 'December 17, 2024'
    match = re.search(r'(\w+ \d{1,2}, \d{4})', whereabout)
    if match:
        return match.group(1)
    else:
        return None
    

def extract_source(whereabout):
    # List of known sources
    sources = ['Facebook', 'Instagram', 'X', 'Twitter', 'YouTube', 'TikTok', 'Threads', 'Pinterest', 'LinkedIn', 'Reddit', 'Truth Social']
    for source in sources:
        if source in whereabout:
            return source
    return 'Unknown'