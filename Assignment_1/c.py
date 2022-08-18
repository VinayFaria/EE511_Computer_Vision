# Reference: https://www.youtube.com/watch?v=8oFRmdDum5k

# Image Mosaicing
import cv2
import os

images_Folder = 'final_5_images'
list_of_images_name = os.listdir(images_Folder)

images = []
print(f'Total number of images detected: {len(list_of_images_name)}')
print(list_of_images_name)
for image_name in list_of_images_name:
    location = "./" + images_Folder + "/" + image_name
    image_data = cv2.imread(location)
    p = 0.5
    w = int(image_data.shape[1] * p)
    h = int(image_data.shape[0] * p)
    image_data = cv2.resize(image_data, (w, h)) # Scaling down original image
    images.append(image_data)
    
stitcher = cv2.Stitcher.create() # instantiating Stitcher class
status, result = stitcher.stitch(images)    # calling stitch function or method from stitcher
if status == cv2.STITCHER_OK:
    print('Stiching successful')
    cv2.imshow(list_of_images_name[0], result)
    cv2.waitKey(1)
else:
    print('Stiching failed')