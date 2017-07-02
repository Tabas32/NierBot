import win32gui, win32api, win32con, win32ui
import numpy as np
import cv2

def grab_screen(region = None):
	winHandle = win32gui.GetDesktopWindow()
	
	if region:
		left, top, right, bottom  = region
		width = right - left
		height = bottom - top
	else:
		top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
		left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
		width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
		height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
	
	winDC = win32gui.GetWindowDC(winHandle)
	sourceDC = win32ui.CreateDCFromHandle(winDC)
	memoryDC = sourceDC.CreateCompatibleDC()
	
	bitmap = win32ui.CreateBitmap()
	bitmap.CreateCompatibleBitmap(sourceDC, width, height)
	
	memoryDC.SelectObject(bitmap)
	memoryDC.BitBlt((0,0), (width, height), sourceDC, (left, top), win32con.SRCCOPY)
	
	bitmapBuffer = bitmap.GetBitmapBits(True)
	image = np.fromstring(bitmapBuffer, dtype='uint8')
	image.shape = (height, width, 4)
	
	sourceDC.DeleteDC()
	memoryDC.DeleteDC()
	win32gui.ReleaseDC(winHandle, winDC)
	win32gui.DeleteObject(bitmap.GetHandle())
	
	return cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)