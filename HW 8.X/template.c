#include "nu32dip.h" // constants, functions for startup and UART
#include "i2c_master_noint.h"
#include "ssd1306.h"
#include "mpu6050.h"
#include "font.h"

void drawChar(char letter, char x, char y);
void drawString(char *m, char x, char y);
void blink(int iterations, int time_ms);

int main(void) {
  NU32DIP_Startup(); // cache on, interrupts on, LED/button init, UART init
  i2c_master_setup();
  ssd1306_setup();
  init_mpu6050();
  
  unsigned char data[14];
  float zXL;
  char m[100];

  while(1){
      	// use core timer for exactly 100Hz loop
        _CP0_SET_COUNT(0);

        // read IMU
        burst_read_mpu6050(data);
        
		// convert data
        zXL = conv_zXL(data);

        // print out the data
        sprintf(m, "Z accel = %f", zXL);
        drawString(m,10,10);
        ssd1306_update();
        unsigned int t = _CP0_GET_COUNT();
        float t2 = t/24000000.0;
        sprintf(m, "Fps: %f", t2);
        drawString(m,10,20);
        ssd1306_update();
        blink(1,5);
    }
}

void drawChar(char letter, char x, char y){
    int j=0;
    int i=0;
    for(j=0; j<5; ++j){
        char col = ASCII[letter-0x20][j];
        for(i=0; i<8; ++i){
            ssd1306_drawPixel(x+j, y+i, (col>>i)&0b1);
        }
    }
}

void drawString(char *m, char x, char y){
    int k=0;
    while(m[k]!=0){
        drawChar(m[k],x+5*k,y);
        k++;
    }
}

void blink(int iterations, int time_ms) {
    int i;
    unsigned int t;
    for (i = 0; i < iterations; i++) {
        NU32DIP_GREEN = 0; // on
        NU32DIP_YELLOW = 1; // off
        t = _CP0_GET_COUNT(); // should really check for overflow here
        // the core timer ticks at half the SYSCLK, so 24000000 times per second
        // so each millisecond is 24000 ticks
        // wait half in each delay
        while (_CP0_GET_COUNT() < t + 12000 * time_ms) {
        }

        NU32DIP_GREEN = 1; // off
        NU32DIP_YELLOW = 0; // on
        t = _CP0_GET_COUNT(); // should really check for overflow here
        while (_CP0_GET_COUNT() < t + 12000 * time_ms) {
        }
    }
}