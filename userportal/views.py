from django.http import HttpResponse

def index(request):
    return HttpResponse("<h1>This is the User Portal</h1>")

/*
 *     SocialLedge.com - Copyright (C) 2013
 *
 *     This file is part of free software framework for embedded processors.
 *     You can use it and/or distribute it as long as this copyright header
 *     remains unmodified.  The code is free for personal use and requires
 *     permission to use in a commercial product.
 *
 *      THIS SOFTWARE IS PROVIDED "AS IS".  NO WARRANTIES, WHETHER EXPRESS, IMPLIED
 *      OR STATUTORY, INCLUDING, BUT NOT LIMITED TO, IMPLIED WARRANTIES OF
 *      MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE APPLY TO THIS SOFTWARE.
 *      I SHALL NOT, IN ANY CIRCUMSTANCES, BE LIABLE FOR SPECIAL, INCIDENTAL, OR
 *      CONSEQUENTIAL DAMAGES, FOR ANY REASON WHATSOEVER.
 *
 *     You can reach the author of this software at :
 *          p r e e t . w i k i @ g m a i l . c o m
 */
#include <stdio.h>
#include "utilities.h"
#include "io.hpp"
#include "tasks.hpp"
#include "examples/examples.hpp"
#include "gpio.hpp"

using namespace std;

/**
 * @file
 * @brief This is the application entry point.
 *          FreeRTOS and stdio printf is pre-configured to use uart0_min.h before main() enters.
 *          @see L0_LowLevel/lpc_sys.h if you wish to override printf/scanf functions.
 *
 */

/**
 * The main() creates tasks or "threads".  See the documentation of scheduler_task class at scheduler_task.hpp
 * for details.  There is a very simple example towards the beginning of this class's declaration.
 *
 * @warning SPI #1 bus usage notes (interfaced to SD & Flash):
 *      - You can read/write files from multiple tasks because it automatically goes through SPI semaphore.
 *      - If you are going to use the SPI Bus in a FreeRTOS task, you need to use the API at L4_IO/fat/spi_sem.h
 *
 * @warning SPI #0 usage notes (Nordic wireless)
 *      - This bus is more tricky to use because if FreeRTOS is not running, the RIT interrupt may use the bus.
 *      - If FreeRTOS is running, then wireless task may use it.
 *        In either case, you should avoid using this bus or interfacing to external components because
 *        there is no semaphore configured for this bus and it should be used exclusively by nordic wireless.
 */

GPIO A0(P1_29);//0
GPIO A1(P1_28);//0
GPIO A2(P1_23);//0
GPIO A3(P1_22);//1
GPIO A4(P1_20);//0
GPIO A5(P1_19);//0
GPIO A6(P0_30);//0
GPIO A7(P0_29);//1

GPIO dir_w(P0_0);
GPIO bus_e(P0_1);
GPIO addr_w(P2_1);
GPIO dataOut_w(P2_2);
GPIO dataIn_e(P2_3);
GPIO cmd_w(P2_4);
GPIO clk(P2_6);


void setAddress(char byte){
//set GPIO as output ();
dir_w.setHigh();
bus_e.setLow();//

A0.setAsOutput();
A1.setAsOutput();
A2.setAsOutput();
A3.setAsOutput();
A4.setAsOutput();
A5.setAsOutput();
A6.setAsOutput();
A7.setAsOutput();

A0.set(byte&(1<<0));
A1.set(byte&(1<<1));
A2.set(byte&(1<<2));
A3.set(byte&(1<<3));
A4.set(byte&(1<<4));
A5.set(byte&(1<<5));
A6.set(byte&(1<<6));
A7.set(byte&(1<<7));

addr_w.setHigh();
delay_ms(100);
addr_w.setLow();
delay_ms(100);
bus_e.setHigh();
delay_ms(100);

/*
if(byte & (1 << 7) A8.setHigh()
        else A8.setLow()
*/
        //do the same for each byte

}

void test(){

//setAddress(data);

    char cmd_reg  =  {0x00};
       dir_w.setHigh();
       bus_e.setLow();

       A0.setAsOutput();
       A1.setAsOutput();
       A2.setAsOutput();
       A3.setAsOutput();
       A4.setAsOutput();
       A5.setAsOutput();
       A6.setAsOutput();
       A7.setAsOutput();

       A7.set(cmd_reg&(1<<0));
       A6.set(cmd_reg&(1<<1));
       A5.set(cmd_reg&(1<<2));
       A4.set(cmd_reg&(1<<3));
       A3.set(cmd_reg&(1<<4));
       A2.set(cmd_reg&(1<<5));
       A1.set(cmd_reg&(1<<6));
       A0.set(cmd_reg&(1<<7));

       //printf("this is the cmd: %c \n", cmd_reg);

       cmd_w.setHigh();
       delay_ms(100);
       cmd_w.setLow();
       delay_ms(100);
       bus_e.setHigh();
       delay_ms(100);

       for(int i = 0; i < 5; i++)
           {

               clk.setHigh();
               delay_ms(100);
               clk.setLow();
               delay_ms(100);

           }
}

