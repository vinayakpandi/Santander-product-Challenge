from tensorflow.keras.preprocessing.image import load_img
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing.image import img_to_array
import io
from PyPDF2 import PdfFileReader 
from tensorflow.keras.models import load_model
from tabula import read_pdf
import math
with io.open('test.pdf',mode = "rb") as f:
  input_pdf = PdfFileReader(f)
  media_box = input_pdf.getPage(0).mediaBox
min_pt = media_box.lowerLeft
max_pt = media_box.upperRight
image = load_img('test.jpg',target_size = (224,224))
image = img_to_array(image)/255.0
image = np.expand_dims(image,axis = 0)

borderless_model = load_model("/content/sample_data/Table_Detector.h5",compile=False)
borderless_preds = borderless_model.predict(image)[0]

(borderless_startX,borderless_startY,borderless_endX,borderless_endY) = borderless_preds
from cv2 import cv2
image = cv2.imread('test.jpg')

image_cp = image.copy()

(h,w) = image.shape[:2]

borderless_startX = int(borderless_startX*w)
borderless_startY = int(borderless_startY*h)
borderless_endX = int(borderless_endX*w)
borderless_endY = int(borderless_endY*h)
final_pdf_coordinates = str(math.floor(borderless_startY/2)-5)+","+str(math.floor(min_pt[0]))+"," + str(math.floor(borderless_endY/2)) + ","+ str(math.ceil(max_pt[0]))

#final_pdf_coordinates = str(math.floor(borderless_startY/2)-5)+","+str(math.floor(min_pt[0]))+","str(math.floor(borderless_endY/2))) + "," str(math.ceil(max_pt[0]))

print("FINAL_TABLE_COORDINATES: ",final_pdf_coordinates)

cv2.rectangle(image,(int(min_pt[0]),borderless_startY,),(int(max_pt[0]*2),borderless_endY),(0,255,0),2)

imS = cv2.resize(image,(560,640))

tables = read_pdf('test.pdf',area = [final_pdf_coordinates],stream = True,output_format = "dataframe",pandas_options = {'header':None})
if len(tables) > 0:
	df_concat = pd.DataFrame(np.concatenate(tables))
	#df_concat,currency_code,total_amount = dataframe_processing(df)
else:
  print("No table")
  #df_concat = pd.DataFrame(tables)

df_concat.head()
#cv2.imwrite('op.jpg', imS)
#cv2.imshow("model_output",imS)

#cv2.waitkey(0)