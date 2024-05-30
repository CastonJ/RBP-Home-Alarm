import time
import smtplib
import RPi.GPIO as GPIO

TO = "xxxxxx@yahoo.com"  # Put in an email address you want to send a text message to.
GMAIL_USER = "xxxx"  # Email address username
PASS = 'xxxx'  # Password for email address login

SUBJECT = 'Alert!'

GPIO.setmode(GPIO.BCM)
sensors = {
    12: 'Master Window',
    25: 'Outside Garage Door',
    4: 'Sliding Glass Door',
    17: 'Front Door',
    27: 'Back Window',
    22: 'Garage Door'
}

for pin in sensors:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.OUT)
GPIO.output(24, GPIO.HIGH)

def send_mail(text):
    print("Sending text")
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(GMAIL_USER, PASS)
        header = f"To: {TO}\nFrom: {GMAIL_USER}\nSubject: {SUBJECT}\n"
        msg = f"{header}\n{text}\n\n"
        server.sendmail(GMAIL_USER, TO, msg)
    time.sleep(1)
    print("Text sent")

try:
    while True:
        for pin, location in sensors.items():
            if GPIO.input(pin) == 0:
                TEXT = location
                GPIO.output(24, 0)
                send_mail(TEXT)
                time.sleep(100)  # Sleep for 100 seconds
            else:
                time.sleep(0.5)  # Check every 0.5 seconds

            if GPIO.input(pin) == 1:
                GPIO.output(24, 1)

finally:
    GPIO.cleanup(24)