void write(char data, char addr){

    setAddress(addr);
    printf("this is address %x\n", addr);



    dir_w.setHigh();


    A0.setAsOutput();
    A1.setAsOutput();
    A2.setAsOutput();
    A3.setAsOutput();
    A4.setAsOutput();
    A5.setAsOutput();
    A6.setAsOutput();
    A7.setAsOutput();

    A0.set(data&(1<<0));
    A1.set(data&(1<<1));
    A2.set(data&(1<<2));
    A3.set(data&(1<<3));
    A4.set(data&(1<<4));
    A5.set(data&(1<<5));
    A6.set(data&(1<<6));
    A7.set(data&(1<<7));

    bus_e.setLow();
   //printf("this is data %c 123", data);

    dataOut_w.setHigh();
    delay_ms(100);
    dataOut_w.setLow();
    delay_ms(100);
    bus_e.setHigh();

    //enable
    //char cmd_reg  =  {0x88}; //1000 1000, displays on board pins
    char cmd_reg = {0x88};
    dir_w.setHigh();
    bus_e.setLow();

    A0.setAsOutput();
    A1.setAsOutput();
    A2.setAsOutput();
    A3.setAsOutput();
    A4.setAsOutput();
    A5.setAsOutput();
    A6.setAsOutput();
    A7.setAsOutput();

    A7.set(cmd_reg&(1<<0));
    A6.set(cmd_reg&(1<<1));
    A5.set(cmd_reg&(1<<2));
    A4.set(cmd_reg&(1<<3));
    A3.set(cmd_reg&(1<<4));
    A2.set(cmd_reg&(1<<5));
    A1.set(cmd_reg&(1<<6));
    A0.set(cmd_reg&(1<<7));

    //printf("this is the cmd: %c \n", cmd_reg);

    cmd_w.setHigh();
    delay_ms(100);
    cmd_w.setLow();
    delay_ms(100);
    bus_e.setHigh();
    delay_ms(100);



//before set address register set clock low

    for(int i = 0; i < 5; i++)
    {

        clk.setHigh();
        delay_ms(100);
        clk.setLow();
        delay_ms(100);

    }
}

char read(char addr){
 //set as input()
char byte='0';
setAddress(addr);


bus_e.setHigh();
dir_w.setLow();
dataIn_e.setLow();

A0.setAsInput();
A1.setAsInput();
A2.setAsInput();
A3.setAsInput();
A4.setAsInput();
A5.setAsInput();
A6.setAsInput();
A7.setAsInput();

bus_e.setLow();

byte = byte | (A0.read() << 0);
byte = byte | (A1.read() << 1);
byte = byte | (A2.read() << 2);
byte = byte | (A3.read() << 3);
byte = byte | (A4.read() << 4);
byte = byte | (A5.read() << 5);
byte = byte | (A6.read() << 6);
byte = byte | (A7.read() << 7);

dataIn_e.setHigh();
bus_e.setHigh();



   char cmd_reg = { 0x90 }; //1001 0000
   dir_w.setHigh();
   bus_e.setLow();

   A0.setAsOutput();
   A1.setAsOutput();
   A2.setAsOutput();
   A3.setAsOutput();
   A4.setAsOutput();
   A5.setAsOutput();
   A6.setAsOutput();
   A7.setAsOutput();

   A7.set(cmd_reg&(1<<0));
   A6.set(cmd_reg&(1<<1));
   A5.set(cmd_reg&(1<<2));
   A4.set(cmd_reg&(1<<3));
   A3.set(cmd_reg&(1<<4));
   A2.set(cmd_reg&(1<<5));
   A1.set(cmd_reg&(1<<6));
   A0.set(cmd_reg&(1<<7));

   cmd_w.setHigh();
   delay_ms(100);
   cmd_w.setLow();
   delay_ms(100);
   bus_e.setHigh();
   delay_ms(100);


   for(int i = 0; i < 5; i++)
   {

       clk.setHigh();
       delay_ms(100);
       clk.setLow();
       delay_ms(100);
   }

return byte;

};




int main(void)
{

dir_w.setAsOutput();
bus_e.setAsOutput();
addr_w.setAsOutput();
dataOut_w.setAsOutput();
dataIn_e.setAsOutput();
cmd_w.setAsOutput();
clk.setAsOutput();

bus_e.setHigh();
addr_w.setLow();
dataOut_w.setLow();
dataIn_e.setHigh();
cmd_w.setLow();
clk.setLow();
dir_w.setHigh();




test();

char wr={0x22}; //0010 0010
//status is 0001 when writing but reading 0100 which is 2! ...
//output read is FF!
//hardware issue that can be resolved with software
char rd;
char addr= {0x55}; // 0100 0010
printf("hello\n");//
write(wr, addr);
test();
rd = read(addr);
test();
char addr2= {0x35};
write(wr, addr2);
test();
rd = read(addr2);


printf("This is what was read %x /n",rd);



    return 0;
}
