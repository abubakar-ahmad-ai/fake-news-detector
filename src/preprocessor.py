"""
preprocessor.py
===============
Complete NLP preprocessing pipeline.
Cleans raw news text through multiple stages:
lowercasing → special char removal → tokenization
→ stopword removal → stemming
"""

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


class TextPreprocessor:
    """
    Handles complete NLP text cleaning pipeline.
    Transforms raw news text into clean, normalized tokens.
    """

    def __init__(self):
        """
        Initialize preprocessor with stopwords and stemmer.
        """
        # --------------------------------------------------------
        # English stopwords list from NLTK
        # Examples: "the", "is", "a", "and", "in", "of"
        # These words carry no meaning for classification
        # --------------------------------------------------------
        self.stop_words = set(stopwords.words("english"))

        # --------------------------------------------------------
        # Porter Stemmer — reduces words to their root form
        # Examples: "running" → "run", "lies" → "lie"
        # --------------------------------------------------------
        self.stemmer = PorterStemmer()

    def clean_text(self, text):
        """
        Full preprocessing pipeline for a single text string.
        
        Steps:
        1. Convert to lowercase
        2. Remove URLs
        3. Remove special characters and numbers
        4. Tokenize into words
        5. Remove stopwords
        6. Apply stemming
        7. Rejoin into clean string
        
        Args:
            text (str): Raw news article text
            
        Returns:
            str: Cleaned and preprocessed text
        """

        # --------------------------------------------------------
        # Step 1: Lowercase
        # "Election FRAUD" → "election fraud"
        # --------------------------------------------------------
        text = text.lower()

        # --------------------------------------------------------
        # Step 2: Remove URLs
        # "Visit https://fake.com for more" → "Visit  for more"
        # --------------------------------------------------------
        text = re.sub(r"http\S+|www\S+|https\S+", "", text)

        # --------------------------------------------------------
        # Step 3: Remove special characters, punctuation, numbers
        # "fraud!!! 100%" → "fraud  "
        # --------------------------------------------------------
        text = re.sub(r"[^a-zA-Z\s]", "", text)

        # --------------------------------------------------------
        # Step 4: Remove extra whitespace
        # --------------------------------------------------------
        text = re.sub(r"\s+", " ", text).strip()

        # --------------------------------------------------------
        # Step 5: Tokenize — split string into list of words
        # "election fraud exposed" → ["election", "fraud", "exposed"]
        # --------------------------------------------------------
        tokens = word_tokenize(text)

        # --------------------------------------------------------
        # Step 6: Remove stopwords + apply stemming
        # "the election was fraudulent" →
        # remove "the", "was" → ["election", "fraudulent"]
        # stem → ["elect", "fraudul"]
        # --------------------------------------------------------
        cleaned_tokens = [
            self.stemmer.stem(word)
            for word in tokens
            if word not in self.stop_words and len(word) > 2
        ]

        # --------------------------------------------------------
        # Step 7: Rejoin tokens into a single string
        # ["elect", "fraudul"] → "elect fraudul"
        # --------------------------------------------------------
        return " ".join(cleaned_tokens)

    def preprocess_dataset(self, df):
        """
        Apply cleaning pipeline to entire dataset.
        
        Args:
            df (pd.DataFrame): Dataset with 'text' column
            
        Returns:
            pd.DataFrame: Dataset with added 'cleaned_text' column
        """
        print("[INFO] Starting text preprocessing pipeline...")
        print("[INFO] This may take a few minutes for large datasets...")

        # Apply clean_text function to every row
        df["cleaned_text"] = df["text"].apply(self.clean_text)

        # --------------------------------------------------------
        # Remove rows where cleaning resulted in empty text
        # --------------------------------------------------------
        before = len(df)
        df = df[df["cleaned_text"].str.strip() != ""].reset_index(drop=True)
        after = len(df)

        print(f"[INFO] Preprocessing complete!")
        print(f"[INFO] Rows before cleaning : {before}")
        print(f"[INFO] Rows after cleaning  : {after}")
        print(f"[INFO] Removed empty rows   : {before - after}")

        return df