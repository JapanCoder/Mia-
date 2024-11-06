import re
import spacy
from transformers import pipeline
from utility_functions import clean_text  # Assuming clean_text from utility_functions
from typing import List, Dict, Tuple

# Load SpaCy model for parsing and NER
nlp_spacy = spacy.load("en_core_web_sm")

# Load Hugging Face pipeline for sentiment analysis
sentiment_pipeline = pipeline("sentiment-analysis")

class NLPProcessing:
    def __init__(self):
        pass

    # ---- 1. Tokenization and Preprocessing ----
    def tokenize_text(self, text: str) -> List[str]:
        """
        Tokenizes and preprocesses input text using SpaCy.
        Args:
            text (str): The text to tokenize.
        Returns:
            List[str]: A list of tokens.
        """
        doc = nlp_spacy(text.lower())
        return [token.text for token in doc if token.is_alpha]  # Keep only alphabetic tokens

    # ---- 2. Advanced Sentiment Analysis ----
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyzes sentiment of the input text using Hugging Face transformer.
        Args:
            text (str): The text to analyze.
        Returns:
            Dict[str, float]: Sentiment scores including positive, negative, and neutral probability.
        """
        sentiment_result = sentiment_pipeline(text)[0]
        label = sentiment_result["label"].lower()
        score = sentiment_result["score"]

        # Normalize sentiment scores
        if label == "positive":
            return {"positive": score, "negative": 1 - score, "neutral": 0.0}
        elif label == "negative":
            return {"positive": 1 - score, "negative": score, "neutral": 0.0}
        else:
            return {"positive": 0.0, "negative": 0.0, "neutral": 1.0}

    # ---- 3. Named Entity Recognition (NER) ----
    def extract_entities(self, text: str) -> List[Tuple[str, str]]:
        """
        Extracts named entities from text using SpaCy.
        Args:
            text (str): The text to process.
        Returns:
            List[Tuple[str, str]]: List of entities and their labels (e.g., PERSON, ORG, etc.).
        """
        doc = nlp_spacy(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        return entities

    # ---- 4. Dependency Parsing and Contextual Intent Recognition ----
    def parse_intent(self, text: str) -> Dict[str, str]:
        """
        Parses intent from the text based on syntax and keywords.
        Args:
            text (str): The text to parse.
        Returns:
            Dict[str, str]: Parsed intent and relevant keywords or subjects.
        """
        doc = nlp_spacy(text.lower())
        intent = "unknown"
        keywords = []

        # Detect intents based on patterns
        if any(token.lemma_ in ["define", "explain", "meaning"] for token in doc):
            intent = "definition"
            keywords = [token.text for token in doc if token.dep_ in {"dobj", "pobj", "attr"}]
        
        elif any(token.lemma_ in ["recommend", "suggest", "advise"] for token in doc):
            intent = "recommendation"
            keywords = [token.text for token in doc if token.dep_ in {"dobj", "pobj"}]
        
        elif any(token.lemma_ in ["create", "build", "make"] for token in doc):
            intent = "creation"
            keywords = [token.text for token in doc if token.dep_ in {"dobj", "pobj"}]

        return {"intent": intent, "keywords": keywords, "original_text": text}

    # ---- 5. Contextual Entity Extraction for Knowledge Lookups ----
    def extract_contextual_entities(self, text: str, context_keywords: List[str]) -> List[Tuple[str, str]]:
        """
        Extracts entities relevant to the current context (e.g., knowledge lookups).
        Args:
            text (str): The text to process.
            context_keywords (List[str]): Contextual keywords to filter relevant entities.
        Returns:
            List[Tuple[str, str]]: List of relevant entities based on the context.
        """
        entities = self.extract_entities(text)
        relevant_entities = [ent for ent in entities if any(kw in ent[0].lower() for kw in context_keywords)]
        return relevant_entities

    # ---- 6. Enhanced Text Cleanup ----
    def clean_and_normalize_text(self, text: str) -> str:
        """
        Cleans text, removes unwanted characters, and normalizes it.
        Args:
            text (str): The text to clean.
        Returns:
            str: Cleaned and normalized text.
        """
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)  # Remove extra whitespace
        text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
        return text

# Test cases to validate enhanced functionality
if __name__ == "__main__":
    nlp = NLPProcessing()

    # Tokenization Test
    print("Tokenized Text:", nlp.tokenize_text("What's the meaning of NLP?"))

    # Sentiment Analysis Test
    print("Sentiment Analysis:", nlp.analyze_sentiment("I absolutely love the new features!"))

    # Named Entity Recognition Test
    print("Named Entities:", nlp.extract_entities("OpenAI is located in San Francisco."))

    # Intent Parsing Test
    print("Intent Parsing:", nlp.parse_intent("Can you recommend a good book?"))

    # Contextual Entity Extraction Test
    print("Contextual Entities:", nlp.extract_contextual_entities("Is Tesla a good investment?", ["tesla", "investment"]))