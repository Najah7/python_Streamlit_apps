from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import json

# APIキーとエンドポイントの読み込み
with open('../.gitignore') as f:
    secret = json.load(f)
 
KEY = secret['KEY']
ENDPOINT = secret['ENDPOINT']

computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))

local_image_path = 'img/coffee.jpg'

local_image_objects = open(local_image_path, "rb")



print("===== Detect Objects - local =====")
# Call API with local image
detect_objects_results_local = computervision_client.detect_objects_in_stream(local_image_objects)

# Print results of detection with bounding boxes
print("Detecting objects in local image:")
if len(detect_objects_results_local.objects) == 0:
    print("No objects detected.")
else:
    for object in detect_objects_results_local.objects:
        print("object at location {}, {}, {}, {}".format( \
        object.rectangle.x, object.rectangle.x + object.rectangle.w, \
        object.rectangle.y, object.rectangle.y + object.rectangle.h))
print()