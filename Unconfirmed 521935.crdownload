import pyttsx3
import smtplib
from email.message import EmailMessage
import serial, time
import requests
import folium
import RPi.GPIO as GPIO


def SendEmail(data):
    Sender_Email = "gurpartap332211@gmail.com"
    Reciever_Email = "gurpartapnitin2002@gmail.com"
    Password = "gurpartapnitin"

    newMessage = EmailMessage()                         
    newMessage['Subject'] = "Emergency Message From Gurpartap" 
    newMessage['From'] = Sender_Email                   
    newMessage['To'] = Reciever_Email
    getLoc()
    location = data['loc'].split(',')
    lat = float(location[0])
    Lng = float(location[1])
    Message='Please help me, I Am in emergency. my Location is Long:'+str(Lng)+" Lat:"+str(lat) 
    newMessage.set_content(Message)
                           
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Sender_Email, Password)              
        smtp.send_message(newMessage)


def getLoc():
    ser = serial.Serial('/dev/ttyS0', 9600, timeout=1) #9600 is baud rate(must be same with that of NodeMCU)
    ser.flush()
    data = ser.readline().decode('utf-8').rstrip()
    if len(data)>0:
        location = data['loc'].split(',')
        lat = float(location[0])
        Lng = float(location[1])
        

def SerialCommRead():
    global ser
    if ser.in_waiting>0:
        Val=ser.readline().decode("ascii").rstrip()
        return Val
    


# Main Code
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(10,GPIO.IN,pull_up_down=GPIO.PUD_UP)

ser=serial.Serial('/dev/ttyACM0',9600)
ser.flush()
engine = pyttsx3.init()
engine.setProperty("rate", 130)
Flag=1
while True:
    res = requests.get('https://ipinfo.io/')
    data = res.json()
    ser.flush()
    Val=SerialCommRead()
    if Val=="Y":
        Tim=1
        engine.say("Accident Occur ")
        engine.runAndWait()
        engine.say("Press Reset Button")
        engine.runAndWait()
        engine.say("To Stop Email")
        engine.runAndWait()
        print("Waiting Button")
        while Tim<3:
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
                
    elif Val=="N":
        Flag=1
        print("Normal State")
    

