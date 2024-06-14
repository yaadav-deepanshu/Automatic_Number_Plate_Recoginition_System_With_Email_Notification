The Automatic Number Plate Recognition (ANPR) System with Email Notification is a tool designed to detect and recognize vehicle number plates from images using OpenCV and machine learning techniques. Upon successfully recognizing a number plate, the system sends an email notification with the detected number plate details. This system is useful for various applications such as security monitoring, parking management, and toll collection.
Features :-

    Real-time Number Plate Detection: Processes images to detect and recognize vehicle number plates.
    Email Notifications: Sends an email with the vehicle's number plate details upon successful recognition.
    Advanced Image Processing: Utilizes OpenCV for image processing to enhance recognition accuracy.
    Machine Learning Integration: Incorporates KNN-based machine learning for character recognition.

Installation

    Clone the Repository:

    bash

git clone https://github.com/yourusername/ANPR-Email-Notification.git
cd ANPR-Email-Notification

Install the Required Dependencies:

steps:
    pip install opencv-python
    pip install numpy
    pip install secure-smtplib
    pip install pathlib

    Prepare Email Notification Settings:
        Edit the send_email function in main.py and replace 'Your_Email@gmail.com' and 'Enter_your_gmail_password' with your email credentials.

    Place the Input Image:
        Ensure the image you want to process is named 1.png and placed in the root directory of the project.

Usage

    Run the ANPR System:

    bash

    python main.py

    The system will:
        Read the image file 1.png.
        Detect and recognize the number plate.
        Draw a red rectangle around the detected plate.
        Display the processed image with the detected number plate.
        Send an email notification with the recognized number plate details.

Configuration

    Email Template: The email template is read from an index.html file. Ensure this file exists in the root directory.
    SMTP Settings: The email notification uses Gmail's SMTP server. Ensure you have allowed less secure apps or set up an app password if using 2FA on your Gmail account.

Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.
License

This project is licensed under the MIT License. See the LICENSE file for details.
Additional Files
requirements.txt

txt

numpy
opencv-python


html :-
index.html

<!DOCTYPE html>
<html>
<body>
    <h2>Vehicle Arrival Notification</h2>
    <p>Dear ${name},</p>
    <p>The vehicle with number plate <strong>${vehicle_number}</strong> has arrived at the main gate.</p>
</body>
</html>
