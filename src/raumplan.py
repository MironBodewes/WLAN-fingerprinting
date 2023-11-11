import matplotlib.pyplot as plt
from skimage import io

img = io.imread("raumplan.png")
img=img[620:1120,:,:]
io.imsave("raumplanS117.png",img)
plt.imshow(img)
plt.show()
print(img.dtype,img.shape)
