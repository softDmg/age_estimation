from age_estimation import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import sys
import requests
import base64
import cv2
import json
import numpy as np

class Functions(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Functions, self).__init__()
        self.setupUi(self)
        self.send_button.clicked.connect(self.send_request)
        self.upload_image.clicked.connect(self.upload_image_file)
        self.image_label.setScaledContents(True)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.response_text_edit.setReadOnly(True)
        self.image_path = 'image.jpg'  # Default image path

    def upload_image_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "Images (*.png *.xpm *.jpg)", options=options)
        if file_name:
            self.image_path = file_name
            pixmap = QPixmap(file_name)
            scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)

    
    def send_request(self):
        # Read the image from the label
        pixmap = self.image_label.pixmap()
        if pixmap:
            image = pixmap.toImage()
            image = image.convertToFormat(4)  # QImage::Format_RGB32
            width = image.width()
            height = image.height()
            ptr = image.bits()
            ptr.setsize(image.byteCount())
            arr = np.array(ptr).reshape(height, width, 4)  # Copies the data
            arr = cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR)  # Convert to BGR format for OpenCV

            _, img_encoded = cv2.imencode('.jpg', arr)
            img_encoded = base64.b64encode(img_encoded).decode('utf-8')
            data = {'image': img_encoded}

            # Get the selected model from the combo box
            selected_model = self.comboBox.currentText().strip()
            if selected_model == "--- Select a model ---":
                self.response_text_edit.setPlainText("Please select a model.")
                return
            data['model'] = selected_model
            
            # Send the request to the Flask API
            response = requests.post('http://127.0.0.1:5000/analyze', json=data)
            
            # Handle the response
            if response.status_code == 200:
                response_data = response.json()
                if "error" in response_data:
                    self.response_text_edit.setPlainText(response_data["error"])
                else:
                    age = response_data.get("age", "unknown")
                    gender = response_data.get("gender", "unknown")
                    emotion = response_data.get("emotion", "unknown")
                    formatted_response = f"This is a <b>{gender}</b>, approximately <b>{age}</b> years old and has a <b>{emotion}</b> face."
                    self.response_text_edit.setHtml(formatted_response)
            else:
                self.response_text_edit.setPlainText(f"Error: {response.status_code}")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Functions()
    window.show()
    sys.exit(app.exec_())