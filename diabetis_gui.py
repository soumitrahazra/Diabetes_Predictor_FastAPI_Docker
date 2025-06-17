import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QFormLayout
)

API_URL = "http://localhost:8001/predict"  # Change if your API runs elsewhere

class DiabetesPredictorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diabetes Progression Predictor")

        self.layout = QFormLayout()

        # Features for input fields (names must match backend input)
        self.features = [
            "age", "sex", "bmi", "bp",
            "s1", "s2", "s3", "s4", "s5", "s6"
        ]

        self.inputs = {}
        for feature in self.features:
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(f"Enter {feature}")
            self.layout.addRow(QLabel(feature.capitalize()), line_edit)
            self.inputs[feature] = line_edit

        self.predict_button = QPushButton("Predict")
        self.predict_button.clicked.connect(self.predict)
        self.layout.addRow(self.predict_button)

        self.result_label = QLabel("")
        self.layout.addRow(self.result_label)

        self.setLayout(self.layout)

    def predict(self):
        # Collect inputs and validate
        try:
            data = {feat: float(self.inputs[feat].text()) for feat in self.features}
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers for all fields.")
            return

        # Call the API
        try:
            response = requests.post(API_URL, json=data)
            response.raise_for_status()
        except requests.RequestException as e:
            QMessageBox.critical(self, "API Error", f"Failed to connect or get response:\n{e}")
            return

        # Parse and display result
        result = response.json()
        score = result.get("predicted_progression_score", "N/A")
        interp = result.get("interpretation", "")
        self.result_label.setText(
            f"<b>Predicted progression score:</b> {score}<br><b>Interpretation:</b> {interp}"
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiabetesPredictorApp()
    window.show()
    sys.exit(app.exec())

