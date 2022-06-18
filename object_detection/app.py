from distutils.command.upload import upload
from turtle import up
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

import streamlit as st

from array import array
import os
from PIL import Image, ImageDraw, ImageFont
import sys
import time
import json

# APIキーとエンドポイントの読み込み
with open('api_key.json') as f:
    secret = json.load(f)
 
KEY = secret['KEY']
ENDPOINT = secret['ENDPOINT']

computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))

# タグを取得する

def get_tags(filepath):
    local_image = open(filepath, "rb")
    tags_result = computervision_client.tag_image_in_stream(local_image)
    tags = tags_result.tags
    tags_name = []
    for tag in tags:
        tags_name.append(tag.name)
    
    return tags_name



#位置と情報を取得
def detect_object(filepath):
    local_image = open(filepath, "rb")
    detect_objects_results = computervision_client.detect_objects_in_stream(local_image)
    objects = detect_objects_results.objects

    return objects


# filepath = 'img/coffee.jpg'
# print(get_tags(filepath))
# print(detect_object(filepath))

#Streamlit

st.title("物体検出アプリ")

uploaded_file = st.file_uploader('Choose an image...', type=['jpg', 'png'])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_path = f'img/{uploaded_file.name}'
    img.save(img_path)
    objects = detect_object(img_path)

    #描画
    draw = ImageDraw.Draw(img,)
    for object in objects:
        x = object.rectangle.x
        y = object.rectangle.y
        w = object.rectangle.w
        h = object.rectangle.h
        caption = object.object_property

        font = ImageFont.truetype(font='.\Helvetica 400.ttf')
        text_w, text_h = draw.textsize(caption, font=font)

        draw.rectangle([(x,y), (x + w, y + h)], fill=None, outline='green',width=5)
        draw.rectangle([(x,y), (x + text_w, y + text_h)], fill='green', outline='green',width=5)
        draw.text((x,y), caption, fill='white', font=font)
    
    tags_name = get_tags(img_path)
    tags_name = ', '.join(tags_name)

    st.image(img)
    st.markdown('**認識されたコンテンツタグ**')
    st.markdown(f'> {tags_name}')



