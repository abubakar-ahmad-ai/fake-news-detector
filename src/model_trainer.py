"""
model_trainer.py
================
Trains and compares Logistic Regression vs Naive Bayes models.
Selects best model based on accuracy and F1-score.
Saves trained model to disk.
"""

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import joblib
import os


class ModelTrainer:
    """
    Handles training, comparison, and saving of ML models.
    """

    def __init__(self):
        self.logistic_model = None
        self.naive_bayes_model = None
        self.best_model = None
        self.best_model_name = ""

    def split_data(self, X, y, test_size=0.2, random_state=42):
        """
        Split data into training and testing sets.
        
        Args:
            X: Feature matrix (TF-IDF vectors)
            y: Labels (0=Fake, 1=Real)
            test_size: 20% for testing, 80% for training
            
        Returns:
            X_train, X_test, y_train, y_test
        """
        print(f"[INFO] Splitting data: {int((1-test_size)*100)}% train, {int(test_size*100)}% test")
        return train_test_split(X, y, test_size=test_size, random_state=random_state)

    def train_logistic_regression(self, X_train, y_train):
        """
        Train Logistic Regression model.
        C=1.0 is regularization parameter (prevents overfitting)
        max_iter=1000 ensures convergence on large datasets
        """
        print("[INFO] Training Logistic Regression...")
        self.logistic_model = LogisticRegression(
            C=1.0,
            max_iter=1000,
            solver="lbfgs",
            random_state=42,
            n_jobs=-1  # Use all CPU cores
        )
        self.logistic_model.fit(X_train, y_train)
        print("[INFO] Logistic Regression training complete!")
        return self.logistic_model

    def train_naive_bayes(self, X_train, y_train):
        """
        Train Multinomial Naive Bayes model.
        alpha=0.1 is Laplace smoothing parameter
        """
        print("[INFO] Training Naive Bayes...")
        self.naive_bayes_model = MultinomialNB(alpha=0.1)
        self.naive_bayes_model.fit(X_train, y_train)
        print("[INFO] Naive Bayes training complete!")
        return self.naive_bayes_model

    def save_model(self, model, path="models/logistic_model.pkl"):
        """
        Save trained model to disk using joblib.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(model, path)
        print(f"[INFO] Model saved to: {path}")

    def load_model(self, path="models/logistic_model.pkl"):
        """
        Load saved model from disk.
        """
        model = joblib.load(path)
        print(f"[INFO] Model loaded from: {path}")
        return model