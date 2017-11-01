import numpy as np
import cv2
import time

# Create a black image
img = np.zeros((512,512,3), np.uint8)

# Draw a diagonal blue line with thickness of 5 px
for i in range(10):
    img = cv2.line(img,(0,0),(i*10,511),(255,0,0),5)
    cv2.imshow("image", img)
    time.sleep(0.5)
cv2.waitKey(0)
cv2.destroyAllWindows()
#time.sleep(2)