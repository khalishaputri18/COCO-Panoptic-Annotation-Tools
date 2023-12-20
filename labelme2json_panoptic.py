# -*- coding: utf-8 -*-
"""
Created on  2021-01-01
labeime.json to coco.json
"""

import numpy as np
import base64
import json
import os
import os.path as osp
import datetime
import glob
import numpy as np
import imgviz
import PIL.Image
import matplotlib.pyplot as plt

from labelme.logger import logger
from labelme import utils
from numpy import asarray, ndim

#directories
root_dir = 'train2/'        #raw images and original labelme json path
out_json_dir = 'output2'    #output path for json coco format
json_file = 'train2/'       #original labelme json path
panoptic_coco_categories = 'panoptic_coco_categories.json'  #panoptiic coco categories
out_dir = 'annotations1_train2'     #png annotations (unused)
out_dir1 = 'annotations2_train2'    #png annotations (unused)
lbl_png = PIL.Image.open("palette.png")
palette = lbl_png.getpalette()
colorIndexMap = np.array(palette).reshape(256, 3)

def json_to_png(data, stuff_cat):
    if not osp.exists(out_dir):
        os.mkdir(out_dir)

    imageData = data.get("imageData")

    if not imageData:
        imagePath = os.path.join(os.path.dirname(json_file), data["key"])
        with open(imagePath, "rb") as f:
            imageData = f.read()
            imageData = base64.b64encode(imageData).decode("utf-8")
    img = utils.img_b64_to_arr(imageData)
    label_name_to_value = {"_background_": 0}
    for shape in sorted(data["boxes"], key=lambda x: x["label"]):
        label_name = shape["label"]
        if label_name in label_name_to_value:
            label_value = label_name_to_value[label_name]
        else:
            label_value = len(label_name_to_value)
            label_name_to_value[label_name] = label_value

    lbl, ins = utils.shapes_to_label(
        img.shape, data["boxes"], label_name_to_value
    )
    file_png = osp.join(out_dir,"{}.png".format(data["key"].split('.')[0]))
    print(data["key"])
    for shape in sorted(data["boxes"], key=lambda x: x["label"]):
        label_name = shape["label"]
        print(label_name)
        if label_name in stuff_cat:
            utils.lblsave(file_png, lbl) #for stuff
        else:
            utils.lblsave(file_png, ins) #for things

    img = PIL.Image.open(file_png).convert('RGB')
    img.save(osp.join(out_dir1,"{}.png".format(data["key"].split('.')[0])))
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

def calculate_polygon_area(points):
    # Using the shoelace formula to calculate the area of a polygon
    n = len(points)
    area = 0.5 * abs(sum(points[i][0] * (points[(i + 1) % n][1] - points[(i - 1) % n][1]) for i in range(n)))
    return area


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
        ],
        annotations=[
        ],
        categories = modified_categories,
    )
    stuff_cat = []
    for i in range(len(modified_categories)):
        if modified_categories[i]['isthing'] == 0:
            stuff_cat.append(modified_categories[i]['name'])

    print("STUFF CATEGORIES:",(stuff_cat))
    label_files = glob.glob(osp.join(root_dir, "*.json"))
    for img_id, filename in enumerate(label_files):
        logger.info("open file : {}".format(filename))
        with open(filename, 'r') as fp:
            data = json.load(fp)
        file_name = os.path.basename(data['key'])
        file_without_extension = file_name.split('.')[0]
        image_id = int(file_without_extension)
        print("image_id:", image_id)
        data_coco['images'].append(
            dict(
                id=image_id,
                file_name=file_name,
                height=data['height'],
                width=data['width'],
                license=None,
                flickr_url=None,
                coco_url=None,
                date_captured=None
            )
        )
        label_name_to_value = json_to_png(data, stuff_cat)
        segment_infos = []
        for i in range(len(data['boxes'])):
            segmentation = [list(np.asarray(data['boxes'][i]['points']).flatten())]

            x = segmentation[0][::2]
            y = segmentation[0][1::2]
            x_left = min(x)
            y_left = min(y)
            w = max(x) - min(x)
            h = max(y) - min(y)
            bbox = [int(x_left), int(y_left), int(w), int(h)]

            cat_list_dict = [cat for cat in data_coco['categories'] if
                             cat['name'] == data['boxes'][i]['label']]
            cls_id = cat_list_dict[0]['id']
            
            instance_id = label_name_to_value[data['boxes'][i]['label']]
            color = colorIndexMap[instance_id]
            maskid = color[0] + 256 * color[1] + 256 * 256 * color[2]
            
            area = calculate_polygon_area(data['boxes'][i]['points'])
            
            segment_infos.append(
                dict(
                    id=int(maskid),
                    category_id=cls_id,
                    area=int(area),
                    bbox=bbox,
                    iscrowd=0
                )
            
            )
        data_coco['annotations'].append(
            dict(
                image_id=data_coco['images'][img_id]['id'],
                file_name=data_coco['images'][img_id]['file_name'].split('.')[0] + ".png",
                segments_info=segment_infos
            )
        )


    out_ann_file = osp.join(out_json_dir, "train2.json")

    with open(out_ann_file, "w") as f:
        json.dump(data_coco, f)


if __name__ == "__main__":
    if osp.exists(out_json_dir):
        print("Output directory already exists:", out_json_dir)
    else:
        os.makedirs(out_json_dir)

    if osp.exists(out_dir):
        print("Output directory already exists:", out_dir)
    else:
        os.makedirs(out_dir)

    if osp.exists(out_dir1):
        print("Output directory already exists:", out_dir1)
    else:
        os.makedirs(out_dir1)
    main()
    
