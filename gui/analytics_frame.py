"""
analytics_frame.py
==================
Analytics dashboard with charts and statistics.
Shows prediction distribution pie chart and bar graph.
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json


class AnalyticsFrame(ctk.CTkFrame):
    """Analytics and visualization page."""

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="#0f0f23", corner_radius=0)
        self.controller = controller
        self.canvas_widget = None
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(
            self,
            text="📊  Analytics Dashboard",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#ffffff"
        ).pack(pady=(25, 5), padx=25, anchor="w")

        ctk.CTkLabel(
            self,
            text="Visual breakdown of your prediction history",
            font=ctk.CTkFont(size=13),
            text_color="#888899"
        ).pack(padx=25, anchor="w", pady=(0, 15))

        # Stats row
        self.stats_row = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_row.pack(fill="x", padx=20, pady=(0, 15))

        self.stat_total = self._stat_card("Total Analyzed", "0", "#4fc3f7")
        self.stat_fake  = self._stat_card("Fake News", "0", "#ff5252")
        self.stat_real  = self._stat_card("Real News", "0", "#00e676")
        self.stat_acc   = self._stat_card("Avg Confidence", "0%", "#ffb74d")

        # Chart area
        self.chart_frame = ctk.CTkFrame(
            self, fg_color="#13132a", corner_radius=15)
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

    def _stat_card(self, title, value, color):
        """Create a stat card widget."""
        card = ctk.CTkFrame(
            self.stats_row,
            fg_color="#13132a",
            corner_radius=12
        )
        card.pack(side="left", fill="x", expand=True, padx=6)

        ctk.CTkLabel(
            card, text=title,
            font=ctk.CTkFont(size=12),
            text_color="#888899"
        ).pack(pady=(15, 3))

        val_label = ctk.CTkLabel(
            card, text=value,
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=color
        )
        val_label.pack(pady=(0, 15))
        return val_label

    def refresh(self):
        """Refresh charts and stats from history data."""
        try:
            with open("history/predictions.json", "r") as f:
                history = json.load(f)
        except Exception:
            history = []

        total     = len(history)
        fake_count = sum(1 for h in history if h["label"] == "FAKE")
        real_count = total - fake_count
        avg_conf   = (sum(h["confidence"] for h in history) / total * 100
                      if total > 0 else 0)

        # Update stat cards
        self.stat_total.configure(text=str(total))
        self.stat_fake.configure(text=str(fake_count))
        self.stat_real.configure(text=str(real_count))
        self.stat_acc.configure(text=f"{avg_conf:.1f}%")

        # Draw charts
        self._draw_charts(fake_count, real_count, history)

    def _draw_charts(self, fake_count, real_count, history):
        """Draw pie chart and bar chart using matplotlib."""

        # Remove old chart
        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().destroy()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.5))
        fig.patch.set_facecolor("#13132a")

        # ── Pie chart ─────────────────────────────────
        if fake_count + real_count > 0:
            ax1.pie(
                [fake_count, real_count],
                labels=["Fake", "Real"],
                colors=["#c62828", "#1b5e20"],
                autopct="%1.1f%%",
                startangle=90,
                textprops={"color": "white", "fontsize": 12}
            )
            ax1.set_title("Prediction Distribution",
                          color="white", fontsize=13, pad=10)
        else:
            ax1.text(0.5, 0.5, "No data yet",
                     ha="center", va="center",
                     color="#555577", fontsize=13)
            ax1.set_facecolor("#13132a")

        ax1.set_facecolor("#13132a")

        # ── Bar chart — last 10 confidences ───────────
        ax2.set_facecolor("#0f0f23")
        ax2.tick_params(colors="white")
        ax2.title.set_color("white")

        recent = history[:10][::-1]
        if recent:
            labels = [
                f"{'F' if h['label']=='FAKE' else 'R'}{i+1}"
                for i, h in enumerate(recent)
            ]
            colors = [
                "#c62828" if h["label"] == "FAKE" else "#1b5e20"
                for h in recent
            ]
            values = [h["confidence"] * 100 for h in recent]

            bars = ax2.bar(labels, values, color=colors, edgecolor="#333355")
            ax2.set_ylim(0, 110)
            ax2.set_ylabel("Confidence %", color="white", fontsize=10)
            ax2.set_title("Last 10 Predictions",
                          color="white", fontsize=13, pad=10)

            for bar, val in zip(bars, values):
                ax2.text(bar.get_x() + bar.get_width() / 2,
                         bar.get_height() + 2,
                         f"{val:.0f}%",
                         ha="center", color="white", fontsize=9)
        else:
            ax2.text(0.5, 0.5, "No data yet",
                     ha="center", va="center",
                     color="#555577", fontsize=13,
                     transform=ax2.transAxes)

        for spine in ax2.spines.values():
            spine.set_edgecolor("#333355")

        plt.tight_layout()

        self.canvas_widget = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().pack(
            fill="both", expand=True, padx=10, pady=10)
        plt.close(fig)