"""
data_loader.py
==============
Responsible for loading and merging the Fake/True news CSV datasets.
Performs initial inspection and basic cleaning of the raw data.
"""

import pandas as pd
import os


class DataLoader:
    """
    Handles all dataset loading operations.
    Loads Fake.csv and True.csv, assigns labels, and merges them.
    """

    def __init__(self, raw_data_path="data/raw"):
        """
        Initialize DataLoader with path to raw data folder.
        
        Args:
            raw_data_path (str): Path to folder containing Fake.csv and True.csv
        """
        self.raw_data_path = raw_data_path
        self.fake_path = os.path.join(raw_data_path, "Fake.csv")
        self.true_path = os.path.join(raw_data_path, "True.csv")

    def load_data(self):
        """
        Load both CSV files, assign labels, merge into one DataFrame.
        
        Returns:
            pd.DataFrame: Merged dataset with 'text' and 'label' columns
        """

        print("[INFO] Loading Fake news dataset...")
        fake_df = pd.read_csv(self.fake_path)

        print("[INFO] Loading True news dataset...")
        true_df = pd.read_csv(self.true_path)

        print(f"[INFO] Fake news articles loaded : {len(fake_df)}")
        print(f"[INFO] True news articles loaded : {len(true_df)}")

        # --------------------------------------------------------
        # Assign numeric labels
        # 0 = Fake News
        # 1 = Real News
        # --------------------------------------------------------
        fake_df["label"] = 0
        true_df["label"] = 1

        # --------------------------------------------------------
        # Combine title + text for richer NLP features
        # More text = better TF-IDF representation
        # --------------------------------------------------------
        fake_df["text"] = fake_df["title"].fillna("") + " " + fake_df["text"].fillna("")
        true_df["text"] = true_df["title"].fillna("") + " " + true_df["text"].fillna("")

        # --------------------------------------------------------
        # Keep only the columns we need
        # --------------------------------------------------------
        fake_df = fake_df[["text", "label"]]
        true_df = true_df[["text", "label"]]

        # --------------------------------------------------------
        # Merge both datasets into one
        # shuffle=True mixes fake and real articles randomly
        # --------------------------------------------------------
        merged_df = pd.concat([fake_df, true_df], ignore_index=True)
        merged_df = merged_df.sample(frac=1, random_state=42).reset_index(drop=True)

        print(f"[INFO] Total articles after merge : {len(merged_df)}")
        print(f"[INFO] Label distribution:\n{merged_df['label'].value_counts()}")

        return merged_df

    def inspect_data(self, df):
        """
        Print detailed inspection report of the loaded dataset.
        
        Args:
            df (pd.DataFrame): The merged dataset
        """
        print("\n" + "=" * 50)
        print("  DATASET INSPECTION REPORT")
        print("=" * 50)
        print(f"  Total rows       : {df.shape[0]}")
        print(f"  Total columns    : {df.shape[1]}")
        print(f"  Fake articles    : {len(df[df['label'] == 0])}")
        print(f"  Real articles    : {len(df[df['label'] == 1])}")
        print(f"  Missing values   :\n{df.isnull().sum()}")
        print(f"  Duplicate rows   : {df.duplicated().sum()}")
        print("=" * 50)
        print("\n  Sample Data (first 3 rows):")
        print(df.head(3))
        print("=" * 50 + "\n")