"""
train.py
========
Main training script. Run this file to:
1. Load dataset
2. Preprocess text
3. Extract TF-IDF features
4. Train Logistic Regression + Naive Bayes
5. Compare models
6. Save best model and vectorizer
"""

from src.data_loader import DataLoader
from src.preprocessor import TextPreprocessor
from src.feature_engineer import FeatureEngineer
from src.model_trainer import ModelTrainer
from src.model_evaluator import ModelEvaluator

def main():
    print("\n" + "=" * 50)
    print("  FAKE NEWS DETECTION — TRAINING PIPELINE")
    print("=" * 50 + "\n")

    # ── Step 1: Load Data ──────────────────────────────
    loader = DataLoader()
    df = loader.load_data()
    loader.inspect_data(df)

    # ── Step 2: Preprocess Text ────────────────────────
    preprocessor = TextPreprocessor()
    df = preprocessor.preprocess_dataset(df)

    # ── Step 3: TF-IDF Vectorization ──────────────────
    engineer = FeatureEngineer()
    trainer  = ModelTrainer()
    evaluator = ModelEvaluator()

    X = df["cleaned_text"]
    y = df["label"]

    X_train_raw, X_test_raw, y_train, y_test = trainer.split_data(X, y)

    X_train = engineer.fit_transform(X_train_raw)
    X_test  = engineer.transform(X_test_raw)

    # ── Step 4: Train Both Models ──────────────────────
    lr_model = trainer.train_logistic_regression(X_train, y_train)
    nb_model = trainer.train_naive_bayes(X_train, y_train)

    # ── Step 5: Evaluate Both Models ──────────────────
    lr_results = evaluator.evaluate(lr_model, X_test, y_test, "Logistic Regression")
    nb_results = evaluator.evaluate(nb_model, X_test, y_test, "Naive Bayes")

    # ── Step 6: Compare and Save Best ─────────────────
    best = evaluator.compare_models([lr_results, nb_results])
    evaluator.save_report([lr_results, nb_results])

    # ── Step 7: Save Model + Vectorizer ───────────────
    best_model = lr_model if "Logistic" in best else nb_model
    trainer.save_model(best_model, "models/logistic_model.pkl")
    engineer.save_vectorizer("models/tfidf_vectorizer.pkl")

    print("\n[SUCCESS] Training pipeline complete!")
    print("[INFO] Model saved to: models/logistic_model.pkl")
    print("[INFO] Vectorizer saved to: models/tfidf_vectorizer.pkl")
    print("\nNext step: Run app.py to launch the GUI!\n")

if __name__ == "__main__":
    main()