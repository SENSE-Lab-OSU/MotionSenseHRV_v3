/* Copyright 2020 The TensorFlow Authors. All Rights Reserved.

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

//define target model to use
#define USENEWMODEL 0

#include "main_functions.h"

#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "constants.h"

#include "output_handler.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "tensorflow/lite/version.h"

#include "sample_test.cc"


#if USENEWMODEL == 1
#include "aencoder.h"
#define MODEL_LEN 123904
#define MODEL_HEADROOM 200000
#define g_modelurd 0
#else
#include "model.h"
#define MODEL_LEN 2512
#define MODEL_HEADROOM 676
#define g_modelurd2 0
#endif

#include <zephyr.h>

// Globals, used for compatibility with Arduino-style sketches.
namespace
{
tflite::ErrorReporter *error_reporter = nullptr;
const tflite::Model *model = nullptr;
tflite::MicroInterpreter *interpreter = nullptr;
TfLiteTensor *input = nullptr;
TfLiteTensor *output = nullptr;
int inference_count = 0;

// Create an area of memory to use for input, output, and intermediate arrays.
// Minimum arena size, at the time of writing. After allocating tensors
// you can retrieve this value by invoking interpreter.arena_used_bytes().
const int kModelArenaSize = MODEL_LEN;
// Extra headroom for model + alignment + future interpreter changes.
const int kExtraArenaSize = MODEL_HEADROOM;
const int kTensorArenaSize = kModelArenaSize + kExtraArenaSize;
static uint8_t tensor_arena[kTensorArenaSize];
} // namespace

// The name of this function is important for Arduino compatibility.
void setup()
{
	outputInit();

	// Set up logging. Google style is to avoid globals or statics because of
	// lifetime uncertainty, but since this has a trivial destructor it's okay.
	// NOLINTNEXTLINE(runtime-global-variables)

	static tflite::MicroErrorReporter micro_error_reporter;
	error_reporter = &micro_error_reporter;

	// Map the model into a usable data structure. This doesn't involve any
	// copying or parsing, it's a very lightweight operation.
        if (USENEWMODEL){
            model = tflite::GetModel(g_modelurd2);
            }
        else {
            model = tflite::GetModel(g_modelurd);
            }


	if (model->version() != TFLITE_SCHEMA_VERSION) {
		TF_LITE_REPORT_ERROR(
			error_reporter,
			"Model provided is schema version %d not equal "
			"to supported version %d.",
			model->version(), TFLITE_SCHEMA_VERSION);
		return;
	}

/* This pulls in all the operation implementations we need. However we might change
       this later on as we only really need dense and convulution functions for the autoencoder
       But, if we want models to be able to be swapped out during runtime, it should stay this way.*/

	// NOLINTNEXTLINE(runtime-global-variables)
	static tflite::AllOpsResolver resolver;

	// Build an interpreter to run the model with.
	static tflite::MicroInterpreter static_interpreter(model, resolver,
							   tensor_arena,
							   kTensorArenaSize,
							   error_reporter);
	interpreter = &static_interpreter;

	// Allocate memory from the tensor_arena for the model's tensors.
	TfLiteStatus allocate_status = interpreter->AllocateTensors();

	if (allocate_status != kTfLiteOk) {
		TF_LITE_REPORT_ERROR(error_reporter,
				     "AllocateTensors() failed");

		return;
	}

	// Obtain pointers to the model's input and output tensors.
	input = interpreter->input(0);
	output = interpreter->output(0);

	// Keep track of how many inferences we have performed.
	inference_count = 0;
}

// The name of this function is important for Arduino compatibility.
unsigned int loop()
{
        //first set our output array
        static float arr_result[16];

	//get a ppg sample to feed into the model. We this is an 8 second
	// sample for a total of 400 values, whitch should be placed in our input.
	

        TfLiteIntArray* n_dims = input->dims;
	// Place the calculated ppg value in the model's input tensor

        /*.f is not actually the floating point cast, it is a a structure member
        since it is a union, each of the . data types represents any possible input format.
        This could mean you could represent your input in uint8, or float32. We use
        float32 since that is the default specification for inputs and outputs in 
        tensorflow lite models.
        */

	float xval = 0;
        //get ready to load the test ppg data into the input tensor
        for (int i = 0; i<400; i++){
                xval = sample_data[i];
                input->data.f[i] = sample_data[i];
        }
        //just using this test variable to inspect whether everything checks out
        float test_bounds = input->data.f[399];



	//Now we run inference, and report any error
	TfLiteStatus invoke_status = interpreter->Invoke();
	if (invoke_status != kTfLiteOk) {
		TF_LITE_REPORT_ERROR(error_reporter,"Invoke failed");
				    
		return NULL;
	}

	// Read the predicted y value from the model's output tensor
	

	// Output the results. A custom HandleOutput function can be implemented
	// for each supported hardware target.

        
        for (int i = 0; i < 16; i++){
            arr_result[i] = output->data.f[i];
            }
        float y_1 = output->data.f[0];
        float y_2 = output->data.f[1];
        float y_16 = output->data.f[15];
	// Increment the inference_counter, and reset it if we have reached
	// the total number per cycle
	inference_count += 1;
        if (inference_count > 2000){
            inference_count = 0;
                       }
        int te = inference_count;
        printk("value returned, %d", te);
        //we return something random here since this is just to check to make sure ble is working.
	return te;	
}
  
