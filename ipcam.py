import cv2

# Replace these with your IP camera's credentials and IP address
username = 'admin'
password = 'Scrc@1234'
ip_address = '192.168.1.121'  # Replace with your camera's IP address
port = '80'  # Common ports are 554 for RTSP or 80 for HTTP
stream_type = '1'  # This could be different based on your camera's stream configuration

# Construct the URL for the camera stream
# For RTSP: rtsp://username:password@ip_address:port/stream_type
# For HTTP: http://username:password@ip_address:port/path_to_stream
url = f'http://{username}:{password}@{ip_address}:{port}/{stream_type}'

# Open the video stream
cap = cv2.VideoCapture(url)

if not cap.isOpened():
    print("Error: Could not open video stream")
else:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        cv2.imshow('IP Camera Stream', frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
