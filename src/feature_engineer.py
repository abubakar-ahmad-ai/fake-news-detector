"""
feature_engineer.py
===================
Implements TF-IDF vectorization pipeline.
Converts cleaned text into numerical feature matrices
that machine learning models can process.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os


class FeatureEngineer:
    """
    Handles TF-IDF vectorization of cleaned text data.
    Fits vectorizer on training data and transforms both
    train and test sets.
    """

    def __init__(self, max_features=50000, ngram_range=(1, 2)):
        """
        Initialize TF-IDF Vectorizer with professional settings.
        
        Args:
            max_features (int): Maximum vocabulary size
                                50000 gives excellent coverage
            ngram_range (tuple): (1,2) means use single words AND
                                 two-word combinations (bigrams)
                                 e.g., "fake news", "election fraud"
        """
        # --------------------------------------------------------
        # TF-IDF Vectorizer Configuration:
        # max_features=50000 → top 50k most important words
        # ngram_range=(1,2)  → unigrams + bigrams
        # sublinear_tf=True  → apply log scaling to TF
        #                       prevents common words dominating
        # min_df=2           → ignore words appearing < 2 times
        # --------------------------------------------------------
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            sublinear_tf=True,
            min_df=2,
            strip_accents="unicode",
            analyzer="word",
        )

    def fit_transform(self, train_texts):
        """
        Fit vectorizer on training data and transform it.
        
        Args:
            train_texts: Series/list of cleaned training texts
            
        Returns:
            sparse matrix: TF-IDF feature matrix for training
        """
        print("[INFO] Fitting TF-IDF vectorizer on training data...")
        X_train = self.vectorizer.fit_transform(train_texts)
        print(f"[INFO] Vocabulary size       : {len(self.vectorizer.vocabulary_)}")
        print(f"[INFO] Training matrix shape : {X_train.shape}")
        return X_train

    def transform(self, texts):
        """
        Transform new texts using already-fitted vectorizer.
        Used for test data and real-time prediction.
        
        Args:
            texts: Series/list of cleaned texts
            
        Returns:
            sparse matrix: TF-IDF feature matrix
        """
        return self.vectorizer.transform(texts)

    def save_vectorizer(self, path="models/tfidf_vectorizer.pkl"):
        """
        Save fitted vectorizer to disk for later use in GUI.
        
        Args:
            path (str): File path to save vectorizer
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self.vectorizer, path)
        print(f"[INFO] Vectorizer saved to: {path}")

    def load_vectorizer(self, path="models/tfidf_vectorizer.pkl"):
        """
        Load previously saved vectorizer from disk.
        
        Args:
            path (str): File path to load vectorizer from
        """
        self.vectorizer = joblib.load(path)
        print(f"[INFO] Vectorizer loaded from: {path}")
        return self.vectorizer