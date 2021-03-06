import imutils
import cv2

class ShapeDetector:
	def __init__(self):
		pass

	def detect(self, c):
		shape = "not circle"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * peri, True)
		if len(approx) > 5:
			shape = "circle"

		return shape

image = cv2.imread('example.png')

resized = imutils.resize(image, width=2000)
ratio = image.shape[0] / float(resized.shape[0])

gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
sd = ShapeDetector()
for c in cnts:
    if sd.detect(c) == "circle" :
	    M = cv2.moments(c)
	    cX = int((M["m10"] / M["m00"]) * ratio)
	    cY = int((M["m01"] / M["m00"]) * ratio)
	    shape = sd.detect(c)
	    c = c.astype("float")
	    c *= ratio
	    c = c.astype("int")
	    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
	    cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
	    	0.5, (0, 255, 0), 2)
	    cv2.imshow("Image", image)
	    cv2.waitKey(0)
en = c
for c in cnts:
    if sd.detect(c) == "circle" :
        c = c.astype("float")
        c *= ratio
        c = c.astype("int")
        area = cv2.contourArea(c) 
        perimeter = cv2.arcLength(c,True)
        enarea = cv2.contourArea(en)
        enperimeter = cv2.arcLength(en,True)
        #pi = perimeter*perimeter/4*area
        if area/perimeter*perimeter > enarea/enperimeter*enperimeter:
            en = c
M = cv2.moments(en)
cX = int((M["m10"] / M["m00"]))
cY = int((M["m01"] / M["m00"]))
cv2.drawContours(image, [en], -1, (0, 0, 255), 2)
cv2.putText(image, sd.detect(en), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
            0.5  , (0, 0, 255), 2)
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()