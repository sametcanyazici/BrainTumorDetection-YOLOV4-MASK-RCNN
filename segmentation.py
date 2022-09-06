import app
import sys
sys.path.append("data/maskrcnn_colab/mrcnn_demo")
from m_rcnn import *
from visualize import random_colors, get_mask_contours, draw_mask
import cv2

global inference_config

def seg(pathimage, filename):

    print(app.probability_minimum)
    img = cv2.imread(pathimage)

    test_model, inference_config = load_inference_model(
        1, "data/maskrcnn_colab/mask_rcnn_object_0005.h5")
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect results
    r = test_model.detect([image])[0]
    colors = random_colors(80)

    # Get Coordinates and show it on the image
    object_count = len(r["class_ids"])
    for i in range(object_count):
        # 1. Mask
        mask = r["masks"][:, :, i]
        contours = get_mask_contours(mask)
        for cnt in contours:
            cv2.polylines(img, [cnt], True, colors[i], 2)
            img = draw_mask(img, [cnt], colors[i])

    cv2.imwrite("static/files/"+"Segmentation"+filename, img)

# seg()
