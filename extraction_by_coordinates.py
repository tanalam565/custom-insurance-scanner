import pytesseract
import cv2
import numpy as np
import re
from PIL import Image, ImageEnhance
from openpyxl import Workbook
 
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
 
image_path = 'applicationImage\\Nationwide_WIP.png'
img = cv2.imread(image_path)
 
def extract_text_from_coords(img, coords):
 
    #Zoom image:
    # Get original dimensions
    height, width = img.shape[:2]
 
    # Define zoom factor (e.g., 2 for 2x zoom)
    zoom_factor = 2
 
    # Calculate new dimensions
    new_width = int(width * zoom_factor)
    new_height = int(height * zoom_factor)
 
    # Resize the image using cv2.resize()
    # INTER_LINEAR is a good default interpolation method for upscaling (zooming in)
    #zoomed_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
 
    x, y, w, h = coords
    #Use NumPy array slicing to extract the defined rectangular region from the loaded image.
    roi = img[y:y+h, x:x+w]
    gray_roi=cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    text=pytesseract.image_to_string(thresh,lang='eng',config='--psm 6 -l eng')
   
    # cleaned_string = re.sub(r'[^a-zA-Z0-9$ ]', '', text.strip())
    # return cleaned_string
    return text.strip()
 
def parse_text(text):
    return text.replace(')','').replace("'","").replace(",","").replace("’","")
 
 
insuranceCompany_coordinates = (155, 33, 145, 30)
policyNumber_coordinates=(454,77,117,19)
datePrepared_coordinates=(610,77,92,20)
insurerName_coordinates=(439,198,250,20)
insurerAddress_coordinates=(434,214,250,20)
insurerCityState_coordinates=(434,230,250,20)
insuranceAmount_coordinates=(639,630,150,20)
 
print('Insurance Company->',parse_text(extract_text_from_coords(img,insuranceCompany_coordinates)))
print('Policy Number->',extract_text_from_coords(img,policyNumber_coordinates))
print('Date Prepared->',extract_text_from_coords(img,datePrepared_coordinates))
print('Insurer Name->',extract_text_from_coords(img,insurerName_coordinates))
print('Insurer Address->',extract_text_from_coords(img,insurerAddress_coordinates))
print('Insurer City State->',parse_text(extract_text_from_coords(img,insurerCityState_coordinates)))
print('Insurance Amount->',parse_text(extract_text_from_coords(img,insuranceAmount_coordinates)))