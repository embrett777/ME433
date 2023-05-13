#include "nu32dip.h" // constants, functions for startup and UART
#include "i2c_master_noint.h"
#include "ssd1306.h"

int main(void) {
  NU32DIP_Startup(); // cache on, interrupts on, LED/button init, UART init
  i2c_master_setup();
  ssd1306_setup();
  
}