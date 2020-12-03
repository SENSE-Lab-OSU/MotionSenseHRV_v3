/* Copyright 2019 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#include "main_functions.h"
#include <zephyr.h>
#include <zephyr/types.h>
#include <stddef.h>
#include <string.h>
#include <errno.h>
#include <sys/printk.h>
#include <sys/byteorder.h>
#include <drivers/gpio.h>
#include <soc.h>
#include <kernel.h>
#include "common.h"
#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>
#include <bluetooth/conn.h>
#include <bluetooth/uuid.h>
#include <bluetooth/gatt.h>

#include "battery_service.h" 
#include <settings/settings.h>
#include "tensorFlowService.h"
#include <nrfx_timer.h>
#include <dk_buttons_and_leds.h>

#define DEVICE_NAME             CONFIG_BT_DEVICE_NAME
#define DEVICE_NAME_LEN         (sizeof(DEVICE_NAME) - 1)

#define DIS_FW_REV_STR		 CONFIG_BT_DIS_FW_REV_STR
#define DIS_FW_REV_STR_LEN 	 (sizeof(DIS_FW_REV_STR))

#define DIS_HW_REV_STR 	 CONFIG_BT_DIS_HW_REV_STR
#define DIS_HW_REV_STR_LEN 	 (sizeof(DIS_HW_REV_STR))

#define DIS_MANUF		 CONFIG_BT_DIS_MANUF
#define DIS_MANUF_LEN 	 	 (sizeof(DIS_MANUF))

#define DIS_MODEL		 CONFIG_BT_DIS_MODEL
#define DIS_MODEL_LEN		 (sizeof(DIS_MODEL))

#define TIMER_MS 20
#define TIMER_PRIORITY 1
#define WORKQUEUE_STACK_SIZE 512
#define WORKQUEUE_PRIORITY 1

#define RUN_STATUS_LED          DK_LED1

K_THREAD_STACK_DEFINE(my_stack_area, WORKQUEUE_STACK_SIZE);
struct batteryInfo my_device;
struct TfMicroInfo my_service;
struct k_work_q my_work_q;

void timer_handler(nrf_timer_event_t, void*);

static K_SEM_DEFINE(ble_init_ok, 0, 1);

uint16_t global_counter;

static bool connectedFlag=false;
static const struct bt_data ad[] = {
	BT_DATA_BYTES(BT_DATA_FLAGS, (BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR)),
	BT_DATA(BT_DATA_NAME_COMPLETE, DEVICE_NAME, DEVICE_NAME_LEN),
};

static const struct bt_data sd[] = {
	BT_DATA_BYTES(BT_DATA_UUID128_ALL, TFMICRO_SERVICE_UUID),
};

struct bt_conn *my_connection;

static const nrfx_timer_t timer_global = NRFX_TIMER_INSTANCE(1); // Using TIMER1 as TIMER 0 is used by RTOS for ble


static uint8_t ii =0;

// Setting up the device information service
static int settings_runtime_load(void)
{
	settings_runtime_set("bt/dis/model",
			     DIS_MODEL,
			     DIS_MODEL_LEN);
	settings_runtime_set("bt/dis/manuf",
			     DIS_MANUF,
			     DIS_MANUF_LEN);


	settings_runtime_set("bt/dis/fw",
			     DIS_FW_REV_STR,
			     DIS_FW_REV_STR_LEN);
	settings_runtime_set("bt/dis/hw",
			     DIS_HW_REV_STR,
			     DIS_HW_REV_STR_LEN);
	return 0;
}

static void timer_deinit(void)
{
	nrfx_timer_disable(&timer_global);
    	nrfx_timer_uninit(&timer_global);	
}


static void timer_init(void)
{
	uint32_t time_ticks;
	nrfx_err_t          err;
	nrfx_timer_config_t timer_cfg = {
		.frequency = NRF_TIMER_FREQ_1MHz,
		.mode      = NRF_TIMER_MODE_TIMER,
		.bit_width = NRF_TIMER_BIT_WIDTH_24,
		.interrupt_priority = TIMER_PRIORITY,
		.p_context = NULL,
	};  

	err = nrfx_timer_init(&timer_global, &timer_cfg, timer_handler);
	if (err != NRFX_SUCCESS) {
		//printk("nrfx_timer_init failed with: %d\n", err);
	}
	else
		//printk("nrfx_timer_init success with: %d\n", err);
	time_ticks = nrfx_timer_ms_to_ticks(&timer_global, TIMER_MS);
	//printk("time ticks = %d\n", time_ticks);


    	nrfx_timer_extended_compare(&timer_global, NRF_TIMER_CC_CHANNEL0, time_ticks \ 
         , NRF_TIMER_SHORT_COMPARE0_CLEAR_MASK, true);

    	nrfx_timer_enable(&timer_global);
}


static void connected(struct bt_conn *conn, uint8_t err)
{
	struct bt_conn_info info; 
	char addr[BT_ADDR_LE_STR_LEN];

	my_connection = conn;

	if (err) 
	{
		//printk("Connection failed (err %u)\n", err);
		return;
	}
	else if(bt_conn_get_info(conn, &info))
	{
		//printk("Could not parse connection info\n");
	}
	else
	{  // Start the timer and stop advertising and initialize all the modules
		bt_addr_le_to_str(bt_conn_get_dst(conn), addr, sizeof(addr));
		
		printk("Connection established!		\n\
		Connected to: %s					\n\
		Role: %u							\n\
		Connection interval: %u				\n\
		Slave latency: %u					\n\
		Connection supervisory timeout: %u	\n"
		, addr, info.role, info.le.interval, info.le.latency, info.le.timeout);
		
		tfMicro_service_init();

               connectedFlag=true;
		timer_init();
		global_counter = 0;
	}

}

static void disconnected(struct bt_conn *conn, uint8_t reason)
{
	// Stop timer and do all the cleanup
	printk("Disconnected (reason %u)\n", reason);
	timer_deinit();	
	connectedFlag=false;
}

static bool le_param_req(struct bt_conn *conn, struct bt_le_conn_param *param)
{
	
	//If acceptable params, return true, otherwise return false.
	if((param->interval_min > 9) && (param->interval_max > 20))
		return false;
	else
		return true; 
}

static void le_param_updated(struct bt_conn *conn, uint16_t interval, uint16_t latency, uint16_t timeout)
{
	struct bt_conn_info info; 
	char addr[BT_ADDR_LE_STR_LEN];
	
	if(bt_conn_get_info(conn, &info))
	{
		//printk("Could not parse connection info\n");
	}
	else
	{
		bt_addr_le_to_str(bt_conn_get_dst(conn), addr, sizeof(addr));
		
		printk("Connection parameters updated!	\n\
		Connected to: %s						\n\
		New Connection Interval: %u				\n\
		New Slave Latency: %u					\n\
		New Connection Supervisory Timeout: %u	\n"
		, addr, info.le.interval, info.le.latency, info.le.timeout);
                
	}
}

static struct bt_conn_cb conn_callbacks = 
{
	.connected			= connected,
	.disconnected   		= disconnected,
	.le_param_req			= le_param_req,
	.le_param_updated		= le_param_updated
};
static void error(void)
{
	while (true) {
		//printk("Error!\n");
		/* Spin for ever */
		k_sleep(K_MSEC(1000)); //1000ms
	}
}

