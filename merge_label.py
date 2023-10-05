import cv2
import glob
import os
import os
import os.path as osp
import numpy as np

ins_dir = 'annotations_ins1'
sem_dir = 'annotations_sem1'
pan_dir = 'annotations_pan'
sem_dir2 = 'annotations_sem2'

ins_files = os.listdir(ins_dir)
sem_files = os.listdir(sem_dir)

def main():
    for file_ins in ins_files:
        corresponding_file = next((file for file in sem_files if file_ins in file), None)

        if corresponding_file:
            ins_img_path = os.path.join(ins_dir, file_ins)
            sem_img_path = os.path.join(sem_dir, corresponding_file)

            ins_img = cv2.imread(ins_img_path)
            sem_img = cv2.imread(sem_img_path)
            
            #reverse the color, then convert the white color to black color from the semantic images
            if sem_img is not None:
                reversed_sem_img= 255 - sem_img
            
                lower_white = np.array([200, 200, 200])  # lower threshold for white color
                upper_white = np.array([255, 255, 255]) 
                
                white_mask = cv2.inRange(reversed_sem_img, lower_white, upper_white)

                black_mask = cv2.bitwise_not(white_mask)
                image_with_black_background = cv2.bitwise_and(reversed_sem_img, reversed_sem_img, mask=black_mask)

                result = cv2.bitwise_and(reversed_sem_img, image_with_black_background)

                cv2.imwrite(sem_img_path, result)
            else:
                print('Error: Could not open or find the image.')

            
            if ins_img is not None and result is not None:
                if ins_img.shape == result.shape:

                    panoptic_result = cv2.bitwise_or(ins_img, result)
                    panoptic_filename = f'{file_ins}'
                    panoptic_file_path = os.path.join(pan_dir, panoptic_filename)

                    cv2.imwrite(panoptic_file_path, panoptic_result)

                    print(f'Saved: {panoptic_file_path}')

                else:
                    print(f'Error: Images {file_ins} and {corresponding_file} must have the same dimensions for bitwise operations.')
            else:
                print(f'Error: Could not open or find one of the images: {ins_img_path}, {sem_img_path}')

        else:
            print(f'Warning: No corresponding file found for {file_ins} in the second folder.')

if __name__ == "__main__":
    if osp.exists(pan_dir):
        print("Output directory already exists:", pan_dir)
        # sys.exit(1)
    else:
        os.makedirs(pan_dir)

    main()