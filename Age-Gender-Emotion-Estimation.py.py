from deepface import DeepFace
import json

backends = [
  'opencv', 
  'ssd', 
  'dlib', 
  'mtcnn', 
  'fastmtcnn',
  'retinaface', 
  'mediapipe',
  'yolov8',
  'yunet',
  'centerface',
]


objs = DeepFace.analyze(
  img_path = "2.png", 
  actions = ['age', 'gender', 'emotion'],
  detector_backend = backends[0],
)

print(objs)
age = objs[0]["age"]
gender = max(objs[0]["gender"], key=objs[0]["gender"].get)
emotion = max(objs[0]["emotion"], key=objs[0]["emotion"].get)
print("Age:", age)
print("Gender:", gender)
print("Emotion:", emotion)