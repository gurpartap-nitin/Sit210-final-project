#define ECHO 2
#define TRIG 3
#define FS 4
#define Buzz 5


void setup() {
  pinMode(FS,INPUT_PULLUP);   
  pinMode(ECHO,INPUT);
  pinMode(TRIG,OUTPUT);   
  pinMode(Buzz,OUTPUT);
  Serial.begin(9600);
}


void loop() {
    
     digitalWrite(TRIG, LOW);  
     delayMicroseconds(2); 
     digitalWrite(TRIG, HIGH);
     delayMicroseconds(10); 
     digitalWrite(TRIG, LOW);
     long duration,distance;
     duration = pulseIn(ECHO, HIGH);
     distance = (duration/2) / 29.1;
 Serial.println(distance);
    if(distance<30){  
      digitalWrite(Buzz,HIGH); 
      delay(200); 
      digitalWrite(Buzz,LOW); 
      delay(200); 
      digitalWrite(Buzz,HIGH); 
      delay(200); 
      digitalWrite(Buzz,LOW); 
      delay(200); 
      digitalWrite(Buzz,HIGH); 
      delay(200); 
      digitalWrite(Buzz,LOW); 
      delay(200);} 

    if (digitalRead(FS)==0)
      {Serial.println("Y");}
   else{Serial.println("N");}      
     delay(500);
   
  

  
}                                                
