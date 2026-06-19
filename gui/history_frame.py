"""
history_frame.py
================
Displays all past predictions in a scrollable table.
Shows timestamp, text preview, verdict, and confidence.
"""

import customtkinter as ctk
import json


class HistoryFrame(ctk.CTkFrame):
    """Prediction history page."""

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#0f0f23", corner_radius=0)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        # Header row
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=25, pady=(25, 10))

        ctk.CTkLabel(
            header,
            text="📋  Prediction History",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff"
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text="🔄  Refresh",
            width=100, height=35,
            corner_radius=8,
            fg_color="#1565c0",
            hover_color="#1976d2",
            command=self._load_history
        ).pack(side="right")

        ctk.CTkButton(
            header,
            text="🗑️  Clear All",
            width=100, height=35,
            corner_radius=8,
            fg_color="#2a2a3a",
            hover_color="#3a3a4a",
            command=self._clear_history
        ).pack(side="right", padx=(0, 10))

        # Scrollable container
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="#0f0f23",
            label_text=""
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        self._load_history()

    def _load_history(self):
        """Load and display history from JSON file."""
        # Clear existing rows
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        try:
            with open("history/predictions.json", "r") as f:
                history = json.load(f)
        except Exception:
            history = []

        if not history:
            ctk.CTkLabel(
                self.scroll_frame,
                text="No predictions yet.\nGo to Home and analyze some news!",
                font=ctk.CTkFont(size=14),
                text_color="#555577"
            ).pack(pady=60)
            return

        # Column headers
        col_frame = ctk.CTkFrame(
            self.scroll_frame, fg_color="#13132a", corner_radius=8)
        col_frame.pack(fill="x", pady=(0, 5))

        headers = [("  Date & Time", 150),
                   ("News Preview", 350),
                   ("Verdict", 100),
                   ("Confidence", 100)]

        for h_text, h_width in headers:
            ctk.CTkLabel(
                col_frame,
                text=h_text,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#4fc3f7",
                width=h_width,
                anchor="w"
            ).pack(side="left", padx=8, pady=10)

        # Data rows
        for i, entry in enumerate(history):
            row_color = "#13132a" if i % 2 == 0 else "#0f0f23"
            row = ctk.CTkFrame(
                self.scroll_frame,
                fg_color=row_color,
                corner_radius=6
            )
            row.pack(fill="x", pady=2)

            verdict_color = "#ff5252" if entry["label"] == "FAKE" else "#00e676"
            verdict_icon  = "🔴" if entry["label"] == "FAKE" else "🟢"

            # Timestamp
            ctk.CTkLabel(
                row, text=f"  {entry['timestamp']}",
                font=ctk.CTkFont(size=11), text_color="#888899",
                width=150, anchor="w"
            ).pack(side="left", padx=4, pady=8)

            # Preview
            ctk.CTkLabel(
                row, text=entry["text_preview"],
                font=ctk.CTkFont(size=11), text_color="#cccccc",
                width=350, anchor="w", wraplength=340
            ).pack(side="left", padx=4)

            # Verdict
            ctk.CTkLabel(
                row,
                text=f"{verdict_icon} {entry['label']}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=verdict_color,
                width=100
            ).pack(side="left", padx=4)

            # Confidence
            ctk.CTkLabel(
                row,
                text=f"{entry['confidence']*100:.1f}%",
                font=ctk.CTkFont(size=12),
                text_color="#aaaacc",
                width=100
            ).pack(side="left", padx=4)

    def _clear_history(self):
        """Clear all history."""
        with open("history/predictions.json", "w") as f:
            json.dump([], f)
        self._load_history()
        self.controller.update_status("History cleared")