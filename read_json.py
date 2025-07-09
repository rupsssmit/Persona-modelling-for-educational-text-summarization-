import json
import re

def clean_text(text):
    """Cleans text by removing extra symbols, fixing spaces, etc."""
    if not isinstance(text, str):
        return text  # Skip if not a string
    
    text = re.sub(r'[“”‘’"\']', '', text)  # Remove curly/smart quotes
    text = re.sub(r'\s+', ' ', text)        # Fix multiple spaces
    text = text.strip()                     # Remove leading/trailing spaces
    return text

input_file = 'ELI5.jsonl'
output_file = 'ELI5_cleaned.jsonl'

processed = 0

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8') as outfile:
    
    for line in infile:
        if processed >= 1000:
            break  # Stop after 1000 entries
        
        # Skip lines that are not JSON (e.g., "question id")
        if not line.strip().startswith('{'):
            continue
        
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue  # Skip corrupted lines
        
        # Clean the 'ctxs' field (if it exists)
        if 'ctxs' in data:
            if isinstance(data['ctxs'], list):
                cleaned_ctxs = []
                for item in data['ctxs']:
                    if isinstance(item, str):
                        cleaned_ctxs.append(clean_text(item))
                    elif isinstance(item, dict) and 'text' in item:
                        item['text'] = clean_text(item['text'])
                        cleaned_ctxs.append(item)
                data['ctxs'] = cleaned_ctxs
        
        # Write cleaned JSON to the output file
        outfile.write(json.dumps(data) + '\n')
        processed += 1

print(f"✅ Cleaned {processed} lines. Saved to {output_file}")



import json
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Download NLTK resources (run once)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    """Applies preprocessing steps to a text string."""
    if not isinstance(text, str):
        return text
    
    # Lowercase
    text = text.lower()
    
    # Remove special chars (keep letters, numbers, basic punctuation)
    text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)
    
    # Tokenization
    tokens = word_tokenize(text)
    
    # Stopword removal
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    return ' '.join(tokens)  # Return as a single string

# File paths
input_file = 'ELI5_cleaned.jsonl'
output_file = 'ELI5_preprocessed.jsonl'

# Process each line
with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8') as outfile:
    
    for line in infile:
        data = json.loads(line)
        
        # Preprocess 'question' (if exists)
        if 'question' in data:
            data['question'] = preprocess_text(data['question'])
        
        # Preprocess 'answers' (if exists)
        if 'answers' in data and isinstance(data['answers'], list):
            data['answers'] = [preprocess_text(ans) for ans in data['answers']]
        
        # Preprocess 'ctxs' (if exists)
        if 'ctxs' in data:
            if isinstance(data['ctxs'], list):
                cleaned_ctxs = []
                for item in data['ctxs']:
                    if isinstance(item, str):
                        cleaned_ctxs.append(preprocess_text(item))
                    elif isinstance(item, dict) and 'text' in item:
                        item['text'] = preprocess_text(item['text'])
                        cleaned_ctxs.append(item)
                data['ctxs'] = cleaned_ctxs
        
        # Write preprocessed JSON
        outfile.write(json.dumps(data) + '\n')

print(f"✅ Preprocessed data saved to {output_file}")


import nltk
import os

# Set the NLTK data path explicitly
nltk.data.path.append(os.path.expanduser('~/nltk_data'))

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading punkt...")
    nltk.download('punkt')

# Now test tokenization
from nltk.tokenize import word_tokenize
print(word_tokenize("This should work now!"))
