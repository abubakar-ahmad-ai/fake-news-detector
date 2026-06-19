"""
home_frame.py
=============
Main analysis page of the application.
Contains news input, analyze button, result card,
confidence meter, and loading animation.
"""

import customtkinter as ctk
import json
import datetime
import threading


class HomeFrame(ctk.CTkFrame):
    """
    Home page — core feature of the app.
    User inputs news text and gets Fake/Real prediction.
    """

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#0f0f23", corner_radius=0)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        """Build the complete home page layout."""

        # ── Page title ────────────────────────────────
        ctk.CTkLabel(
            self,
            text="Analyze News Article",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff"
        ).pack(pady=(25, 5), padx=30, anchor="w")

        ctk.CTkLabel(
            self,
            text="Paste any news article below and our AI will detect if it's Real or Fake",
            font=ctk.CTkFont(size=13),
            text_color="#888899"
        ).pack(padx=30, anchor="w")

        # ── Main content: 2 columns ───────────────────
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=15)

        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)

        # ════════════════════════════════════════════
        # LEFT COLUMN — Input area
        # ════════════════════════════════════════════
        left = ctk.CTkFrame(content, fg_color="#13132a", corner_radius=15)
        left.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="nsew")

        ctk.CTkLabel(
            left,
            text="📰  News Text Input",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#4fc3f7"
        ).pack(pady=(18, 8), padx=20, anchor="w")

        # Text input box
        self.text_input = ctk.CTkTextbox(
            left,
            height=280,
            font=ctk.CTkFont(size=13),
            fg_color="#0a0a20",
            border_color="#2a2a4a",
            border_width=1,
            text_color="#e0e0e0",
            wrap="word"
        )
        self.text_input.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        # Placeholder text
        placeholder = ("Paste your news article here...\n\n"
                       "Example: 'Scientists discover new treatment...' or "
                       "'SHOCKING: Government secretly...'")
        self.text_input.insert("1.0", placeholder)
        self.text_input.bind("<FocusIn>", self._clear_placeholder)

        # Button row
        btn_row = ctk.CTkFrame(left, fg_color="transparent")
        btn_row.pack(fill="x", padx=15, pady=(0, 15))

        # Analyze button
        self.analyze_btn = ctk.CTkButton(
            btn_row,
            text="🔍  Analyze News",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            corner_radius=10,
            fg_color="#1565c0",
            hover_color="#1976d2",
            command=self._start_analysis
        )
        self.analyze_btn.pack(side="left", fill="x", expand=True, padx=(0, 8))

        # Clear button
        ctk.CTkButton(
            btn_row,
            text="🗑️  Clear",
            font=ctk.CTkFont(size=13),
            height=45,
            width=90,
            corner_radius=10,
            fg_color="#2a2a3a",
            hover_color="#3a3a4a",
            command=self._clear_input
        ).pack(side="right")

        # ════════════════════════════════════════════
        # RIGHT COLUMN — Results
        # ════════════════════════════════════════════
        right = ctk.CTkFrame(content, fg_color="transparent")
        right.grid(row=0, column=1, padx=(10, 0), sticky="nsew")

        # ── Result card ───────────────────────────────
        self.result_card = ctk.CTkFrame(
            right,
            fg_color="#13132a",
            corner_radius=15,
            border_width=2,
            border_color="#2a2a4a"
        )
        self.result_card.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            self.result_card,
            text="🤖  AI Prediction",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#4fc3f7"
        ).pack(pady=(18, 5), padx=20, anchor="w")

        # Verdict label (FAKE / REAL)
        self.verdict_label = ctk.CTkLabel(
            self.result_card,
            text="⏳  Awaiting Analysis",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#555577"
        )
        self.verdict_label.pack(pady=(10, 5))

        # Confidence percentage
        self.confidence_label = ctk.CTkLabel(
            self.result_card,
            text="Confidence: —",
            font=ctk.CTkFont(size=14),
            text_color="#888899"
        )
        self.confidence_label.pack(pady=(0, 8))

        # Confidence progress bar
        self.confidence_bar = ctk.CTkProgressBar(
            self.result_card,
            width=220,
            height=14,
            corner_radius=7,
            fg_color="#1a1a3a",
            progress_color="#1565c0"
        )
        self.confidence_bar.set(0)
        self.confidence_bar.pack(pady=(0, 18))

        # ── Probability breakdown card ─────────────────
        prob_card = ctk.CTkFrame(
            right,
            fg_color="#13132a",
            corner_radius=15
        )
        prob_card.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            prob_card,
            text="📊  Probability Breakdown",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#4fc3f7"
        ).pack(pady=(15, 10), padx=20, anchor="w")

        # Fake probability row
        fake_row = ctk.CTkFrame(prob_card, fg_color="transparent")
        fake_row.pack(fill="x", padx=20, pady=(0, 6))

        ctk.CTkLabel(
            fake_row,
            text="🔴 Fake",
            font=ctk.CTkFont(size=12),
            text_color="#ff5252",
            width=70
        ).pack(side="left")

        self.fake_bar = ctk.CTkProgressBar(
            fake_row, height=10, corner_radius=5,
            fg_color="#1a1a3a", progress_color="#c62828"
        )
        self.fake_bar.set(0)
        self.fake_bar.pack(side="left", fill="x", expand=True, padx=8)

        self.fake_pct = ctk.CTkLabel(
            fake_row, text="0%",
            font=ctk.CTkFont(size=12), text_color="#ff5252", width=40
        )
        self.fake_pct.pack(side="right")

        # Real probability row
        real_row = ctk.CTkFrame(prob_card, fg_color="transparent")
        real_row.pack(fill="x", padx=20, pady=(0, 15))

        ctk.CTkLabel(
            real_row,
            text="🟢 Real",
            font=ctk.CTkFont(size=12),
            text_color="#00e676",
            width=70
        ).pack(side="left")

        self.real_bar = ctk.CTkProgressBar(
            real_row, height=10, corner_radius=5,
            fg_color="#1a1a3a", progress_color="#1b5e20"
        )
        self.real_bar.set(0)
        self.real_bar.pack(side="left", fill="x", expand=True, padx=8)

        self.real_pct = ctk.CTkLabel(
            real_row, text="0%",
            font=ctk.CTkFont(size=12), text_color="#00e676", width=40
        )
        self.real_pct.pack(side="right")

        # ── Loading indicator ─────────────────────────
        self.loading_label = ctk.CTkLabel(
            right,
            text="",
            font=ctk.CTkFont(size=13),
            text_color="#4fc3f7"
        )
        self.loading_label.pack(pady=5)

    # ════════════════════════════════════════════════
    # EVENT HANDLERS
    # ════════════════════════════════════════════════

    def _clear_placeholder(self, event):
        """Remove placeholder text on first click."""
        current = self.text_input.get("1.0", "end").strip()
        if "Paste your news article" in current:
            self.text_input.delete("1.0", "end")

    def _clear_input(self):
        """Clear text input and reset results."""
        self.text_input.delete("1.0", "end")
        self.verdict_label.configure(
            text="⏳  Awaiting Analysis", text_color="#555577")
        self.confidence_label.configure(text="Confidence: —")
        self.confidence_bar.set(0)
        self.fake_bar.set(0)
        self.real_bar.set(0)
        self.fake_pct.configure(text="0%")
        self.real_pct.configure(text="0%")
        self.loading_label.configure(text="")
        self.controller.update_status("Cleared — Ready for new analysis")

    def _start_analysis(self):
        """Start analysis in separate thread to keep UI responsive."""
        text = self.text_input.get("1.0", "end").strip()

        if not text or "Paste your news article" in text or len(text) < 20:
            self.controller.update_status(
                "⚠️  Please enter a valid news article (min 20 characters)")
            return

        # Disable button during analysis
        self.analyze_btn.configure(
            state="disabled", text="⏳  Analyzing...")
        self.loading_label.configure(text="🤖 AI is analyzing...")
        self.controller.update_status("Analyzing article with AI model...")

        # Run in thread so UI doesn't freeze
        thread = threading.Thread(
            target=self._run_prediction, args=(text,), daemon=True)
        thread.start()

    def _run_prediction(self, text):
        """Run prediction and update UI with results."""
        try:
            result = self.controller.predictor.predict(text)
            # Update UI from main thread
            self.after(0, self._display_result, result, text)
        except Exception as e:
            self.after(0, self._show_error, str(e))

    def _display_result(self, result, original_text):
        """Update UI widgets with prediction results."""

        label      = result["label"]
        confidence = result["confidence"]
        fake_prob  = result["fake_probability"]
        real_prob  = result["real_probability"]

        # ── Update verdict ────────────────────────────
        if label == "FAKE":
            self.verdict_label.configure(
                text="🔴  FAKE NEWS",
                text_color="#ff5252"
            )
            self.confidence_bar.configure(progress_color="#c62828")
        else:
            self.verdict_label.configure(
                text="🟢  REAL NEWS",
                text_color="#00e676"
            )
            self.confidence_bar.configure(progress_color="#1b5e20")

        # ── Update confidence ──────────────────────────
        self.confidence_label.configure(
            text=f"Confidence: {confidence*100:.1f}%")
        self.confidence_bar.set(confidence)

        # ── Update probability bars ────────────────────
        self.fake_bar.set(fake_prob)
        self.real_bar.set(real_prob)
        self.fake_pct.configure(text=f"{fake_prob*100:.1f}%")
        self.real_pct.configure(text=f"{real_prob*100:.1f}%")

        # ── Re-enable button ──────────────────────────
        self.analyze_btn.configure(
            state="normal", text="🔍  Analyze News")
        self.loading_label.configure(text="✅  Analysis complete!")
        self.controller.update_status(
            f"Result: {label} | Confidence: {confidence*100:.1f}% | "
            f"Fake: {fake_prob*100:.1f}% | Real: {real_prob*100:.1f}%"
        )

        # ── Save to history ───────────────────────────
        self._save_to_history(original_text, result)

    def _show_error(self, error_msg):
        """Display error in UI."""
        self.verdict_label.configure(
            text="❌  Error", text_color="#ff9800")
        self.analyze_btn.configure(
            state="normal", text="🔍  Analyze News")
        self.loading_label.configure(text="")
        self.controller.update_status(f"Error: {error_msg}")

    def _save_to_history(self, text, result):
        """Save prediction result to JSON history file."""
        entry = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "text_preview": text[:120] + "..." if len(text) > 120 else text,
            "label": result["label"],
            "confidence": result["confidence"],
            "fake_probability": result["fake_probability"],
            "real_probability": result["real_probability"],
        }
        try:
            with open("history/predictions.json", "r") as f:
                history = json.load(f)
        except Exception:
            history = []

        history.insert(0, entry)   # Most recent first

        with open("history/predictions.json", "w") as f:
            json.dump(history, f, indent=2)