static void bt_ready(int err)
{
	if (err) 
	{
		printk("BLE init failed with error code %d\n", err);
		return;
	}
	else 	
		printk("BLE init success\n");
	
       
	settings_load();
	 
	settings_runtime_load();

	//Configure connection callbacks
	bt_conn_cb_register(&conn_callbacks);

	//Initalize services
	err = tfMicro_service_init();
        
	if (err) 
	{
		//printk("Failed to init tf Micro (err:%d)\n", err);
		return;
	}

	//Start advertising
	const struct bt_le_adv_param v={ \
        .id = BT_ID_DEFAULT, \
        .sid = 0, \
        .secondary_max_skip = 0, \
        .options = BT_LE_ADV_OPT_CONNECTABLE,\
        .interval_min = BT_GAP_ADV_FAST_INT_MIN_2, \
        .interval_max = BT_GAP_ADV_FAST_INT_MAX_2, \
        .peer = NULL
	};
	
        err = bt_le_adv_start(&v, ad, ARRAY_SIZE(ad),
			      sd, ARRAY_SIZE(sd));
	if (err) {
		//printk("Advertising failed to start (err %d)\n", err);

	}
       else
       //printk("Advertising successfully started\n");

	k_sem_give(&ble_init_ok);
}

// Initialize BLE
static void ble_init(void)
{
	int err;
	


	err = bt_enable(bt_ready);
	if (err) 
	{
		printk("BLE initialization failed\n");
		error(); //Catch error
	}
	
	err = k_sem_take(&ble_init_ok, K_MSEC(500));

	if (!err) 
	{
		printk("Bluetooth initialized\n");
	} else 
	{
		printk("BLE initialization did not complete in time\n");
		error(); //Catch error
	}
	if (err) {
		printk("Bluetooth init failed (err %d)\n", err);
		
	}	
}

