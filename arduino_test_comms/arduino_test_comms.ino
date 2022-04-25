



#define RELEASE_PIN 8



const int BUFFER_SIZE = 50;
char buf[BUFFER_SIZE];
int message_counter_idx = 0;
char msg[5];



void setup() {
  // put your setup code here, to run once:

  pinMode(RELEASE_PIN, OUTPUT);    // sets the digital pin 8 as output
  digitalWrite(RELEASE_PIN, LOW);
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
//    digitalWrite(RELEASE_PIN, HIGH);
//    delay(500);
//    digitalWrite(RELEASE_PIN, LOW);
//    delay(500);
    if (Serial.available() > 0)
    {

      char data = Serial.read();
      msg[message_counter_idx] = data;
        
      if (message_counter_idx == 3) //Message Recieved
      {
          msg[4] = "\0";

          //Whole Message Recieved 
          //Check integrity
          if (msg[0] == (char) 0xFE && msg[3] == (char)0xFF)
          {

            //DO SERVO ROTATIONS HERE

            if (msg[2] == (char) 0x01)
            {
              digitalWrite(RELEASE_PIN, HIGH); //Stop Toasting
            }
            if (msg[2] == (char) 0x00)
            {
              digitalWrite(RELEASE_PIN, LOW);
            }
            
            Serial.print(msg);
            Serial.print("\n");
            message_counter_idx = 0;
          }
        
      }
      else
      {
        message_counter_idx += 1; 
      }
     
    }
   

}
