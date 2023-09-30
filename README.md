# COCO-Panoptic-Annotation-Tools
Tools that can be used to label and annotate COCO Panoptic Segmentation annotation format

This repository is a modification from https://github.com/wshilaji/panoptic_coco_scipt

### Requirements
* panopticapi
  ```ruby
   git clone https://github.com/cocodataset/panopticapi
* labelme
  ```ruby
   git clone https://github.com/wkentaro/labelme

### Steps
1. Label your data images with labelme.
   ```ruby
   labelme
2. Save the .json annotation file of each data image within the same folder your data images are located.
3. Clone this repository within the same path where the data images folder are located.
4. Before you run the labelme2panoptic.py, change the root_dir, out_json_dir, json_file, out_dir, and out_dir1 path based on your folder path.
  ```ruby
   root_dir: path to your data images folder
   out_json_dir: path to the COCO annotation .json format output folder
   out_dir: png output format of each image annotations
   out_dir1: png output format of each image annotations
6. Run labelme2panoptic.py
   ```ruby
   python labelme2panoptic.py

