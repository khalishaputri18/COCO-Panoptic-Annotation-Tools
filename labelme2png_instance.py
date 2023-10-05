# -*- coding: utf-8 -*-
"""
Created on  2021-01-01
labeime.json to coco.json
"""

import cv2
import numpy as np

import argparse
import base64
import json
import os
import os.path as osp
import datetime
import glob

import numpy as np
import  sys
import imgviz
import PIL.Image
import matplotlib.pyplot as plt
import time

from labelme.logger import logger
from labelme import utils
from numpy import asarray, ndim

root_dir = 'instance/train/'
out_json_dir = 'output'
json_file = 'instance/train/'
panoptic_coco_categories = 'panoptic_coco_categories.json'
out_dir = 'annotations_ins1'
out_dir1 = 'annotations_ins2'
lbl_png = PIL.Image.open("palette.png")
palette = lbl_png.getpalette()
colorIndexMap = np.array(palette).reshape(256, 3)

def json_to_png(data):
    if not osp.exists(out_dir):
        os.mkdir(out_dir)

    imageData = data.get("imageData")

    if not imageData:
        imagePath = os.path.join(os.path.dirname(json_file), data["imagePath"])
        print(imagePath)
        with open(imagePath, "rb") as f:
            imageData = f.read()
            imageData = base64.b64encode(imageData).decode("utf-8")
    img = utils.img_b64_to_arr(imageData)
    label_name_to_value = {"_background_": 0}
    print(type(data['shapes']))
    for shape in sorted(data["shapes"], key=lambda x: x["label"]):
        print(type(shape))
        label_name = shape["label"]
        if label_name in label_name_to_value:
            label_value = label_name_to_value[label_name]
        else:
            label_value = len(label_name_to_value)
            label_name_to_value[label_name] = label_value

    print("LBLNAMETOVLUE:",label_name_to_value)

    lbl, ins = utils.shapes_to_label(
        img.shape, data["shapes"], label_name_to_value
    )

    file_png = osp.join(out_dir,"{}.png".format(data["imagePath"].split('.')[0]))
    utils.lblsave(file_png, ins) #for things


    img = PIL.Image.open(file_png).convert('RGB')
    '''
    plt.figure(figsize=(9, 5))
    plt.subplot(121)
    plt.imshow(lbl_png)
    plt.axis('off')
    plt.subplot(122)
    plt.imshow(img)
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    '''
    img.save(osp.join(out_dir1,"{}.png".format(data["imagePath"].split('.')[0])))
    return  label_name_to_value


def counter():
    cnt = 1
    def increce():
        nonlocal cnt
        x = cnt
        cnt += 1
        return x
    return increce

def modify_categories():
    with open(panoptic_coco_categories, 'r') as f:
        categories_list = json.load(f)

    ref_json_path = '000000397133.json'
    data = json.load(open(ref_json_path))
    return categories_list,data['info'],data['licenses']


def main():

    now = datetime.datetime.now()
    modified_categories, info, p_license = modify_categories()

    data_coco = dict(
        info=dict(
            description=info['description'],
            url=info['url'],
            version=info['version'],
            year=now.year,
            contributor=info['contributor'],
            date_created=now.strftime("%Y-%m-%d %H:%M:%S.%f"),
        ),
        licenses=p_license,
        images=[
            # license, url, file_name, height, width, date_captured, id
        ],
        annotations=[
            # segmentation, area, iscrowd, image_id, bbox, category_id, id
        ],
        categories = modified_categories,
    )
    
    json_list = os.listdir(root_dir)
    cnt = counter()
    label_files = glob.glob(osp.join(root_dir, "*.json"))
    for image_id, filename in enumerate(label_files):
        logger.info("open file : {}".format(filename))
        with open(filename, 'r') as fp:
            data = json.load(fp)
        file_name = os.path.basename(data['imagePath'])
        data_coco['images'].append(
            dict(
                id=image_id,
                file_name=file_name,
                height=data['imageHeight'],
                width=data['imageWidth'],
                license=None,
                flickr_url=None,
                coco_url=None,
                date_captured=None
            )
        )
        label_name_to_value = json_to_png(data)
        # annotations
        segment_infos = []

        for i in range(len(data['shapes'])):
            segmentation = [list(np.asarray(data['shapes'][i]['points']).flatten())]  # data['shapes'][0]['points']

            x = segmentation[0][::2]
            y = segmentation[0][1::2]
            x_left = min(x)
            y_left = min(y)
            w = max(x) - min(x)
            h = max(y) - min(y)
            bbox = [int(x_left), int(y_left), int(w), int(h)]

            cat_list_dict = [cat for cat in data_coco['categories'] if
                             cat['name'] == data['shapes'][i]['label']]
            cls_id = cat_list_dict[0]['id']

            
            instance_id = label_name_to_value[data['shapes'][i]['label']]
            color = colorIndexMap[instance_id]
            maskid = color[0] + 256 * color[1] + 256 * 256 * color[2]
            segment_infos.append(
                dict(
                    id=int(maskid),
                    category_id=cls_id,
                    area=0,
                    bbox=bbox,
                    iscrowd=0
                )
            
            )
        data_coco['annotations'].append(
            dict(
                image_id=data_coco['images'][image_id]['id'],
                file_name=data_coco['images'][image_id]['file_name'].split('.')[0] + ".png",
                segments_info=segment_infos
            )
        )
        
if __name__ == "__main__":
    if osp.exists(out_dir):
        print("Output directory already exists:", out_dir)
    else:
        os.makedirs(out_dir)

    if osp.exists(out_dir1):
        print("Output directory already exists:", out_dir1)
    else:
        os.makedirs(out_dir1)
    main()
    
