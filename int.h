#ifndef int_h
#define int_h

#if ARDUINO >= 100
  #include "Arduino.h"
#else
  #include "WProgram.h"
  #include "pins_arduino.h"
  #include "WConstants.h"
#endif


extern void SetupTimer2(void);
ISR(TIMER2_OVF_vect);
extern void assemble_dcc_msg(unsigned char a, unsigned char b);  
#endif
