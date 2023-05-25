#include "nu32dip.h" // constants, functions for startup and UART
#include "ws2812b.h"

int main(void) {
  NU32DIP_Startup(); // cache on, interrupts on, LED/button init, UART init
  ws2812b_setup();

  wsColor pixels[8];
  volatile int hues[8] = {0, 45, 90, 135, 180, 225, 270, 315};
  char message[100];
  while(1){
        for (int k=0; k<8; k++){
          pixels[k] = HSBtoRGB(hues[k],1,1);
          hues[k] = hues[k] + 1;
          if (hues[k]>360){
              hues[k] = 0;
          }
        }

        ws2812b_setColor(pixels, 8);
        int t = _CP0_GET_COUNT();
        while(_CP0_GET_COUNT()<t+24000000/1000){}
        
  }
}
