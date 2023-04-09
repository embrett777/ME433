#include "nu32dip.h" // constants, functions for startup and UART
#include <math.h>

void blink(int, int); // blink the LEDs function

int main(void) {
  char message[100];
  NU32DIP_Startup(); // cache on, interrupts on, LED/button init, UART init
  
  float wave[100];
  int j;
  for (int j=0; j<100; j++){
      wave[j] = sin(2*3.14*j/100);
  }
  while (1) {
      while(NU32DIP_USER){}
      int i = 0;
      for (i=0; i<100; i++){
          sprintf(message, "%f\r\n", wave[i]);
          NU32DIP_WriteUART1(message);
          _CP0_SET_COUNT(0);
          while(_CP0_GET_COUNT()<240000){}
      }
  }
}
		