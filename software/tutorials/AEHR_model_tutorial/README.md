# MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial
This folder contains the files related to AEHR_model_tutorial.
Install Docker to recreate environment with all dependencies.
If you want to install all requirements on your linux PC instead, install miniconda and follow the commands in both Dockerfiles step by step. In general, execute commands next to RUN directive.

Some Useful Commands:

At first: cd <..tutorials/AEHR_model_tutorial folder on local computer>

# To build only conda docker image (conda_gcc ~4.8GB)
docker build -f Dockerfile_conda_gcc -t conda_gcc .
# To build tf_micro deployment image (tfmicro_1 ~4.8GB + 4.7 GB) on top of conda docker image
docker build -f Dockerfile_zephyr_tfmicro -t tfmicro_1 .

# To run docker image in a container with bluetooth access on linux
docker run --rm --net=host --privileged -it -v <path to local shared folder>:/files/shared <image tag>:latest

#To enable running jupyter with usb access on linux
docker run --privileged -it -p 8888:8888 -v <path to local shared folder>:/files/shared -v /dev/bus/usb:/dev/bus/usb <image tag>:latest

#To enable running jupyter on any platform
docker run --privileged -it -p 8888:8888 -v <path to local shared folder>:/files/shared <image tag>:latest 

# To start a jupyter server inside the container
jupyter notebook --ip='*' --port=8888 --no-browser --allow-root