#importing the libraries
import pytesseract
from PIL import Image
import sys
import cv2
import numpy as np
import sys
import json
from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api

#importing the functions for different type of cheques
from persnal import *
from cashier import *

#initializing the API
app = Flask(__name__)
api = Api(app)

#defining the path for tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

#sorting function to sort contours from top to bottom and left to right
def get_contour_precedence(contour, cols):
  tolerance_factor = 10
  origin = cv2.boundingRect(contour)
  return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]

# for the personal check
@app.route('/personal', methods =['POST'])
def cheque_details():
  #getting the image
  file = request.files['image']
  chk = Image.open(file.stream)

  #preprocess the image
  chk = cv2.cvtColor(np.array(chk), cv2.COLOR_BGR2RGB)
  chk = cv2.resize(chk,(1000,458))
  gray = cv2.cvtColor(np.array(chk), cv2.COLOR_RGB2GRAY)
  edged = cv2.Canny(gray,40,200)
  rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (14,10))
  #ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU| cv2.THRESH_BINARY_INV)
  dilation = cv2.dilate(edged, rect_kernel, iterations = 2)
  contours, hierarchy = cv2.findContours(dilation, 
      cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

  #sorting the contours
  contours.sort(key=lambda x:get_contour_precedence(x, chk.shape[1]))

  #cropping the check in an image
  for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if(w>900 and h>=380):
      crop = chk[y+10:y + h-10, x+10:x + w-10]

  # checking for another outer edge
  another = 0
  gr = cv2.cvtColor(np.array(crop), cv2.COLOR_RGB2GRAY)
  ed = cv2.Canny(gr,30,200)
  dil = cv2.dilate(ed, rect_kernel, iterations = 1)
  cont, hierarchy = cv2.findContours(dil, 
      cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  cv2.drawContours(gr, cont, -1, (0, 255, 0), 1)
  cont.sort(key=lambda x:get_contour_precedence(x, chk.shape[1]))
  for cnt1 in cont:
    x1, y1, w1, h1 = cv2.boundingRect(cnt1)
    if(w1>800 and h1>350):
      croped = crop[y1+15:y1 + h1-10, x1+15:x1 + w1-15]
      another =1

  if another ==1:
    crop = croped.copy()

  #cropping cheque into two parts
  a = crop.shape
  start = int(a[0]-a[0]*0.12)
  end = int(a[0])
  micr = crop[start:end,0:a[1]]
  upper = crop[0:start,0:a[1]]
  upper = upper[:,15:]
  
  #using the personal_chk function getting details and returning them
  check_details = personal_chk(upper, micr)
  return (jsonify(check_details))


#for the cashier check
@app.route('/cashier', methods =['POST'])
def cheque_details_sec():
  #getting the image
  file = request.files['image']
  chk = Image.open(file.stream)

  #preprocess the image
  chk = cv2.cvtColor(np.array(chk), cv2.COLOR_BGR2RGB)
  chk = cv2.resize(chk,(1000,458))
  gray = cv2.cvtColor(np.array(chk), cv2.COLOR_RGB2GRAY)
  edged = cv2.Canny(gray,40,200)
  rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (14,10))
  #ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU| cv2.THRESH_BINARY_INV)
  dilation = cv2.dilate(edged, rect_kernel, iterations = 2)
  contours, hierarchy = cv2.findContours(dilation, 
      cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

  #sorting the contours
  contours.sort(key=lambda x:get_contour_precedence(x, chk.shape[1]))

  #cropping the check in an image
  for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if(w>900 and h>=380):
      crop = chk[y+10:y + h-10, x+10:x + w-10]

  #checking for another outer edge
  another = 0
  gr = cv2.cvtColor(np.array(crop), cv2.COLOR_RGB2GRAY)
  ed = cv2.Canny(gr,30,200)
  dil = cv2.dilate(ed, rect_kernel, iterations = 1)
  cont, hierarchy = cv2.findContours(dil, 
      cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  cv2.drawContours(gr, cont, -1, (0, 255, 0), 1)
  cont.sort(key=lambda x:get_contour_precedence(x, chk.shape[1]))
  for cnt1 in cont:
    x1, y1, w1, h1 = cv2.boundingRect(cnt1)
    if(w1>800 and h1>350):
      croped = crop[y1+15:y1 + h1-10, x1+15:x1 + w1-15]
      another =1

  if another ==1:
    crop = croped.copy()

  #cropping cheque into two parts
  a = crop.shape
  start = int(a[0]-a[0]*0.12)
  end = int(a[0])
  micr = crop[start:end,0:a[1]]
  upper = crop[0:start,0:a[1]]
  upper = upper[:,15:]
  
  #using the cashier_chk function getting details and returning them
  check_details = cashier_chk(upper, micr)
  return (jsonify(check_details))

if __name__ == "__main__":
    app.run(debug=True)
