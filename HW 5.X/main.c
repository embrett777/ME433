#include "spi.h"
#include "nu32dip.h"
#include <math.h>

void main(){
    NU32DIP_Startup();
    initSPI();
    
    unsigned short v = 0;
    unsigned char c = 0;
    unsigned short p;
    //creating sine wave buffer
    int sine_wave[100];
    for(int i=0; i<100; i++){
        sine_wave[i] = 512 + 512*sin(2*3.14*i/50);
    }
    //creating triangle wave buffer
    int tri_wave[100];
    for(int i=0; i<50; i++){
        tri_wave[i] = 1023.0/50*i;
    }
    for(int i=0; i<50; i++){
        tri_wave[i+50] = 1023 - 1023.0/50*i;
    }
    
    
    while(1){
        //cycle through voltages to sent to MPC4912
        int i;
        for(i=0; i<100; i++){
            //choose first channel
            c = 0;
            //set desired voltage
            v = sine_wave[i];
            //create message to send
            p = (c<<15);
            p = p|(0b111<<12);
            p = p|v;
            
            //set CS low
            LATBbits.LATB7 = 0;
            //send first 8 bits
            spi_io((p>>8));
            //send second 8 bits
            spi_io(p);
            LATBbits.LATB7 = 1;
           
            
            
            //choose second channel
            c = 1;
            //set desired voltage
            v = tri_wave[i];
            //create message to send
            p = (c<<15);
            p = p|(0b111<<12);
            p = p|v;
            
            //set CS low
            LATBbits.LATB7 = 0;
            //send first 8 bits
            spi_io((p>>8));
            //send second 8 bits
            spi_io(p);
            LATBbits.LATB7 = 1;
            
            _CP0_SET_COUNT(0);
            while(_CP0_GET_COUNT() < 12000*10){}
        }
    }
}