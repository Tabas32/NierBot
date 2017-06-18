import numpy as np
from PIL import ImageGrab
import cv2
import time
from directkeys import ReleaseKey, PressKey, W, A, S, D

def process_img(original_image):
	processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
	processed_img = cv2.Canny(processed_img, threshold1=100, threshold2=200)
	
	# detect circles in the image
	circles = cv2.HoughCircles(processed_img, 
		cv2.HOUGH_GRADIENT, 
		1, 
		10, 
		param1=200,
		param2=16,
		minRadius=6,
		maxRadius=18)
	
	draw_circles(processed_img, circles)
	
	return processed_img
	
#circles from HoughCircles
def draw_circles(img, circles):
	if circles is not None:
		circles = np.round(circles[0, :]).astype("int")
	 
		for (x, y, r) in circles:
			cv2.circle(img, (x, y), r, (255, 255, 255), 4)

while(True):
	screen = np.array(ImageGrab.grab(bbox=(0, 25, 640, 420)))
	new_screen = process_img(screen)
	
	cv2.imshow('window2', new_screen)
	#cv2.imshow('window1', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))
	if cv2.waitKey(25) & 0xFF == ord('q'):
		cv2.destroyAllWindows()
		break


 

