import pyttsx3 #library used text to speech.
import smtplib  # library to send email thorugh a server .
from email.message import EmailMessage #email details
import serial, time # for serial communication between arduino and raspberry pi
import requests # for gps module
import folium  # for gps module
import RPi.GPIO as GPIO # for using GPIO pins


def SendEmail(data): # function to send emails 

    Sender_Email = "gurpartap332211@gmail.com"
    Reciever_Email = "gurpartapnitin2002@gmail.com"
    Password = "gurpartapnitin"
#-------------------------------------MESSAGE-----------------------------------------------------------
    newMessage = EmailMessage() #object
    newMessage['Subject'] = "Emergency Message From Gurpartap"
    newMessage['From'] = Sender_Email
    newMessage['To'] = Reciever_Email
    getLoc()# function to get location of accidents from gps module
    location = data['loc'].split(',')
    lat = float(location[0])
    Lng = float(location[1])
    Message='Please help me, I Am in emergency. my Location is Long:'+str(Lng)+" Lat:"+str(lat)
    newMessage.set_content(Message) # to pass a message we use this function

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp: # server for gmail
        smtp.login(Sender_Email, Password) # ceredentials for email
        smtp.send_message(newMessage)

def SerialCommRead(): # function to read the serial communication from arduino nano 33 iot
    global ser # declared function
    if ser.in_waiting>0: # condition if their is any value
        Val=ser.readline().decode("ascii").rstrip() # sending data in ascii code from arduino nano 33 iot
        return Val

def getLoc(): # gives location of accident
    ser = serial.Serial('/dev/ttyS0', 9600, timeout=1) #9600 is baud rate/ ttyS0 is used for on board serial communication/ttyacm0
    ser.flush()
    data = ser.readline().decode('utf-8').rstrip() # its in uni code as it is sending from same  board
    if len(data)>0: # condition if it gives a value to it will split the value and give it's value equal to lat and lng
        location = data['loc'].split(',')
        lat = float(location[0])
        Lng = float(location[1])

#-------------------------------------------------------Main Code---------------------------------------------------------------------
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(10,GPIO.IN,pull_up_down=GPIO.PUD_UP)

ser=serial.Serial('/dev/ttyACM0',9600)# serial object which will be used to convert my text to speech 
ser.flush()
engine = pyttsx3.init()
engine.setProperty("rate", 130)# speed at which you want the message to be delivered.
Flag=1
while True:
    res = requests.get('https://ipinfo.io/')# have to go through a link as without it sometimes the gps module give you a loaction sometimes it doesn't
    data = res.json()# data some in json file
    ser.flush()
    Value=SerialCommRead()# reads serial data through Uart
    if Value=="Y":
        Tim=1
        engine.say("Accident Occur ")
        engine.runAndWait()# it wait until the full sentence has been spoken 
        engine.say("Press Reset Button")
        engine.runAndWait()
        engine.say("To Stop Email")
        engine.runAndWait()
        print("Waiting Button")
        while Tim<30:
            print("waiting...")
            Flag2=1
            if GPIO.input(10)==GPIO.LOW:
                Flag2=0
                Val='N'
                break
            time.sleep(1)
            Tim+=1

        while Flag2==1:
            engine.say("Help")
            engine.runAndWait()
            if Flag==1:
                SendEmail(data)
                print("Email Sent")
                Flag=2

    elif Value=="N":
        Flag=1
        print("Normal State")
    

