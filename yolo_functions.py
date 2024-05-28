from ultralytics import YOLO
import cv2
import math
from testMessage import send_notify
import cvzone
# from temhumid import temp, humidity

def video_detection(path_x):
    video_capture = path_x
    notify = False
    nothing = True

    cap=cv2.VideoCapture(video_capture)

    model=YOLO("final_model.pt")

    # classNames = ["fire", "other", "smoke"]
    classnames = ['Liquid', 'Metal', 'fire', 'Solid', 'object', 'smoke', 'background']

    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (50, 150)
    fontScale = 5
    color = (255, 255, 255)
    thickness = 10
    notification = "NOTHING"

    font2 = cv2.FONT_HERSHEY_SIMPLEX
    org2 = (150, 150)
    fontScale2 = 5
    color2 = (255, 255, 255)
    thickness2 = 10
    notification2 = f'Temperature:   -  Humidity: '
    while True:
        success, frame = cap.read()
        results = model(frame, stream=True)
        # for result in results:
        #     boxes = result.boxes
        #     for box in boxes:
        #         x1, y1, x2, y2 = box.xyxy[0]
        #         x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        #         print(x1, y1, x2, y2)
        #         cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,255), 3)
        #         conf = math.ceil((box.conf[0]*100))/100
        #         cls = int(box.cls[0])
        #         class_name = classNames[cls]
        #         label = f'{class_name}{conf}'
        #         t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
        #         print(t_size)
        #         c2 = x1 + t_size[0], y1 - t_size[1] - 3
        #         cv2.rectangle(img, (x1, y1), c2, [255,0,255], -1, cv2.LINE_AA)
        #         cv2.putText(img, label, (x1, y1-2), 0, 1, [255,255,255], thickness=1, lineType=cv2.LINE_AA)
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
                    cv2.putText(frame, notification, org, font, fontScale, color, thickness, cv2.LINE_AA)
                elif class_name == "smoke" and confidence > 0.4:
                    color = (255, 165, 0)
                    notification = "SMOKE"
                    cv2.putText(frame, notification, org, font, fontScale, color, thickness, cv2.LINE_AA)
                else:
                    color = (255, 255, 255)
                    notification = "NOTHING"
                    cv2.putText(frame, notification, org, font, fontScale, color, thickness, cv2.LINE_AA)

                if class_name == "fire" and confidence > 50 and notify:
                    send_notify()
                    notify = False

                temperature = 30
                humid = 50
                notification2 = f"Temperature: {temperature}  -  Humidity: {humid}"

                cv2.putText(frame, notification2, org2, font2, fontScale2, color2, thickness2, cv2.LINE_AA)
                # color = (255, 255, 255)
                # notification = "NOTHING"
                
        # cv2.putText(frame, notification, org, font, fontScale, color, thickness, cv2.LINE_AA)

        yield frame


cv2.destroyAllWindows()
