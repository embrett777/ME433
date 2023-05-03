#include "nu32dip.h" // constants, functions for startup and UART
#include "i2c_master_noint.h"

void turnOnGP7(void);
void turnOffGP7(void);
unsigned char write_address = 0b01000000;
unsigned char read_address = 0b01000001;

int main(void) {
  NU32DIP_Startup(); // cache on, interrupts on, LED/button init, UART init
  i2c_master_setup();
  
  //setting output and input pins
  //send start bit
  i2c_master_start();
  //send address of chip
  i2c_master_send(write_address);
  //send register name: IODIR
  i2c_master_send(0x00);
  //send the value to clear bit 7 and set bit 0
  //this makes GP7 an output and GP0 an input
  i2c_master_send(0b00000001);
  //send stop bit
  i2c_master_stop();
  
  while(1){
      NU32DIP_YELLOW = 0;
      turnOnGP7();
      unsigned int t = _CP0_GET_COUNT();
      while(_CP0_GET_COUNT() < t + 12000*2000){}
      NU32DIP_YELLOW = 1;
      turnOffGP7();
      t = _CP0_GET_COUNT();
      while(_CP0_GET_COUNT() < t + 12000*2000){}
  }
}

void turnOnGP7(void){
    //send start bit
    i2c_master_start();
    //send address of chip
    i2c_master_send(write_address);
    //send register name: OLAT
    i2c_master_send(0x0A);
    //send the value to turn on GP7
    i2c_master_send(0b10000000);
    //send stop bit
    i2c_master_stop();
}

void turnOffGP7(){
    //send start bit
    i2c_master_start();
    //send address of chip
    i2c_master_send(write_address);
    //send register name: OLAT
    i2c_master_send(0x0A);
    //send the value to turn on GP7
    i2c_master_send(0b00000000);
    //send stop bit
    i2c_master_stop();
}