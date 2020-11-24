# Install script for directory: /home/devan/Documents/ncs/zephyr

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "TRUE")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/zephyr/arch/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/zephyr/lib/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/zephyr/soc/arm/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/zephyr/boards/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/zephyr/subsys/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/zephyr/drivers/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/modules/nrf/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/modules/mcuboot/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/modules/mcumgr/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/modules/nrfxlib/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/modules/cmsis/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/modules/canopennode/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/modules/civetweb/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/modules/fatfs/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/modules/nordic/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/modules/st/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/modules/libmetal/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/modules/lvgl/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/modules/mbedtls/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/modules/open-amp/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/modules/loramac-node/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/modules/openthread/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/modules/segger/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/modules/tinycbor/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/modules/tinycrypt/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/modules/littlefs/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/modules/mipi-sys-t/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/modules/nrf_hw_models/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/zephyr/kernel/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/zephyr/cmake/flash/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/zephyr/cmake/usage/cmake_install.cmake")
  include("/home/devan/Documents/MotionSenseHRV_v3/software/tutorials/AEHR_model_tutorial/Edge-BLE-build/app_core/CodeTF_BLE_integrated/build_nrf5340dk_nrf5340_cpuapp/hci_rpmsg/zephyr/cmake/reports/cmake_install.cmake")

endif()

