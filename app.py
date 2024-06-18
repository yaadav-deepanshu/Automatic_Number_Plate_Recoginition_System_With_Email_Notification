from flask import Flask, request, render_template, jsonify
import cv2
import numpy as np
import os
import DetectChars
import DetectPlates
import PossiblePlate
import smtplib as smtp
from email.message import EmailMessage
from string import Template
from pathlib import Path

app = Flask(__name__)

SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    if file:
        img = np.fromstring(file.read(), np.uint8)
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)
        plate_number = detect_license_plate(img)
        return jsonify({'plate_number': plate_number})
    return "File upload failed"

def detect_license_plate(imgOriginalScene):
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()
    if not blnKNNTrainingSuccessful:
        return "KNN training failed"

    if imgOriginalScene is None:
        return "Image not read from file"

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)
    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)

    if len(listOfPossiblePlates) == 0:
        return "No license plates detected"
    else:
        listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)
        licPlate = listOfPossiblePlates[0]
        if len(licPlate.strChars) == 0:
            return "No characters detected"
        drawRedRectangleAroundPlate(imgOriginalScene, licPlate)
        writeLicensePlateCharsOnImage(imgOriginalScene, licPlate)
        cv2.imwrite("static/imgOriginalScene.png", imgOriginalScene)
        send_email(licPlate.strChars)
        return licPlate.strChars

def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):
    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)
    p2fRectPoints = np.int0(p2fRectPoints)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), SCALAR_RED, 2)

def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate):
    ptCenterOfTextAreaX = 0
    ptCenterOfTextAreaY = 0
    ptLowerLeftTextOriginX = 0
    ptLowerLeftTextOriginY = 0
    sceneHeight, sceneWidth, sceneNumChannels = imgOriginalScene.shape
    plateHeight, plateWidth, plateNumChannels = licPlate.imgPlate.shape
    intFontFace = cv2.FONT_HERSHEY_SIMPLEX
    fltFontScale = float(plateHeight) / 30.0
    intFontThickness = int(round(fltFontScale * 1.5))
    textSize, baseline = cv2.getTextSize(licPlate.strChars, intFontFace, fltFontScale, intFontThickness)
    ( (intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg ) = licPlate.rrLocationOfPlateInScene
    intPlateCenterX = int(intPlateCenterX)
    intPlateCenterY = int(intPlateCenterY)
    ptCenterOfTextAreaX = int(intPlateCenterX)
    if intPlateCenterY < (sceneHeight * 0.75):
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(round(plateHeight * 1.6))
    else:
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(round(plateHeight * 1.6))
    textSizeWidth, textSizeHeight = textSize
    ptLowerLeftTextOriginX = int(ptCenterOfTextAreaX - (textSizeWidth / 2))
    ptLowerLeftTextOriginY = int(ptCenterOfTextAreaY + (textSizeHeight / 2))
    cv2.putText(imgOriginalScene, licPlate.strChars, (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY), intFontFace, fltFontScale, SCALAR_YELLOW, intFontThickness)

def send_email(vehicle_number):
    html = Template(Path("index.html").read_text())
    email = EmailMessage()
    email_addr = 'yaadav.practice@gmail.com'
    email_passwd = 'fkus bmnu zpla nnir'
    email['From'] = email_addr
    email['To'] = 'yaadav.deepanshu@gmail.com'
    email['Subject'] = "Notification: Vehicle Arrival at Main Gate The vehicle's number is [{}]".format(vehicle_number)
    email.set_content(html.substitute({"name": "Your Name", "vehicle_number": vehicle_number}), "html")
    connection = smtp.SMTP_SSL('smtp.gmail.com', 465)
    connection.login(email_addr, email_passwd)
    connection.send_message(email)
    connection.close()

if __name__ == "__main__":
    app.run(debug=True)
