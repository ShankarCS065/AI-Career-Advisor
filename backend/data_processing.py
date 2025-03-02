import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """
    Preprocess input text: lowercasing, removing stop words, and lemmatization.
    """
    doc = nlp(text.lower())  # Convert text to lowercase
    processed_text = " ".join([token.lemma_ for token in doc if not token.is_stop])
    return processed_text
