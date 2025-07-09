import json
import re
import nltk

# Download required NLTK data (run once)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')  # This is what was missing

def clean_text(text):
    """Simplified text cleaner that doesn't rely heavily on NLTK"""
    if not isinstance(text, str):
        text = str(text)
    
    # Basic cleaning without NLTK tokenization
    text = re.sub(r'[\{\}\[\]\"\\]', ' ', text)  # Remove JSON artifacts
    text = re.sub(r'http\S+|www\S+|https\S+', ' ', text)  # Remove URLs
    text = re.sub(r'[^\w\s.,!?;:\'-]', ' ', text)  # Keep basic punctuation
    
    # Remove standalone single characters
    text = ' '.join([word for word in text.split() if len(word) > 1 or word.lower() in ['i', 'a']])
    
    # Normalize whitespace and fix punctuation
    text = re.sub(r'\s+([.,!?;:])\s*', r'\1 ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Capitalize first letter
    if len(text) > 1:
        text = text[0].upper() + text[1:]
    
    return text

def process_entry(entry):
    """Process a single JSON entry into clean paragraph"""
    paragraph_parts = []
    
    for key, value in entry.items():
        # Skip metadata fields
        if key.lower() in ['id', 'question_id', 'index', 'score']:
            continue
            
        # Handle different value types
        if isinstance(value, (str, int, float, bool)):
            cleaned = clean_text(value)
        elif isinstance(value, (list, dict)):
            cleaned = clean_text(json.dumps(value, ensure_ascii=False))
        else:
            cleaned = ""
            
        if cleaned:
            paragraph_parts.append(cleaned)
    
    return ' '.join(paragraph_parts)

# Main processing
processed_data = []
with open("ELI5.jsonl", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i >= 1000:
            break
            
        try:
            entry = json.loads(line)
            paragraph = process_entry(entry)
            if paragraph and len(paragraph.split()) > 3:  # Minimum 4 words
                processed_data.append(paragraph)
        except json.JSONDecodeError:
            continue

# Save results
output = {
    "metadata": {
        "source": "ELI5.jsonl",
        "processed_entries": len(processed_data),
        "cleaning_method": "basic_clean_v3"
    },
    "paragraphs": processed_data
}

with open("ELI5_clean_paragraphs.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"Successfully processed {len(processed_data)} entries")
print("Saved to ELI5_clean_paragraphs.json")
