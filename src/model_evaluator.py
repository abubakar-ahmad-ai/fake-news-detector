"""
model_evaluator.py
==================
Evaluates trained ML models using professional metrics.
Generates accuracy, precision, recall, F1-score,
and confusion matrix reports.
"""

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)
import os


class ModelEvaluator:
    """
    Handles all model evaluation and reporting.
    """

    def evaluate(self, model, X_test, y_test, model_name="Model"):
        """
        Full evaluation of a trained model.
        
        Args:
            model: Trained sklearn model
            X_test: Test feature matrix
            y_test: True test labels
            model_name: Name for display purposes
            
        Returns:
            dict: Dictionary containing all metric scores
        """
        # Get predictions
        y_pred = model.predict(X_test)

        # Calculate all metrics
        accuracy  = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall    = recall_score(y_test, y_pred)
        f1        = f1_score(y_test, y_pred)
        cm        = confusion_matrix(y_test, y_pred)

        # Print professional report
        print("\n" + "=" * 50)
        print(f"  EVALUATION REPORT — {model_name}")
        print("=" * 50)
        print(f"  Accuracy  : {accuracy:.4f}  ({accuracy*100:.2f}%)")
        print(f"  Precision : {precision:.4f}")
        print(f"  Recall    : {recall:.4f}")
        print(f"  F1-Score  : {f1:.4f}")
        print("=" * 50)
        print(f"\n  Confusion Matrix:")
        print(f"  TN={cm[0][0]}  FP={cm[0][1]}")
        print(f"  FN={cm[1][0]}  TP={cm[1][1]}")
        print("=" * 50)
        print(f"\n  Full Classification Report:")
        print(classification_report(y_test, y_pred,
              target_names=["Fake News", "Real News"]))

        return {
            "model_name": model_name,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "confusion_matrix": cm,
        }

    def compare_models(self, results_list):
        """
        Compare multiple model results and identify best model.
        
        Args:
            results_list: List of result dicts from evaluate()
            
        Returns:
            str: Name of the best performing model
        """
        print("\n" + "=" * 50)
        print("  MODEL COMPARISON SUMMARY")
        print("=" * 50)
        print(f"  {'Model':<25} {'Accuracy':>10} {'F1-Score':>10}")
        print("-" * 50)

        best_f1 = 0
        best_name = ""

        for result in results_list:
            print(f"  {result['model_name']:<25} "
                  f"{result['accuracy']*100:>9.2f}% "
                  f"{result['f1_score']:>10.4f}")
            if result["f1_score"] > best_f1:
                best_f1 = result["f1_score"]
                best_name = result["model_name"]

        print("=" * 50)
        print(f"  BEST MODEL: {best_name} (F1={best_f1:.4f})")
        print("=" * 50)
        return best_name

    def save_report(self, results_list, path="reports/model_report.txt"):
        """
        Save evaluation report to text file.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write("FAKE NEWS DETECTION — MODEL EVALUATION REPORT\n")
            f.write("=" * 50 + "\n\n")
            for result in results_list:
                f.write(f"Model     : {result['model_name']}\n")
                f.write(f"Accuracy  : {result['accuracy']*100:.2f}%\n")
                f.write(f"Precision : {result['precision']:.4f}\n")
                f.write(f"Recall    : {result['recall']:.4f}\n")
                f.write(f"F1-Score  : {result['f1_score']:.4f}\n")
                f.write("-" * 50 + "\n\n")
        print(f"[INFO] Report saved to: {path}")