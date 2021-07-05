import numpy as np
import sys
import cv2
import json
import pytesseract 
from flask import Flask, render_template, request, jsonify

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def get_contour_precedence(contour, cols):
  tolerance_factor = 10
  origin = cv2.boundingRect(contour)
  return ((origin[1] // tolerance_factor) * tolerance_factor) * cols + origin[0]

rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (14,10))

def cashier_chk(upper,micr):
    gr = cv2.cvtColor(np.array(upper), cv2.COLOR_BGR2GRAY)
    ed = cv2.Canny(gr,30,200)
    dil = cv2.dilate(ed, rect_kernel, iterations = 1)
    cont, hierarchy = cv2.findContours(dil, 
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(gr, cont, -1, (0, 255, 0), 1)
    cont.sort(key=lambda x:get_contour_precedence(x, upper.shape[1]))
    #cv2.imshow('cont',gr)
    #cv2.waitKey(0)

    check_details ={}
    i=0
    flag_payee=0
    flag_info =0
    flag_dollar =0
    flag_bank = 0
    flag_amount=0
    flag_date =0
    cropped = upper.copy()
    n = len(cont)
    
    for cnt in cont:
        i = i+1
        x, y, w, h = cv2.boundingRect(cnt)
        crop = cropped[y:y + h, x:x + w]
        #cv2_imshow(crop)
        text = pytesseract.image_to_string(crop,config= r'--psm 6')
        l = len(text)
        if (x<100 and y<100 and l>6 and w<400):
            check_details['bank']=text
        elif (((l>=10) and (i<=4)) and ((flag_date ==0) and x >500) ):
            if (l>12):
                text = text[4:]
                check_details['date'] = text
                flag_date =1
        elif (x<300 and y>100 and flag_amount==0 and w > 400 ):
            flag_amount=1
            s = crop.shape
            m = int(s[1])-50
            crop = crop[0:int(s[0]),90:m]
            text = pytesseract.image_to_string(crop,config= r'--psm 6')
            check_details['amount'] = text
        elif ((l>5 and flag_dollar ==0) and (x>500 and h<70) and (flag_date==1 and w>100)):
            check_details['dollar'] = text
            flag_dollar =1
        elif (x<300 and flag_amount==1 and flag_dollar ==1 and flag_payee==0 and l>6):
            flag_payee = 1
            check_details['payee'] = text
        elif ((i>n-2 and flag_payee==1) and (x>400 and y > 250)):
            check_details['sign'] = text
        else:
            if (flag_info ==1):
                check_details['info_2'] = text
            else:
                check_details['info'] = text
                flag_info =1


    micr_code =  pytesseract.image_to_string(micr, lang='mcr')
    check_details['micr'] = micr_code

    for key in check_details:
        value = check_details[key]
        l = len(value)
        n = l-2
        #print(key)
        value = value[:n]
        m = len(value)
        for i in range (m-1):
            if value[i]=='\n':
                #print("yes")
                list1 = list(value)
                list1[i] = ', '
                value = ''.join(list1)
                
            check_details[key]=value

    return (check_details)
