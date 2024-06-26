from flask import Flask, render_template, Response
import cv2
from deepface import DeepFace

app = Flask(__name__)

# Initialize the webcam
cap = cv2.VideoCapture(1)

def gen_frames():
    print("Starting video stream...")
    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to capture frame")
            break
        else:
            try:
                # Analyze the frame using DeepFace
                analysis = DeepFace.analyze(frame, actions=['age', 'gender', 'emotion'], enforce_detection=False)
                
                for face in analysis:
                    x, y, w, h = face['region']['x'], face['region']['y'], face['region']['w'], face['region']['h']
                    age = face['age']
                    
                    # Extract gender predictions
                    gender_predictions = face['gender']
                    gender = max(gender_predictions, key=gender_predictions.get)
                    gender_confidence = gender_predictions[gender]
                    
                    emotion = face['dominant_emotion']
                    
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, f'Age: {age}', (x, y-40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(frame, f'Gender: {gender} ({gender_confidence:.2f})', (x, y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(frame, f'Emotion: {emotion}', (x, y-60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            except Exception as e:
                print(f"Error during analysis: {e}")
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
