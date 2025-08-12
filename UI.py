import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QPushButton, QVBoxLayout, QCheckBox
)
from PyQt5.QtGui import QPixmap, QTextCharFormat, QColor, QFont
from PyQt5.QtCore import Qt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class PlantDoctorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌱 Plant Doctor")
        self.setGeometry(300, 100, 700, 800)

        # Set black background
        self.setStyleSheet("background-color: black; color: white;")
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        self.init_form_ui()

    def init_form_ui(self):
        """Form to collect plant details."""
        # Logo
        logo_path = os.path.join(BASE_DIR, "image", "logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(180, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label = QLabel()
            logo_label.setPixmap(pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(logo_label)
        else:
            logo_label = QLabel("🌱 Plant Doctor")
            logo_label.setAlignment(Qt.AlignCenter)
            logo_label.setFont(QFont("Arial", 20, QFont.Bold))
            self.layout.addWidget(logo_label)

        # Input fields
        self.flower_name = self.add_input("Name of the Flower:")
        self.plant_color = self.add_input("Plant Color:")
        self.plant_age = self.add_input("Age of the Plant (seedling, mature, etc.):")
        self.soil_type = self.add_input("Soil Type:")
        self.mature_level = self.add_input("Mature Level:")

        # Checkbox for patches
        self.patches_checkbox = QCheckBox("Patches Present?")
        self.patches_checkbox.setFont(QFont("Arial", 12))
        self.patches_checkbox.setStyleSheet("color: white;")
        self.layout.addWidget(self.patches_checkbox)

        # Submit button
        submit_btn = QPushButton("Submit")
        submit_btn.setStyleSheet("background-color: blue; color: white; font-weight: bold; font-size: 14px;")
        submit_btn.clicked.connect(self.submit_form)
        self.layout.addWidget(submit_btn)

    def add_input(self, label_text):
        """Helper to create a label + text input."""
        label = QLabel(label_text)
        label.setFont(QFont("Arial", 12))
        label.setStyleSheet("color: white;")
        entry = QLineEdit()
        entry.setFont(QFont("Arial", 12))
        self.layout.addWidget(label)
        self.layout.addWidget(entry)
        return entry

    def submit_form(self):
        """Runs main.py and shows results."""
        flower = self.flower_name.text().strip()
        color = self.plant_color.text().strip()
        age = self.plant_age.text().strip()
        soil = self.soil_type.text().strip()
        mature = self.mature_level.text().strip()
        patches = "Yes" if self.patches_checkbox.isChecked() else "No"

        main_py_path = os.path.join(BASE_DIR, "main.py")

        try:
            result = subprocess.run(
                ["python", main_py_path, flower, color, age, soil, mature, patches],
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True
            )
            output_text = result.stdout.strip() if result.stdout else "No output from backend."
        except subprocess.CalledProcessError as e:
            output_text = f"[Error Running Backend]\n{e.stderr}"
        except Exception as e:
            output_text = f"Unexpected Error:\n{str(e)}"

        self.show_result(output_text)

    def show_result(self, text):
        """Display the plant analysis results."""
        self.clear_layout()

        text_area = QTextEdit()
        text_area.setReadOnly(True)
        text_area.setFont(QFont("Arial", 12))
        text_area.setText(text)

        # Emoji highlighting
        highlights = {
            "✅": QColor("green"),
            "⚠️": QColor("orange"),
            "❌": QColor("red"),
            "🌸": QColor("purple"),
            "💧": QColor("blue"),
            "☀️": QColor("gold")
        }
        cursor = text_area.textCursor()
        for emoji, color in highlights.items():
            cursor.setPosition(0)
            while cursor.find(emoji):
                fmt = QTextCharFormat()
                fmt.setForeground(color)
                cursor.mergeCharFormat(fmt)

        self.layout.addWidget(text_area)

        back_btn = QPushButton("Back to Lobby")
        back_btn.setStyleSheet("background-color: gray; color: white; font-weight: bold;")
        back_btn.clicked.connect(self.reset_form)
        self.layout.addWidget(back_btn)

    def reset_form(self):
        """Reset to the form view."""
        self.clear_layout()
        self.init_form_ui()

    def clear_layout(self):
        """Clear all widgets from the layout."""
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlantDoctorApp()
    window.show()
    sys.exit(app.exec_())
