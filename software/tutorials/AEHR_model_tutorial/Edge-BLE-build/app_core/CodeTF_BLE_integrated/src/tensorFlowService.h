#include <zephyr/types.h>
#include <stddef.h>
#include <string.h>
#include <errno.h>
#include <zephyr.h>
#include <soc.h>
#include "common.h"
#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>
#include <bluetooth/conn.h>
#include <bluetooth/uuid.h>
#include <bluetooth/gatt.h>

// work queue structure used to send TF lite data and packet counter notification 
//in a interrupt service handler initiated by a timer. 	
struct TfMicroInfo {
    struct k_work work;
    float *dataPacket;
    //this is all we have edited so far, need to make it a lot more comprehensive
    uint16_t packetLength;
}; 
extern struct TfMicroInfo my_service ;  // work-queue instance for tflite notifications

#define TFMICRO_SERVICE_UUID 0x1F, 0x35, 0xBD, 0x4B, 0xAE, 0xD0, 0x68, 0x9C,\
				  0xE2, 0x48, 0x81, 0x1D, 0x22, 0x5D, 0x39, 0xDA      

#define RX_CHARACTERISTIC_UUID  0x1F, 0x35, 0xBD, 0x4B, 0xAE, 0xD0, 0x68, 0x9C, \
				 0xE2, 0x48, 0x81, 0x1D, 0x21, 0xC9, 0x39, 0xDA       

#define TX_CHARACTERISTIC_UUID  0x1F, 0x35, 0xBD, 0x4B, 0xAE, 0xD0, 0x68, 0x9C, \
				 0xE2, 0x48, 0x81, 0x1D, 0x22, 0xC9, 0x39, 0xDA       
			                   
/** @brief Callback type for when new data is received. */
typedef void (*data_rx_cb_t)(float *data, uint16_t length);

/** @brief Callback struct used by the tfMicro_service Service. */
struct tfMicro_service_cb 
{
	/** Data received callback. */
	data_rx_cb_t    data_rx_cb;
};

int tfMicro_service_init(void);

void tfMicro_service_send(struct bt_conn *conn, const float *data, uint16_t len);

static void tfMicro_notify(struct k_work *);
static void tfMicro_notify(struct k_work *item)
{
    	struct TfMicroInfo* the_device=  ((struct TfMicroInfo *)(((char *)(item)) - offsetof(struct TfMicroInfo, work)));
        
	float *dataPacket = the_device->dataPacket;
	uint16_t packetLength = the_device->packetLength;
	//printk("data LED =%u, Data counter1=%u, Data counter2=%u,pk=%u\n", dataPacket[0],dataPacket[1],dataPacket[2],packetLength);
	tfMicro_service_send(my_connection, the_device->dataPacket, packetLength);
}



