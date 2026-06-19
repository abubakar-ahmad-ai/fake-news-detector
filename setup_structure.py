"""
Project Structure Setup Script
Creates all necessary directories and empty files
for the Fake News Detection System
"""

import os

# ============================================================
# Define the complete project folder structure
# ============================================================
folders = [
    "data/raw",
    "data/processed",
    "models",
    "src",
    "gui",
    "assets/icons",
    "assets/images",
    "history",
    "reports",
    "tests",
]

# ============================================================
# Define all Python files to be created (empty initially)
# ============================================================
files = [
    # Source backend files
    "src/__init__.py",
    "src/data_loader.py",
    "src/preprocessor.py",
    "src/feature_engineer.py",
    "src/model_trainer.py",
    "src/model_evaluator.py",
    "src/predictor.py",

    # GUI files
    "gui/__init__.py",
    "gui/main_window.py",
    "gui/home_frame.py",
    "gui/history_frame.py",
    "gui/analytics_frame.py",
    "gui/about_frame.py",

    # Test files
    "tests/__init__.py",
    "tests/test_predictor.py",

    # Root level files
    "train.py",
    "app.py",
    "README.md",
]

# ============================================================
# Create folders
# ============================================================
print("=" * 50)
print("  Creating Project Structure...")
print("=" * 50)

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"  [FOLDER] Created: {folder}/")

# ============================================================
# Create empty files
# ============================================================
for file in files:
    with open(file, "w") as f:
        pass  # Create empty file
    print(f"  [FILE]   Created: {file}")

# ============================================================
# Create a placeholder for history JSON
# ============================================================
with open("history/predictions.json", "w") as f:
    f.write("[]")  # Empty JSON array
print("  [FILE]   Created: history/predictions.json")

print("=" * 50)
print("  Project structure created successfully!")
print("=" * 50)