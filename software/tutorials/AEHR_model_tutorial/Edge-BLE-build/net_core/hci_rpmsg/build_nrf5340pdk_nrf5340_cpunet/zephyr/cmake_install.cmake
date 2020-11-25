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
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/zephyr/arch/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/zephyr/lib/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/zephyr/soc/arm/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/zephyr/boards/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/zephyr/subsys/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/zephyr/drivers/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/modules/nrf/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/modules/mcuboot/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/modules/mcumgr/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/modules/nrfxlib/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/modules/cmsis/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/modules/canopennode/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/modules/civetweb/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/modules/fatfs/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/modules/nordic/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/modules/st/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/modules/libmetal/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/modules/lvgl/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/modules/mbedtls/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/modules/open-amp/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/modules/loramac-node/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/modules/openthread/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/modules/segger/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/modules/tinycbor/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/modules/tinycrypt/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/modules/littlefs/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/modules/mipi-sys-t/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/modules/nrf_hw_models/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/zephyr/kernel/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/zephyr/cmake/flash/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/zephyr/cmake/usage/cmake_install.cmake")
  include("/home/devan/Documents/ncs/zephyr/samples/bluetooth/hci_rpmsg/build_nrf5340pdk_nrf5340_cpunet/zephyr/cmake/reports/cmake_install.cmake")

endif()

