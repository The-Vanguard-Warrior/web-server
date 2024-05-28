import cv2
import math
from ultralytics import YOLO

# Function to test YOLO model on video
def test_yolo_on_video(video_path, model_path, output_path):
    # Load the YOLO model
    model = YOLO(model_path)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Define the codec and create VideoWriter object
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Make predictions on the frame
        results = model(frame, stream=True)

        # Process the results
        for result in results:
            for box in result.boxes:
                # Get bounding box coordinates
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                # Get confidence score
                conf = math.ceil(box.conf[0] * 100) / 100
                # Get class label
                class_id = int(box.cls[0])
                class_name = model.names[class_id]

                # Draw bounding box and label on the frame
                label = f'{class_name} {conf:.2f}'
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Write the frame to the output video
        out.write(frame)

        # Display the frame (optional)
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Parameters
video_path = 'fire.mp4'  # Path to input video file
model_path = 'best.pt'  # Path to YOLO model weights
output_path = 'output.mp4'  # Path to output video file

# Test the YOLO model on the video
test_yolo_on_video(video_path, model_path, output_path)
