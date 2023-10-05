from labelme2json_panoptic import modify_categories
from labelme.logger import logger
import json
import glob
import os
import os.path as osp

root_dir = 'train/'
out_sem = 'semantic/'
out_ins = 'instance/'
sem_train = 'semantic/train'
ins_train = 'instance/train'

def main():
    modified_categories, info, p_license = modify_categories()
    stuff_cat = []
    for i in range(len(modified_categories)):
        if modified_categories[i]['isthing'] == 0:
            stuff_cat.append(modified_categories[i]['name'])

    label_files = glob.glob(osp.join(root_dir, "*.json"))
    for image_id, filename in enumerate(label_files):
        logger.info("open file : {}".format(filename))
        with open(filename, 'r') as fp:
            data = json.load(fp)

        instance_ann = {}
        semantic_ann = {}
        sem_anns = []
        ins_anns = []

        for shape in data['shapes']:
            label_name = shape['label']
            print(label_name)
            if label_name in stuff_cat:
                sem_anns.append(shape)
                print('sem an 0:', sem_anns)
               
            else:
                ins_anns.append(shape)
                print('ins an 0:', ins_anns)
                
                
            semantic_ann ={
                    'version': data['version'],
                    'flags': data['flags'],
                    'shapes': sem_anns,
                    'lineColor': data['lineColor'],
                    'fillColor': data['fillColor'],
                    'imagePath': data['imagePath'],
                    'imageData': data['imageData'],
                    'imageHeight': data['imageHeight'],
                    'imageWidth': data['imageWidth']
                    }
            print('sem an 1;',semantic_ann)

            instance_ann ={
                    'version': data['version'],
                        'flags': data['flags'],
                    'shapes': ins_anns,
                    'lineColor': data['lineColor'],
                    'fillColor': data['fillColor'],
                    'imagePath': data['imagePath'],
                    'imageData': data['imageData'],
                    'imageHeight': data['imageHeight'],
                    'imageWidth': data['imageWidth']
                    }
            print('ins ann 1:', instance_ann)

        print('sem ann 2', semantic_ann)
        output_semantic = osp.join(out_sem, f'{filename}_semantic.json')
        with open(output_semantic, 'w') as output_s:
            json.dump(semantic_ann, output_s, indent=4)
        output_instance = osp.join(out_ins, f'{filename}_instance.json')
        with open(output_instance, 'w') as output_i:
                    json.dump(instance_ann, output_i, indent=4)


if __name__ == "__main__":
    if osp.exists(sem_train):
        print("Output directory already exists:", sem_train)
    else:
        os.makedirs(sem_train)

    if osp.exists(ins_train):
        print("Output directory already exists:", ins_train)
    else:
        os.makedirs(ins_train)
    main()