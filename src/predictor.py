"""
predictor.py
============
Real-time prediction engine used by the GUI.
Loads saved model and vectorizer, preprocesses input,
and returns prediction with confidence score.
"""

import joblib
from src.preprocessor import TextPreprocessor


class FakeNewsPredictor:
    """
    Production prediction engine for the GUI application.
    Loads trained model + vectorizer and makes real-time predictions.
    """

    def __init__(self,
                 model_path="models/logistic_model.pkl",
                 vectorizer_path="models/tfidf_vectorizer.pkl"):
        """
        Load model and vectorizer from saved .pkl files.
        """
        self.preprocessor = TextPreprocessor()
        self.model = joblib.load(model_path)
        self.vectorizer = joblib.load(vectorizer_path)
        print("[INFO] Predictor loaded successfully!")

    def predict(self, raw_text):
        """
        Full prediction pipeline for a single news article.
        
        Args:
            raw_text (str): Raw news text from GUI input
            
        Returns:
            dict: {
                'label': 'FAKE' or 'REAL',
                'confidence': float (0.0 to 1.0),
                'fake_probability': float,
                'real_probability': float
            }
        """
        # Step 1: Clean the input text
        cleaned = self.preprocessor.clean_text(raw_text)

        # Step 2: Vectorize using saved TF-IDF
        vector = self.vectorizer.transform([cleaned])

        # Step 3: Get prediction (0=Fake, 1=Real)
        prediction = self.model.predict(vector)[0]

        # Step 4: Get probability scores
        probabilities = self.model.predict_proba(vector)[0]
        fake_prob = probabilities[0]
        real_prob = probabilities[1]

        # Step 5: Confidence = probability of the predicted class
        confidence = real_prob if prediction == 1 else fake_prob

        return {
            "label": "REAL" if prediction == 1 else "FAKE",
            "confidence": round(float(confidence), 4),
            "fake_probability": round(float(fake_prob), 4),
            "real_probability": round(float(real_prob), 4),
        }