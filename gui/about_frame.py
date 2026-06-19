"""
about_frame.py
==============
About page showing project information,
technologies used, and model performance.
"""

import customtkinter as ctk


class AboutFrame(ctk.CTkFrame):
    """About / Info page."""

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#0f0f23", corner_radius=0)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        scroll = ctk.CTkScrollableFrame(
            self, fg_color="#0f0f23")
        scroll.pack(fill="both", expand=True, padx=20, pady=15)

        # Title
        ctk.CTkLabel(
            scroll,
            text="ℹ️  About This Project",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff"
        ).pack(pady=(15, 20))

        sections = [
            ("🎯  Project Title",
             "AI-Based Fake News Detection System\nUsing Machine Learning, NLP, and Tkinter GUI"),

            ("🧠  Technologies Used",
             "• Python 3.x\n• Scikit-Learn (Machine Learning)\n"
             "• NLTK (Natural Language Processing)\n"
             "• TF-IDF Vectorization\n• Logistic Regression\n"
             "• CustomTkinter (Modern GUI)\n• Matplotlib (Visualizations)"),

            ("📈  Model Performance",
             "• Algorithm: Logistic Regression\n"
             "• Accuracy: 99.14%\n• Precision: 98.94%\n"
             "• Recall: 99.28%\n• F1-Score: 99.11%\n"
             "• Dataset: 44,898 articles"),

            ("📁  Dataset",
             "Fake and Real News Dataset\n"
             "Source: Kaggle\n"
             "Fake Articles: 23,481\n"
             "Real Articles: 21,417"),

            ("🔄  How It Works",
             "1. User inputs a news article\n"
             "2. Text is cleaned and preprocessed\n"
             "3. TF-IDF converts text to numbers\n"
             "4. Logistic Regression classifies it\n"
             "5. Confidence score is displayed\n"
             "6. Result is saved to history"),
        ]

        for title, content in sections:
            card = ctk.CTkFrame(
                scroll, fg_color="#13132a", corner_radius=12)
            card.pack(fill="x", pady=8)

            ctk.CTkLabel(
                card, text=title,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#4fc3f7"
            ).pack(pady=(15, 5), padx=20, anchor="w")

            ctk.CTkLabel(
                card, text=content,
                font=ctk.CTkFont(size=13),
                text_color="#cccccc",
                justify="left"
            ).pack(pady=(0, 15), padx=25, anchor="w")