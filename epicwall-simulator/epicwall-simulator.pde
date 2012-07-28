import processing.serial.*;

// sudo socat -d -d pty,raw,echo=0,link=/dev/ttyS10,user=god pty,raw,echo=0,link=/dev/ttyS11,user=god

Serial port;

Cell[][] wall;
int rows = 5, cols = 10, pkgPointer = 0;
int[] led = new int[4];

class Cell {
  float x,y,w,h;
  Cell(float X, float Y, float W, float H) {
    x = X; y = Y; w = W; h = H;
  }
  void draw(int r, int g, int b) {
    fill(r,g,b);
    rect(x,y,w,h);
  }
}

void setup() {
  frameRate(100);
  size(500, 150);
  println(Serial.list());
  port = new Serial(this, "/dev/ttyS11", 115200);
  wall = new Cell[rows][cols];
  for (int i = 0; i < rows; i ++ ) {
    for (int j = 0; j < cols; j ++ ) {
      wall[i][j] = new Cell(j*50, i*30, 50, 30);
    }
  }
}

void draw() {
  while (port.available() > 0) {
    char inByte = port.readChar();
    if(inByte == 255){
      pkgPointer = 0;
    }else if(pkgPointer < 4){
      led[pkgPointer] = inByte;
      if(pkgPointer == 3){
          wall[ led[0] / cols ][ led[0] % cols ].draw(led[1], led[2], led[3]);
      }
      pkgPointer += 1;
    }
  }
}
