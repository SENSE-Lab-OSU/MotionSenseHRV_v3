
// printer.h file
#ifndef COMMON_H_
#define COMMON_H_
typedef union{ 
    float float_val;
    uint8_t floatcast[4];
}float_cast;
 // common.h code goes here
extern struct bt_conn *my_connection; // BLE conection instance used to access the  sofr-device controller
extern uint16_t global_counter;
#endif



