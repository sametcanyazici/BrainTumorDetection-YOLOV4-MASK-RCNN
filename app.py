from fileinput import filename
from urllib import request
from flask import Flask, render_template, request
import os
import cv2
import matplotlib.pyplot as plt
import time
import numpy as np
import segmentation
global image_input, pathImage

configuration_path = "data/last.cfg"
weights_path = "data/last.weights"

labels = open("data/coco.names").read().strip().split('\n')

probability_minimum = 0.3
 
threshold = 0.3
network = cv2.dnn.readNetFromDarknet(configuration_path, weights_path)


layers_names_all = network.getLayerNames()
layers_names_output = [layers_names_all[i[0] - 1]
                       for i in network.getUnconnectedOutLayers()]


app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'


app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', "POST"])
def index():
    return render_template("index.html")


def Results(x, y, img_x, img_y, w, h):
    global scale, area
    print(img_x, img_y)
    if img_x/2 < x and img_y/2 < y:
        area = (" Bölge= Sağ alt")
        if w > h:
            scale = ("Tümör büyüklüğü {} cm |".format((w*2)/100))
        else:
            scale = ("Tümör büyüklüğü {} cm |".format((h*2)/100))
    if img_x/2 > x and img_y/2 > y:
        area = (" Bölge= Sol üst ")
        if w > h:
            scale = ("Tümör büyüklüğü {} cm |".format((w*2)/100))
        else:
            scale = ("Tümör büyüklüğü {} cm |".format((h*2)/100))
    if img_x/2 < x and img_y/2 > y:
        area = (" Bölge= Sağ üst")
        if w > h:
            scale = ("Tümör büyüklüğü {} cm |".format((w*2)/100))
        else:
            scale = ("Tümör büyüklüğü {} cm | ".format((h*2)/100))
    if img_x/2 > x and img_y/2 < y:
        area = (" Bölge= Sol alt")
        if w > h:
            scale = ("Tümör büyüklüğü {} cm |".format((w*2)/100))
        else:
            scale = ("Tümör büyüklüğü {} cm |".format((h*2)/100))


global scale, area


@app.route("/predict", methods=['GET', 'POST'])
def predict():
    global img, img1, image_input, pathImage, objects, filename, scale, area
    if request.method == 'POST':
        file = request.files['file']
        try:
            if file and allowed_file(file.filename):
                filename = file.filename
                file_path = os.path.join('static/files', filename)
                file.save(file_path)
                pathImage = file_path

                image_input = img = cv2.imread(pathImage)
                cv2.imwrite("static/files/1"+filename, img)
                image_input_shape = image_input.shape

                print(img.shape)
                blob = cv2.dnn.blobFromImage(image_input, 1 / 255.0, (416, 416),
                                             swapRB=True, crop=False)

                print(blob.shape)

                network.setInput(blob)
                start = time.time()
                output_from_network = network.forward(layers_names_output)
                end = time.time()

                print('YOLO v4 took {:.5f} seconds'.format(end - start))
                np.random.seed(42)

                bounding_boxes = []
                confidences = []
                class_numbers = []

                h, w = image_input_shape[:2]

                for result in output_from_network:

                    for detection in result:

                        scores = detection[5:]
                        class_current = np.argmax(scores)

                        confidence_current = scores[class_current]

                        if confidence_current > probability_minimum:

                            box_current = detection[0:4] * \
                                np.array([w, h, w, h])

                            x_center, y_center, box_width, box_height = box_current.astype(
                                'int')
                            x_min = int(x_center - (box_width / 2))
                            y_min = int(y_center - (box_height / 2))

                            bounding_boxes.append(
                                [x_min, y_min, int(box_width), int(box_height)])
                            confidences.append(float(confidence_current))
                            class_numbers.append(class_current)
                results = cv2.dnn.NMSBoxes(
                    bounding_boxes, confidences, probability_minimum, threshold)

                objects = []
                for i in range(len(class_numbers)):

                    objects.append(labels[int(class_numbers[i])])

                if len(results) > 0:

                    for i in results.flatten():

                        x_min, y_min = bounding_boxes[i][0], bounding_boxes[i][1]
                        box_width, box_height = bounding_boxes[i][2], bounding_boxes[i][3]

                        print(x_min, y_min, box_height, box_width)

                        img1 = img[y_min-20:y_min+box_height +
                                   20, x_min-20:x_min+box_width+20]
                        cv2.imwrite("static/files/"+"cropped"+filename, img1)
                        cv2.rectangle(image_input, (x_min, y_min), (x_min + box_width, y_min + box_height),
                                      color=(0, 255, 255), thickness=2)
                        Results(x_min, y_min, h, w, box_width, box_height)
                print("Doğruluk değeri: ", confidences[i])
                conf = " %.2f" % confidences[i]
                plt.rcParams['figure.figsize'] = (10.0, 10.0)
                outpot = cv2.cvtColor(image_input, cv2.COLOR_BGR2BGRA)
                cv2.imwrite("static/files/"+filename, outpot)

                return render_template('predict.html', confidence=conf, product=list(set(objects)), cropped="static/files/"+"cropped"+filename, filename1=filename, image="static/files/1"+filename, product2=scale, product3=area, user_image="static/files/"+filename)

        except Exception as e:
            return "Unable to read the file. Please check if the file extension is correct."


