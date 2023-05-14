#include "nu32dip.h" // constants, functions for startup and UART
#include "i2c_master_noint.h"
#include "ssd1306.h"
#include "font.h"

void drawChar(char letter, char x, char y);
void drawString(char *m, char x, char y);

int main(void) {
  NU32DIP_Startup(); // cache on, interrupts on, LED/button init, UART init
  i2c_master_setup();
  ssd1306_setup();
  
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