// Timer handler that periodically executes commands with a period, 
// which is defined by the macro-variable TIMER_MS

void timer_handler(nrf_timer_event_t event_type, void* p_context)
{
   	uint8_t counts1 = 0;
        float *y;
        float_cast tempVal;
    	uint8_t dataPacket[TFMICRO_DATA_LEN]; // Data packet sent in the TF lite service, contains 3 Bytes 
    	
    switch (event_type)
    {
 
        case NRF_TIMER_EVENT_COMPARE0:
        	global_counter++; // Packet counter 
        	
        	if(global_counter % 100 ==0) { // Executes every 2 seconds
        		ii++;
			////printk("Counter=%d\n",ii);
			my_device.battery_value=ii;
			k_work_submit(&my_device.work); // Schedule a work in the workqueue to notify battery level
        	}
        	
        	if(global_counter % 400 ==0) { // Executes every 8 seconds
        	   	y = loop();
                        for(int i=0;i<16;i++){
                          tempVal.float_val = y[i];
                          dataPacket[counts1++] = tempVal.floatcast[0];
                          dataPacket[counts1++] = tempVal.floatcast[1];
                          dataPacket[counts1++] = tempVal.floatcast[2];
                          dataPacket[counts1++] = tempVal.floatcast[3];             
                        }

        	    	dataPacket[TFMICRO_DATA_LEN-2] = (uint8_t)((global_counter& 0xFF00)>>8);
        	    	dataPacket[TFMICRO_DATA_LEN-1] = (uint8_t)((global_counter& 0x00FF));        	    
		    	my_service.dataPacket = dataPacket;
		    	my_service.packetLength = sizeof(dataPacket);
		    	////printk("global counter=%u,size=%u\n",global_counter,sizeof(dataPacket));
		    	k_work_submit(&my_service.work); // Schedule a work in the workqueue to send TF lite data
        	}    
	        
           break;

        default:
            //Do nothing.
            break;
    }
}



// This is the default main used on systems that have the standard C entry
// point. Other devices (for example FreeRTOS or ESP32) that have different
// requirements for entry code (like an app_main function) should specialize
// this main.cc file in a target-specific subfolder.
int main(int argc, char* argv[]) {
  int blink_status = 0;	
  setup();
  IRQ_CONNECT(TIMER1_IRQn, TIMER_PRIORITY,
			nrfx_timer_1_irq_handler, NULL, 0);
  // Setup the LEDs for blinking while advertising	
  if (dk_leds_init()) {
		//printk("LEDs init failed\n");
		
	}
  // Setup the workqueue thread 
  k_work_q_start(&my_work_q, my_stack_area,
               K_THREAD_STACK_SIZEOF(my_stack_area), WORKQUEUE_PRIORITY);
               
  k_work_init(&my_device.work, bas_notify);             // associate Battery service with a qorkqueue  
  k_work_init(&my_service.work, tfMicro_notify);        // associate tensorflow service with another workqueue     
  
               
  ble_init();	// Initialize BLE
  tfMicro_service_init(); // Initaalize array for TF service
  while (true) {
  
      k_sleep(K_MSEC(1000));
      if(!connectedFlag) // blink LED when the device is not connected and is in advertising state
      	dk_set_led(RUN_STATUS_LED, (++blink_status) % 2);
      else
      	dk_set_led(RUN_STATUS_LED, 0);  // Do not blink if  the device is connected

  }
}
