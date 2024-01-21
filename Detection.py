import cv2
import numpy as np
import easyocr

def TextDetection(platepath : str) :
	reader = easyocr.Reader(['en'])
	img = cv2.imread(platepath)
	results = reader.readtext(img)
	plate_number = ""
	for res in results:
		letter = res[1]
		plate_number += letter
	return plate_number

def ObjectFinder(bin_img, real_img) :
	objects_list = cv2.findContours(bin_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	parents_idx_list = [objects_list[1][0][i][3] for i in range(0, len(objects_list[1][0])) if objects_list[1][0][i][3] != -1]
	parents_idx_list = np.unique(np.array(parents_idx_list)).tolist()
	counter = 0
	path_list = []
	for idx in parents_idx_list :
		perimeter = cv2.arcLength(objects_list[0][idx], True)
		polygon = cv2.approxPolyDP(objects_list[0][idx], 10, True)
		if len(polygon) == 4 :
			mask1 = np.zeros(bin_img.shape, np.uint8)
			cv2.fillConvexPoly(mask1, objects_list[0][idx], 255)
			x, y, w, h = cv2.boundingRect(objects_list[0][idx])
			cropped = cv2.bitwise_and(real_img, real_img, mask = mask1)[y:y+h, x:x+w]
			cv2.imwrite("cropped_results/" + str(counter) + ".png", cropped)
			path_list.append("cropped_results/" + str(counter) + ".png")
			counter += 1
	return path_list

def Method1(gray_img, th) :
	gray_img_filtered = cv2.bilateralFilter(gray_img, -1, 20, 20)
	if th != None:
		threshold_from_otsu, bin_tozero_img = cv2.threshold(gray_img_filtered, th, 255, cv2.THRESH_TOZERO)
	else :
		threshold_from_otsu, bin_tozero_img = cv2.threshold(gray_img_filtered, 0, 255, cv2.THRESH_TOZERO + cv2.THRESH_OTSU)
	return cv2.adaptiveThreshold(bin_tozero_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 3, 4)

def Method2(gray_img, th) :
	gray_img_filtered = cv2.bilateralFilter(gray_img, -1, 20, 20)
	threshold_from_otsu, bin_tozero_img = cv2.threshold(gray_img_filtered, 0, 255, cv2.THRESH_TOZERO + cv2.THRESH_OTSU)
	return cv2.Canny(gray_img_filtered, threshold_from_otsu / 2, threshold_from_otsu)

def Method3(gray_img, th) :
	gray_img_filtered = cv2.bilateralFilter(gray_img, -1, 20, 20)
	return cv2.Laplacian(gray_img_filtered, -1)

def PlateDetection(imagepath : str, Method, progress, th = None) :
	img = cv2.imread(imagepath)
	progress['value'] = 10
	result = Method(cv2.cvtColor(img, cv2.COLOR_RGB2GRAY), th)
	path_list = ObjectFinder(result, img)
	progress['value'] = 40
	for path in path_list :
		plate_number = TextDetection(path)
		progress['value'] += 30 / len(path_list)
		if len(plate_number) != 0 :
			return plate_number
	return ""

