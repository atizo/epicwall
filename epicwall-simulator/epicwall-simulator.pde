import processing.serial.*;

// sudo socat -d -d pty,raw,echo=0,link=/dev/ttyS10,user=god pty,raw,echo=0,link=/dev/ttyS11,user=god

Serial port;

Cell[][] wall;
int rows = 5;
int cols = 10;

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
  size(500, 150);
  println(Serial.list());
  port = new Serial(this, "/dev/ttyS11", 115200);
  port.bufferUntil(-1); // signed...
  wall = new Cell[rows][cols];
  for (int i = 0; i < rows; i ++ ) {
    for (int j = 0; j < cols; j ++ ) {
      wall[i][j] = new Cell(j*50, i*30, 50, 30);
    }
  }
}

void draw() {}

byte[] input = new byte[5];
int id, id_r, id_g, id_b;
void serialEvent(Serial port) {
  input = port.readBytes();
  if (input.length != 5) return; 
  id = input[0] & 255;
  id_r = input[1] & 255;
  id_g = input[2] & 255;
  id_b = input[3] & 255;
  wall[ id / cols ][ id % cols ].draw(id_r, id_g, id_b);
}