def predict1(pathImage, filename):

    image_input = img = cv2.imread(pathImage)
    cv2.imwrite("static/files/1"+filename, img)
    image_input_shape = image_input.shape

    print(img.shape)
    blob = cv2.dnn.blobFromImage(image_input, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)

    print(blob.shape)

    network.setInput(blob)
    start = time.time()
    output_from_network = network.forward(layers_names_output)
    end = time.time()

    print('YOLO v4 took {:.5f} seconds'.format(end - start))
    np.random.seed(42)

    bounding_boxes = []
    confidences = []
    class_numbers = []

    h, w = image_input_shape[:2]

    for result in output_from_network:

        for detection in result:

            scores = detection[5:]
            class_current = np.argmax(scores)

            confidence_current = scores[class_current]

            if confidence_current > probability_minimum:

                box_current = detection[0:4] * \
                    np.array([w, h, w, h])

                x_center, y_center, box_width, box_height = box_current.astype(
                    'int')
                x_min = int(x_center - (box_width / 2))
                y_min = int(y_center - (box_height / 2))

                bounding_boxes.append(
                    [x_min, y_min, int(box_width), int(box_height)])
                confidences.append(float(confidence_current))
                class_numbers.append(class_current)
    results = cv2.dnn.NMSBoxes(
        bounding_boxes, confidences, probability_minimum, threshold)

    objects = []
    for i in range(len(class_numbers)):

        objects.append(labels[int(class_numbers[i])])

    if len(results) > 0:

        for i in results.flatten():

            x_min, y_min = bounding_boxes[i][0], bounding_boxes[i][1]
            box_width, box_height = bounding_boxes[i][2], bounding_boxes[i][3]

            print(x_min, y_min, box_height, box_width)

            img1 = img[y_min-20:y_min+box_height +
                       20, x_min-20:x_min+box_width+20]
            cv2.imwrite("static/files/"+"cropped"+filename, img1)
            # cv2.rectangle(image_input, (x_min, y_min), (x_min + box_width, y_min + box_height),
            # color=(0, 255, 255), thickness=2)
            Results(x_min, y_min, h, w, box_width, box_height)
    print("Doğruluk değeri: ", confidences[i])
    conf = " %.2f" % confidences[i]
    plt.rcParams['figure.figsize'] = (10.0, 10.0)
    outpot = cv2.cvtColor(image_input, cv2.COLOR_BGR2BGRA)
    cv2.imwrite("static/files/"+filename, outpot)


@app.route("/segmentation", methods=['GET', 'POST'])
def funcSegmentation():
    global objects, filename
    if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join('static/files', filename)
            file.save(file_path)
            pathImage = file_path
    predict1(pathImage, filename)
    segmentation.seg(pathImage, filename)
    return render_template('segmentation.html', cropped="static/files/"+"cropped"+filename, filename1=filename, image="static/files/1"+filename, user_image1="static/files/"+filename, user_image="static/files/Segmentation"+filename, matchname=filename)


if __name__ == "__main__":

    app.run(debug=False)
