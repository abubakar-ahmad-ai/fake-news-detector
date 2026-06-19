"""
main_window.py
==============
Main application window for Fake News Detection System.
Modern dark theme GUI using CustomTkinter.
Professional sidebar navigation with multiple pages.
"""

import customtkinter as ctk
from gui.home_frame import HomeFrame
from gui.history_frame import HistoryFrame
from gui.analytics_frame import AnalyticsFrame
from gui.about_frame import AboutFrame
from src.predictor import FakeNewsPredictor


# ─────────────────────────────────────────────
# Global appearance settings
# ─────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):
    """
    Root application window.
    Contains sidebar navigation and content area.
    """

    def __init__(self):
        super().__init__()

        # ── Window Configuration ──────────────────────
        self.title("🔍 AI Fake News Detector")
        self.geometry("1200x750")
        self.minsize(1000, 650)

        # ── Load AI Model ─────────────────────────────
        self._load_predictor()

        # ── Build UI ──────────────────────────────────
        self._build_sidebar()
        self._build_content_area()

        # ── Show Home by default ──────────────────────
        self.show_frame("home")

    def _load_predictor(self):
        """Load the trained ML model and vectorizer."""
        try:
            self.predictor = FakeNewsPredictor()
            self.model_status = "✅  Model Loaded  |  Accuracy: 99.14%"
        except Exception as e:
            self.predictor = None
            self.model_status = f"❌  Model Error: {str(e)}"

    def _build_sidebar(self):
        """Build left sidebar with navigation buttons."""

        # Sidebar container
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0,
                                     fg_color="#1a1a2e")
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # ── App Logo / Title ──────────────────────────
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=(30, 10), padx=20, fill="x")

        ctk.CTkLabel(
            logo_frame,
            text="🔍",
            font=ctk.CTkFont(size=40)
        ).pack()

        ctk.CTkLabel(
            logo_frame,
            text="FakeNews\nDetector",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#4fc3f7"
        ).pack()

        ctk.CTkLabel(
            logo_frame,
            text="AI-Powered System",
            font=ctk.CTkFont(size=11),
            text_color="#888888"
        ).pack(pady=(2, 0))

        # Divider
        ctk.CTkFrame(self.sidebar, height=1,
                     fg_color="#333355").pack(fill="x", padx=15, pady=20)

        # ── Navigation Buttons ────────────────────────
        nav_items = [
            ("🏠   Home",      "home"),
            ("📋   History",   "history"),
            ("📊   Analytics", "analytics"),
            ("ℹ️   About",     "about"),
        ]

        self.nav_buttons = {}

        for label, key in nav_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=label,
                font=ctk.CTkFont(size=14),
                anchor="w",
                height=45,
                corner_radius=10,
                fg_color="transparent",
                hover_color="#16213e",
                text_color="#cccccc",
                command=lambda k=key: self.show_frame(k)
            )
            btn.pack(fill="x", padx=15, pady=4)
            self.nav_buttons[key] = btn

        # ── Bottom Info ───────────────────────────────
        ctk.CTkFrame(self.sidebar, height=1,
                     fg_color="#333355").pack(fill="x", padx=15, pady=20,
                                              side="bottom")

        

    def _build_content_area(self):
        """Build main right-side content area."""

        # ── Outer container ───────────────────────────
        right_panel = ctk.CTkFrame(self, fg_color="#0f0f23", corner_radius=0)
        right_panel.pack(side="right", fill="both", expand=True)

        # ── Top header bar ────────────────────────────
        header = ctk.CTkFrame(right_panel, height=50,
                               fg_color="#16213e", corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="AI-Based Fake News Detection System",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#4fc3f7"
        ).pack(side="left", padx=20, pady=12)

        # Model status label (top right)
        ctk.CTkLabel(
            header,
            text=self.model_status,
            font=ctk.CTkFont(size=11),
            text_color="#00e676" if "✅" in self.model_status else "#ff5252"
        ).pack(side="right", padx=20)

        # ── Content frame (pages load here) ──────────
        self.content_area = ctk.CTkFrame(right_panel,
                                          fg_color="#0f0f23",
                                          corner_radius=0)
        self.content_area.pack(fill="both", expand=True)

        # ── Status bar (bottom) ───────────────────────
        self.status_bar = ctk.CTkLabel(
            right_panel,
            text="Ready — Enter news text and click Analyze",
            font=ctk.CTkFont(size=11),
            fg_color="#0a0a1a",
            text_color="#666688",
            anchor="w",
            height=28
        )
        self.status_bar.pack(fill="x", padx=10, pady=(0, 5))

        # ── Initialize all page frames ────────────────
        self.frames = {
            "home":      HomeFrame(self.content_area, self),
            "history":   HistoryFrame(self.content_area, self),
            "analytics": AnalyticsFrame(self.content_area, self),
            "about":     AboutFrame(self.content_area, self),
        }

        # Stack all frames on top of each other
        for frame in self.frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def show_frame(self, key):
        """Switch visible page and highlight active nav button."""

        # Raise selected frame to top
        self.frames[key].lift()

        # Update nav button styles
        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(fg_color="#16213e", text_color="#4fc3f7")
            else:
                btn.configure(fg_color="transparent", text_color="#cccccc")

        # Refresh analytics chart when switching to it
        if key == "analytics":
            self.frames["analytics"].refresh()

    def update_status(self, message):
        """Update bottom status bar text."""
        self.status_bar.configure(text=message)