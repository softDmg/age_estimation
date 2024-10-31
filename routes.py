from flask import Flask, request, jsonify
from deepface import DeepFace
import base64
import cv2
import numpy as np

app = Flask(__name__)

backends = {
    'OpenCV': 'opencv', 
    'Yolo': 'yolov8', 
    'MediaPipe': 'mediapipe', 
    'centerface': 'centerface', 
    'retinaface': 'retinaface'
}

@app.route('/analyze', methods=['POST'])
def analyze_image():
    data = request.json
    img_data = base64.b64decode(data['image'])
    np_img = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    
    selected_model = data.get('model', 'opencv')
    backend = backends.get(selected_model, 'opencv')
    
    try:
        objs = DeepFace.analyze(
            img_path=img, 
            actions=['age', 'gender', 'emotion'],
            detector_backend=backend,
            enforce_detection=False
        )
        
        if objs:
            age = objs[0]["age"]
            gender = max(objs[0]["gender"], key=objs[0]["gender"].get)
            emotion = max(objs[0]["emotion"], key=objs[0]["emotion"].get)
            return jsonify({
                "age": age,
                "gender": gender,
                "emotion": emotion
            })
        else:
            return jsonify({
                "error": "No face detected"
            })
    except Exception as e:
        return jsonify({
            "error": str(e)
        })

if __name__ == "__main__":
    app.run(debug=True)