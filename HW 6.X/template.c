#include "nu32dip.h" // constants, functions for startup and UART
#include "i2c_master_noint.h"

void turnOnGP7(void);
void turnOffGP7(void);
int readGP0(void);
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
      NU32DIP_GREEN = 0;
      _CP0_SET_COUNT(0);
      while(_CP0_GET_COUNT() < 12000*2000){
                    int r = readGP0();
          if (r){
              turnOffGP7();
          }
          else{
              turnOnGP7();
          }
      }

      NU32DIP_GREEN = 1;
      _CP0_SET_COUNT(0);
      while(_CP0_GET_COUNT() < 12000*2000){
          int r = readGP0();
          if (r){
              turnOffGP7();
          }
          else{
              turnOnGP7();
          }
      }
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

int readGP0(void){
    //send start bit
    i2c_master_start();
    //send address of chip to write
    i2c_master_send(write_address);
    //send register to read from: GPIO
    i2c_master_send(0x09);
    //send restart bit
    i2c_master_restart();
    //send address of chip to read
    i2c_master_send(read_address);
    //receive
    unsigned char r = i2c_master_recv();
    //acknowledge (1=done)
    i2c_master_ack(1);
    //send stop bit
    i2c_master_stop();
    //return the value of GP0
    return (r&0b00000001);
}