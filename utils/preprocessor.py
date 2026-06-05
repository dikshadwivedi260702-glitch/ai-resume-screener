import re
import nltk
import string
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords

def clean_text(text):
    """
    Cleans raw text - lowercases, removes special chars & stopwords.
    """
    # Lowercase
    text = text.lower()

    # Remove emails, URLs, phone numbers
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\b\d{10}\b', '', text)

    # Remove punctuation and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [w for w in words if w not in stop_words]

    return " ".join(words)