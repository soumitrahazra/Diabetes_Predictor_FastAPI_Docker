import sys
import pickle
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QFormLayout
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

# Load model
with open("models/diabetes_model.pkl", "rb") as f:
    model = pickle.load(f)

feature_names = [
    "Age", "Sex", "BMI", "Blood Pressure", "S1", "S2", "S3", "S4", "S5", "S6"
]

class DiabetesPredictorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🩺 Diabetes Predictor")
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QLabel {
                font-weight: bold;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                padding: 10px;
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        self.inputs = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("🧮 Predict Diabetes Progression")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        form_layout = QFormLayout()

        for name in feature_names:
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(f"Enter {name.lower()} (numeric)")
            self.inputs.append(line_edit)
            form_layout.addRow(QLabel(name + ":"), line_edit)

        layout.addLayout(form_layout)

        self.predict_button = QPushButton("Predict Score")
        self.predict_button.clicked.connect(self.predict)
        layout.addWidget(self.predict_button)

        self.setLayout(layout)

    def predict(self):
        try:
            values = [float(inp.text()) for inp in self.inputs]
            features = np.array([values])
            prediction = model.predict(features)[0]
            QMessageBox.information(self, "Prediction",
                f"✅ Predicted Diabetes Progression Score:\n\n🧾 {round(prediction, 2)}",
                QMessageBox.StandardButton.Ok)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input",
                "⚠️ Please fill all fields with valid numbers.",
                QMessageBox.StandardButton.Ok)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiabetesPredictorApp()
    window.resize(400, 500)
    window.show()
    sys.exit(app.exec())

