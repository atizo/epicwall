import processing.serial.*;

Serial myPort;  // Create object from Serial class
int val;      // Data received from the serial port

PImage box1, box2;
float offset;

void setup() {
  size(930, 315);
  box1 = loadImage("box1.png");
  box2 = loadImage("box2.png");
  String portName = Serial.list()[0];
  myPort = new Serial(this, portName, 115200);//230400);
  
  background(51);
  for(int i=0; i<50; i++){
    drawBox(i, 255, 255, 255);
  }
}

void drawBox(int address, int cred, int cgreen, int cblue) {
  int row = address / 10;
  int col = address % 10;  
  int flip = row % 2;
  tint(cred, cgreen, cblue, 255);
  if(address % 2 == flip){
    image(box1, 10 + col * 90, 20 + row * 55);
  }else{
    image(box2, 10 + col * 90, 20 + row * 55);
  }

}

void draw() {
//  for(int i=0; i<50; i++){
//    drawBox(i, int(random(255)), int(random(255)), int(random(255)));
//  }
  
  while ( myPort.available() > 0) {  // If data is available,
    int lf = 0xff;
    byte[] inBuffer = new byte[5];
    
    myPort.readBytesUntil(lf, inBuffer);
    
    if (inBuffer != null) {
      drawBox(int(inBuffer[0]), int(inBuffer[1]), int(inBuffer[2]), int(inBuffer[3]));
    }
  }
}





