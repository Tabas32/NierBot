import numpy as np
from PIL import ImageGrab
import cv2
import time
from directkeys import ReleaseKey, PressKey, W, A, S, D
from grabScreen import grab_screen

def process_img(original_image):
	"""Converts image to gray colors, finds edges and detect circles (bullets)
	returns converted image
	"""
	
	processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
	processed_img = cv2.Canny(processed_img, threshold1=100, threshold2=200)
	#processed_img = cv2.GaussianBlur(processed_img, (3,3), 0 )
	
	# detect circles in the image
	circles = cv2.HoughCircles(processed_img, 
		cv2.HOUGH_GRADIENT, 
		1, 
		10, 
		param1=200,
		param2=16,
		minRadius=6,
		maxRadius=18)
	
	draw_circles(original_image, circles)
	
	return processed_img, circles
	
def draw_circles(img, circles):
	"""Drows circles to image
	param circles is [[[x, y, radius] ....]] (from cv2.HoughCircles())
	"""
	
	if circles is not None:
		circles = np.round(circles[0, :]).astype("int")
	 
		for (x, y, r) in circles:
			cv2.circle(img, (x, y), r, (0, 255, 0), 4)
			
def mark_player(scene):
	procesImg = cv2.cvtColor(scene, cv2.COLOR_BGR2HSV)

	# lowPlayer = np.array([21,20,150])
	# highPlayer = np.array([24,30,255])
	lowPlayer = np.array([92,20,150])
	highPlayer = np.array([98,30,255])

	mask = cv2.inRange(procesImg, lowPlayer, highPlayer)

	imgS, contoursS, hierarchyS = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

	maxArea = 0
	i = 0
	maxIndex = -1
	for cnt in contoursS:
		cntArea = cv2.contourArea(cnt)
		if cntArea > maxArea:
			maxArea = cntArea
			maxIndex = i
		i += 1
	
	if maxIndex > -1:
		return contoursS[maxIndex]
	else:
		return None
	
	
while(True):
	#screen = np.array(ImageGrab.grab(bbox=(0, 25, 640, 420)))
	screen = grab_screen((0, 25, 640, 420))
	new_screen = process_img(screen)
	cnt = mark_player(screen)
	if cnt is not None:
		x,y,w,h = cv2.boundingRect(cnt)
		cv2.rectangle(screen,(x,y),(x+w,y+h),(255,0,0),3)
	
	# new_screen = grab_screen((0, 25, 640, 420))
	# cv2.imshow('window2', new_screen)
	cv2.imshow('window1', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break


 

