#include <zephyr.h>
#include <zephyr/types.h>
#include <sys/printk.h>
#include <device.h>
#include <drivers/pwm.h>
#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>
#include <bluetooth/conn.h>
#include <bluetooth/uuid.h>
#include <bluetooth/gatt.h>
#include <kernel.h>
#include <bluetooth/services/lbs.h>
#include <bluetooth/services/bas.h>
#include <settings/settings.h>
#include "common.h"

struct batteryInfo {
    struct k_work work;
    uint8_t battery_value; // user-defined value to pass as input to the work-queue
}; // work queue structure used to execute Batter level notification in a interrupt service handler initiated by a timer. 
extern struct batteryInfo my_device ;  // work-queue instance for batter level

static void bas_notify(struct k_work *);
static void battery_config(void)
{
	// Code for configuring the battery monitor chip to be called in the initalization
}

// Function that periodically extracts the battery level and needs to be called in a timer routine 
static void bas_notify(struct k_work *item)
{
    	struct batteryInfo* the_device=  ((struct batteryInfo *)(((char *)(item)) - offsetof(struct batteryInfo, work)));
        	
    	//printk("Battery value =%u\n", the_device->battery_value);
	uint8_t battery_level = the_device->battery_value;

	bt_bas_set_battery_level(battery_level);
}

