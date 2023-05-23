#include "nu32dip.h" // constants, functions for startup and UART
#include "ws2812b.h"

int main(void) {
  NU32DIP_Startup(); // cache on, interrupts on, LED/button init, UART init
  ws2812b_setup();
  
  wsColor pixels[5];
  int hues[5] = {0, 70, 140, 210, 280};
  int a=0, b=70, c=140, d=210, e=280;
  while(1){
      for (int i=0; i<5; i++){
          pixels[i] = HSBtoRGB(hues[i],1,0.5);
          hues[i] = hues[i] + 1;
          if (hues[i]>360){
              hues[i] = 0;
          }
      }
    ws2812b_setColor(pixels, 5);
  }
}
