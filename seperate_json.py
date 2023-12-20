from labelme2json_panoptic_train import modify_categories
from labelme.logger import logger
import json
import glob
import os
import os.path as osp

#directories
root_dir = 'train2/'            #labelme json input
out_sem = 'semantic/'           #directory for labelme json semantic result
out_ins = 'instance/'           #directory for labelme json instance result
sem_train = 'semantic/train2'   #specific directory for labelme json semantic result
ins_train = 'instance/train2'   #specific directory for labelme json instance result

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

        for shape in data['boxes']:
            label_name = shape['label']
            print(label_name)
            if label_name in stuff_cat:
                sem_anns.append(shape)
                print('sem an 0:', sem_anns)
               
            else:
                ins_anns.append(shape)
                print('ins an 0:', ins_anns)
                  
            semantic_ann ={                     #Roboflow labelme format: 
                    'boxes': sem_anns,          #polygon details
                    'key': data['key'],         #source image path
                    'height': data['height'],   #image height
                    'width': data['width']      #image width
                    }
            print('sem an 1;',semantic_ann)

            instance_ann ={
                    'boxes': ins_anns,
                    'key': data['key'],
                    'height': data['height'],
                    'width': data['width']
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
