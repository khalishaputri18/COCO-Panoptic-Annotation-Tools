# COCO-panoptic-annotation-tools
Tools that can be used to label and annotate COCO Panoptic Segmentation annotation format

This repository is a modification from https://github.com/wshilaji/panoptic_coco_scipt

Original: each color of the png annotations output represents each class, no different colors for each class instance (semantic)

Modification: different colors for each instance and each class with stuff category (panoptic)

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
   Example:
   ```ruby
   data
    |___train
          |___000.jpg
          |___000.json #labelme json annotation file
          |___001.jpg
          |___001.json #labelme json annotation file
4. Clone this repository within the same path where the data images folder are located. (within data/ folder if according to example above)
5. Run seperate_json.py to seperate the stuff and things categories from each image into two json files (stuff categories json and things categories json). The stuff categories json will be saved within semantic/train folder, and the thing categories json within instance/train folder.
   ```ruby
   python seperate_json.py
6. Run labelme2png_instance.py and labelme2png_semantic.py to generate both stuff and things mask as two seperate image, where the stuff mask png images result are saved within annotations_sem1 and annotations_sem2 folders, and the things mask png images result within annotations_ins1 and annotations_ins2 folders.
   ```ruby
   python labelme2png_instance.py
   python labelme2png_semantic.py
7. Run merge_label.py to merge both stuff and things masks of each image, the result will be saved within annotations_pan folder.
   ```ruby
   python merge_label.py
9. Run labelme2json_panoptic.py tp generate the COCO panoptic json format file that will be saved within the output folder.
   ```ruby
   python labelme2json_panoptic.py
10. As the result, you will get:
    * Panoptic segmentation mask png files as the data png annotations
    * Panoptic segmentation json annotation file for every annotations of every images within one folder

