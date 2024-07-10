import cv2
import pytesseract
import mysql.connector
import re
import sys

cnx = mysql.connector.connect(user='arm', password='procedure',
                              host='localhost',
                              database='crm')

try:
	cursor = cnx.cursor()
	query = ("INSERT INTO weight_memory(k,v) VALUES(2, NULL);")
	cursor.execute(query)
except:
	print("Ключ уже создан в оперативной памяти")                              

carplate_haar_cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')
video_capture = cv2.VideoCapture(0)

while True:
	ret, frame = video_capture.read()
	try:
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	except:
		continue
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
		number = re.sub(r'\s+', '', number)
		number = re.sub(r'\n', '', number)
		if len(number) >= 5:
			#cv2.imwrite('/tmp/Video_Number_Znak.jpg', carplate_extract_img_gray)
			print('Номер авто: ', number)
			cursor = cnx.cursor()
			query = ("UPDATE weight_memory SET v = '" + number + "' WHERE k = 2;")
			cursor.execute(query)
			
		video_capture = cv2.VideoCapture(0)

	#cv2.imshow('Video', frame)
	
video_capture.relase()
cv2.destroyAllWindows()
