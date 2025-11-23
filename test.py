import cv2
import pytesseract
import re
import sys
                  

carplate_haar_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')
video_capture = cv2.VideoCapture(0)


ret, frame = video_capture.read()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

plaques = carplate_haar_cascade.detectMultiScale(gray, 1.3, 5)
				  
for i, (x, y, w, h) in enumerate(plaques):
	roi_color = frame[y:y + h, x:x + w]
	cv2.putText(frame, str(x) + " " + str(y) + " " + str(w) + " " + str(h),
		(480, 220), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
	r = 400.0 / roi_color.shape[1]
	dim = (400, int(roi_color.shape[0] * r))
	resized = cv2.resize(roi_color, dim, interpolation=cv2.INTER_AREA)
	w_resized = resized.shape[0]
	h_resized = resized.shape[1]
	
	frame[100:100 + w_resized, 100:100 + h_resized] = resized
	cv2.rectangle(roi_color, (x, y), (x + w, y + h), (0, 255, 0), 2)
			
	number = pytesseract.image_to_string(
		resized,
		config='--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

	cv2.imwrite('/tmp/Video_Number_Znak.jpg', resized)

			

