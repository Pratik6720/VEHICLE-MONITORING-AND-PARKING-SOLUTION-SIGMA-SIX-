import threading
import time
import cv2
import numpy as np
import platerecognize as pr

# Load Yolo
confidence = 1
net = cv2.dnn.readNetFromDarknet("./yolo trained weights/yolov3-obj.cfg",
                                 "./yolo trained weights/yolov3-tiny-obj_4000.weights")
# net.setPreferableTarget(DNN_BACKEND_OPENCV)
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))
fix_color = (255, 255, 0)


def call_repeatedly(interval, func, *args):
    stopped = threading.Event()

    def loop():
        while not stopped.wait(interval):  #
            func(*args)

    threading.Thread(target=loop, daemon=True).start()
    return stopped.set


# To get the value of plate from the image by applying ocr
def callone():
    if confidence >= 0.90:  # here if the confidence of the plate detected is above 90% then apply ocr
        pr.ocr()

    # Check the value in database whether it is resident or a visitor


# Calling the Function repeatedly for live video
abc = call_repeatedly(6, callone)

# For running on live video please enter the camera ip in below function
# cap = cv2.VideoCapture("http://192.168.0.105/video")

# Loading camera
cap = cv2.VideoCapture("./sample videos/finalcombine2.mp4")
font = cv2.FONT_HERSHEY_PLAIN
starting_time = time.time()
frame_id = 0

while True:
    _, frame = cap.read()
    frame_id += 1
    height, width, channels = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.2:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.4, 0.3)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            color = colors[class_ids[i]]
            cv2.rectangle(frame, (x, y), (x + w + 10, y + h + 10), fix_color, 2)

            # cv2.rectangle(frame, (x, y), (x + w, y + h), fix_color, 2)
            cv2.rectangle(frame, (x, y), (x + w, y), fix_color, -1)
            cv2.imwrite('./output/sdad.jpg', frame)
            img = cv2.imread("./output/sdad.jpg")
            crop_img = img[y:y + h + 10, x:x + w + 20]
            cv2.imshow("cropped", crop_img)
            cv2.imwrite("cropped.jpeg", crop_img)
            small = cv2.resize(crop_img, (0, 0), fx=0.3, fy=0.3)
            cv2.imwrite("cropped.jpeg", small)
            cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y), font, 1, (255, 255, 255), 2)
            if confidence > 0.9:
                cv2.imshow("cropped", crop_img)
                cv2.imwrite("cropped.jpeg", crop_img)
                small = cv2.resize(crop_img, (0, 0), fx=0.3, fy=0.3)
                cv2.imwrite("cropped.jpeg", small)

            elapsed_time = time.time() - starting_time
            fps = frame_id / elapsed_time
            cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), font, 3, (0, 0, 0), 3)
            cv2.imshow("Image", frame)
            key = cv2.waitKey(1)

            if key == 27:
                break
cap.release()
cv2.destroyAllWindows()
