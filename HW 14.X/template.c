#include "nu32dip.h" // constants, functions for startup and UART

#define MS_LOW 0.5
#define MS_HIGH 2.5

void Timer2_Setup(void);

int main(void) {
  NU32DIP_Startup(); // cache on, interrupts on, LED/button init, UART init
  Timer2_Setup();
  
  int deg45 = (int)((MS_HIGH - MS_LOW)*45/180.0 + MS_LOW)/20.0*60000;
  int deg135 = (int)((MS_HIGH - MS_LOW)*135/180.0 + MS_LOW)/20.0*60000;
  while (1) {
      _CP0_SET_COUNT(0);
      while (_CP0_GET_COUNT()<96000000){}
      OC1RS = deg45;
      _CP0_SET_COUNT(0);
      while (_CP0_GET_COUNT()<96000000){}
      OC1RS = deg135;
  }
  
}


void Timer2_Setup(void)
{
	//set OC1 connected to timer 2
  RPA0Rbits.RPA0R = 0b0101;              // sets A0 to be OC1
  T2CONbits.TCKPS = 4;     // Timer2 prescaler N=16 (1:16)
  PR2 = 59999;              // period = (PR2+1) * N * (1/48000000) = 50 Hz
  TMR2 = 0;                // initial TMR2 count is 0
  OC1CONbits.OCM = 0b110;  // PWM mode without fault pin; other OC1CON bits are defaults
  OC1CONbits.OCTSEL = 0;   // Use timer2
  OC1RS = 4500;             // duty cycle = OC1RS/(PR2+1) = 25%
  OC1R = 500;              // initialize before turning OC1 on; afterward it is read-only
  T2CONbits.ON = 1;        // turn on Timer2
  OC1CONbits.ON = 1;       // turn on OC1
  
}