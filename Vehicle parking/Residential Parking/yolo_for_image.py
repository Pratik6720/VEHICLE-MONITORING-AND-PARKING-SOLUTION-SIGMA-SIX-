import cv2
import imutils
import numpy as np
#import openalpr as alpr
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load Yolo
net = cv2.dnn.readNet("yolov3-tiny-obj_3000.weights", "yolov3-obj.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Loading image
img = cv2.imread("cacrar11.jpeg")
img = cv2.resize(img, None, fx=0.4, fy=0.4)
# img = cv2.resize(img, None, fx=0.1, fy=0.1)
height, width, channels = img.shape


# 320×320 it’s small so less accuracy but better speed
# 609×609 it’s bigger so high accuracy and slow speed
# 416×416 it’s in the middle and you get a bit of both.

# Detecting objects
blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
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
        if confidence > 0.5:
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

indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

font = cv2.FONT_HERSHEY_PLAIN
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        color = colors[i]
        cv2.rectangle(img, (x , y), (x + w , y + h), color, 2)
        cv2.imwrite("42.png",img)

        img = cv2.imread("42.png")
        crop_img = img[y:y + h, x:x + w]
        cv2.imshow("cropped", crop_img)
        cv2.imwrite("cropped.jpeg",crop_img)
        cv2.waitKey(0)
        #cv2.putText(img, label, (x, y + 30), font,1, color, 3)
cv2.imshow("Image", img)
text = pytesseract.image_to_string(crop_img , lang='eng')
print("plate is "+text)
cv2.waitKey(0)

