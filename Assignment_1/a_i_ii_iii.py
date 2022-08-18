#%% import numpy as np
from PIL import Image
import numpy as np
from statistics import median
import matplotlib.pyplot as plt
import math

#%%
image = np.array(Image.open("Image_1.png"))             # Load the image

#%%
in1 = int(input('1 for Rotate, 2 for Homography Transform: '))  # Ask the user to enter the angle of rotation

if (in1==1):
    angle = float(input('Enter angle in Degrees : '))
    anglerad = math.pi*angle/180
    in2 = int(input('1 for other transform, 2 for only rotation: '))
    if (in2 == 1):
        h13 = float(input("Enter h13 (translation in x): "))
        h23 = float(input("Enter h23 (translation in y): "))
        h31 = float(input("Enter h31 (3D movement): "))
        h32 = float(input("Enter h32 (3D movement): "))
        
        A = [[math.cos(anglerad), math.sin(anglerad), h13], [-math.sin(anglerad), math.cos(anglerad), h23], [h31, h32, 1]]
    else:
        A = [[math.cos(anglerad), math.sin(anglerad),0],[-math.sin(anglerad),math.cos(anglerad),0],[0,0,1]];
else:
    h11 = float(input("Enter h11 (Scaling in x): "))
    h12 = float(input("Enter h12 (shearing along x): "))
    h13 = float(input("Enter h13 (translation in x): "))
    h21 = float(input("Enter h21 (shearing along y): "))
    h22 = float(input("Enter h22 (Scaling in x): "))
    h23 = float(input("Enter h23 (translation in y): "))
    h31 = float(input("Enter h31 (3D movement): "))
    h32 = float(input("Enter h32 (3D movement): "))
    h33 = float(input("Enter h11 (Scaling in x and y) "))
    A = [[h11, h12, h13], [h21, h22, h23], [h31, h32, h33]]

A = np.array(A)

#%%
# Is it color or grayscale
b = image.shape;
if b[2]==3:
    a1 = 1

#%%
trans = np.array([[1,0,-b[1]/2], [0,1,-b[0]/2], [0,0,1]]) # Bring the origin to the center by this Matrix
outx = np.zeros((b[0],b[1])) 
outy = np.zeros((b[0],b[1])) 

for i in range(0,b[0]):
    for j in range(0,b[1]):
        dummy = np.array([j+1, i+1, 1])
        new  = A @ trans @ dummy
        outx[i,j] = np.round(new[0]/new[2]) # x''/w
        outy[i,j] = np.round(new[1]/new[2]) # y''/w

#%%        
# Forming the transformed image
minoutx = int(np.min(outx))
minouty = int(np.min(outy))

maxoutx = int(np.max(outx))
maxouty = int(np.max(outy))

f = np.zeros((maxouty + abs(minouty) + 1, maxoutx + abs(minoutx) + 1,3))

for i in range(0, b[0]):
    for j in range(0, b[1]):
        f[int(outy[i,j])+abs(minouty),int(outx[i,j])+abs(minoutx),0] = image[i,j,0]
        if a1 == 1:
            f[int(outy[i,j])+abs(minouty),int(outx[i,j])+abs(minoutx),1] = image[i,j,1];
            f[int(outy[i,j])+abs(minouty),int(outx[i,j])+abs(minoutx),2] = image[i,j,2];
 
#%%
# Fill the gaps
#Fill in the gaps By using Median Filter
b1 = f.shape;
for i in range(2,b1[0]-2):
    for j in range(2,b1[1]-2):
        
        if f[i,j,0]==0:
            f[i,j,0] = median([f[i-1,j-1,0],f[i-1,j,0],f[i-1,j+1,0],f[i,j-1,0],f[i,j,0],f[i,j+1,0],f[i+1,j-1,0],f[i+1,j,0],f[i+1,j+1,0]]);
        if a1 == 1:
            f[i,j,1] = median([f[i-1,j-1,1],f[i-1,j,1],f[i-1,j+1,1],f[i,j-1,1],f[i,j,1],f[i,j+1,1],f[i+1,j-1,1],f[i+1,j,1],f[i+1,j+1,1]]);
            f[i,j,2] = median([f[i-1,j-1,2],f[i-1,j,2],f[i-1,j+1,2],f[i,j-1,2],f[i,j,2],f[i,j+1,2],f[i+1,j-1,2],f[i+1,j,2],f[i+1,j+1,2]]);


#%%
# Display the Images  
plt.imshow(f)
plt.show
plt.title("Transformed Image")
plt.savefig("./Transformed_Image.jpg")