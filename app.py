"""
app.py
======
Application entry point.
Launches the Fake News Detection GUI.
"""

from gui.main_window import MainWindow


def main():
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()