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

#include "output_handler.h"

#include <zephyr.h>
#include <zephyr/types.h>
#include <sys/printk.h>
#include <device.h>
//#include <drivers/pwm.h>
#include <settings/settings.h>
#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>
#include <bluetooth/conn.h>
#include <bluetooth/uuid.h>
#include <bluetooth/gatt.h>
#include "common.h"





#define MIN_PERIOD_USEC (USEC_PER_SEC / 64U)


static unsigned int period;
static unsigned int new_period;

void outputInit()
{

	period = MIN_PERIOD_USEC;
}


unsigned int HandleOutput(tflite::ErrorReporter *error_reporter, float x_value,
		  float y_value)
{
new_period = (unsigned int)((period * (y_value + 1) )/2);
    if( new_period >= period){
        new_period = period;
    } 
    
	
	// Log the current X and Y values

   // pwm_pin_set_usec(pwm, PWM_CHANNEL, period, new_period , PWM_FLAGS);
 	 /* TF_LITE_REPORT_ERROR(error_reporter, "x_value: %f, y_value: %f\n",
			     static_cast<double>(x_value),
			     static_cast<double>(y_value));  */ 
return new_period;
}
