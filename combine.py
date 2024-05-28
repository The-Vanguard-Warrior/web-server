from ultralytics import YOLO
import cv2
import math
from testMessage import send_notify
import cvzone

def combine_detection(path_x):
    video_capture = path_x
    notify = False

    cap = cv2.VideoCapture(video_capture)

    # Load both models
    model = YOLO("final_model.pt")
    model2 = YOLO("mr.pt")

    classnames = ['Liquid', 'Metal', 'fire', 'Solid', 'object', 'smoke', 'background']
    classnames_fall = ['person-fall']
    # with open('classes.txt', 'r') as f:
    #     classnames_fall = f.read().splitlines()

    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (50, 150)
    fontScale = 5
    color = (255, 255, 255)
    thickness = 10
    notification = "NOTHING"

    font2 = cv2.FONT_HERSHEY_SIMPLEX
    org2 = (50, 750)
    fontScale2 = 1
    color2 = (255, 255, 255)
    thickness2 = 2
    notification2 = f'Temperature:   -  Humidity: '
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        # Predict using both models
        results = model(frame, stream=True)
        results_fall = model2(frame, stream=True)
        
        # Process results from the first model
        for info in results:
            boxes = info.boxes
            for box in boxes:
                confidence = box.conf[0]
                confidence = math.ceil(confidence * 100)
                Class = int(box.cls[0])
                class_name = classnames[Class]
                if confidence > 50:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
                    cvzone.putTextRect(frame, f'{classnames[Class]} {confidence}%', [x1 + 8, y1 + 100],
                                       scale=1.5, thickness=2)
                
                if class_name == "fire" and confidence > 50:
                    color = (0, 0, 255)
                    notification = "FIRE"
                    notify = True
                elif class_name == "smoke" and confidence > 50:
                    color = (255, 165, 0)
                    notification = "SMOKE"
                else:
                    color = (255, 255, 255)
                    notification = "NOTHING"

                if class_name == "fire" and confidence > 50 and notify:
                    send_notify()
                    notify = False

        # Process results from the second model
        for info in results_fall:
            boxes = info.boxes
            for box in boxes:
                confidence = box.conf[0]
                confidence = math.ceil(confidence * 100)
                Class = int(box.cls[0])
                class_name = classnames_fall[Class]
                if confidence > 50:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 5)
                    cvzone.putTextRect(frame, f'{classnames_fall[Class]} {confidence}%', [x1 + 8, y1 + 150],
                                       scale=1.5, thickness=2)

        cv2.putText(frame, notification, org, font, fontScale, color, thickness, cv2.LINE_AA)
        cv2.putText(frame, notification2, org2, font2, fontScale2, color2, thickness2, cv2.LINE_AA)
        yield frame

    cap.release()
    cv2.destroyAllWindows()
