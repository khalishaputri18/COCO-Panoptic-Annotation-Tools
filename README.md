# COCO-panoptic-annotation-tools
Tools that can be used to label and annotate COCO Panoptic Segmentation annotation format

This repository is a modification from https://github.com/wshilaji/panoptic_coco_scipt

Original: each color of the png annotations output represents each class with no different colors for each class instance (semantic), and the polygon area is 0.

Modification: different colors for each instance for things categories and each class for stuff categories, and the polygon area is calculated using the shoelace algorithm.

### Requirements
* panopticapi
  ```ruby
   git clone https://github.com/cocodataset/panopticapi
* labelme
  ```ruby
   git clone https://github.com/wkentaro/labelme

### Steps
1. Label your data images using Roboflow (you can use Smart Polygon in Roboflow to label faster).
2. Save the labelme JSON annotation file from Roboflow of each data image within the same folder your data images are located.
   Example:
   ```ruby
   data
    |___train
          |___000.jpg
          |___000.json #labelme json annotation file
          |___001.jpg
          |___001.json #labelme json annotation file
4. Run seperate_json.py to separate the stuff and things categories from each image into two JSON files (stuff categories JSON and things categories JSON). Change the directory path in the program according to your need.
   ```ruby
   python seperate_json.py
5. Run labelme2png_instance.py and labelme2png_semantic.py to generate both stuff and things mask as two separate images. Change the directory path in the program according to your need.
   ```ruby
   python labelme2png_instance.py
   python labelme2png_semantic.py
7. Run merge_label.py to merge both stuff and things masks of each image. Change the directory path in the program according to your need.
   ```ruby
   python merge_label.py
8. Run labelme2json_panoptic.py to generate the COCO panoptic JSON format file that will be saved within the output folder.
   ```ruby
   python labelme2json_panoptic.py
9. As the result, you will get:
    * Panoptic segmentation mask png files as the data png annotations.
    * Panoptic segmentation JSON COCO annotation format file for every annotation of every image within one folder (e.g. train, val).

