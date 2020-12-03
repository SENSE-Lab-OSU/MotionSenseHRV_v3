from __future__ import print_function

from time import gmtime, strftime, sleep
from bluepy.btle import Scanner, DefaultDelegate, BTLEException
import sys
from bluepy.btle import UUID, Peripheral, ADDR_TYPE_RANDOM, DefaultDelegate
import argparse
import time
import struct
import binascii
import os
import sys
import threading
import time
import subprocess
import numpy as np

from threading import Thread
import subprocess



'''
For Adaptive setting:
20 s calibration time. Have some margin from Saturation, ma.
Hyperparams: ma, thres_max for green S/N, thres_min for infra/red DC value.
Green (main Channel): Start Green from (maximum intensity-ma) and reduce it until S/N ratio is < thres_max. Then set it to the previous intensity.
Red/Infrared (noise channel): Start increasing intensity and keep it in some range, i.e. as long as DC is > thres_min, STOP!. 
'''
# Gives root access to the Python script.
#"D4:F7:FA:85:56:AA","DD:44:77:53:96:0E","F0:77:95:41:44:62","D2:67:36:A2:9E:9F"
#bigmacs = np.array(["CE:29:1F:E7:26:8B", "FE:23:64:32:DF:41", "D4:F7:FA:85:56:AA"]);
bigmacs = np.array(["c3:68:c4:59:2f:19"]);
numSensors = 1

mac_address1 = bigmacs[0]


if os.geteuid() != 0:
    # os.execvp() replaces the running process, rather than launching a child
    # process, so there's no need to exit afterwards. The extra "sudo" in the
    # second parameter is required because Python doesn't automatically set $0
    # in the new process.
    # os.execvp("sudo", ["sudo"] + sys.argv)
    pass

def write_uint16(data, value, index):
    """ Write 16bit value into data string at index and return new string """
    data = data.decode('utf-8')  # This line is added to make sure both Python 2 and 3 works
    return '{}{:02x}{:02x}{}'.format(
                data[:index*4], 
                value & 0xFF, value >> 8, 
                data[index*4 + 4:])

def write_uint8(data, value, index):
    """ Write 8bit value into data string at index and return new string """
    data = data.decode('utf-8')  # This line is added to make sure both Python 2 and 3 works
    return '{}{:02x}{}'.format(
                data[:index*2], 
                value, 
                data[index*2 + 2:])

# The base UUID used in bluetooth services in all hardware setups.
def MotionSense_UUID(val):
    """ Adds base UUID and inserts value to return motionSenseHRV UUID """
    return UUID("DA39%04X-1D81-48E2-9C68-D0AE4BBD351F" % val)

# Definition of all UUID used by motionSenseHRV
BATTERY_SERVICE_UUID = 0xADF0
BATTERY_CHAR_UUID    = 0x2A19

MOTION_SERVICE_UUID  = 0x5D22
MOTION_ACCELERO_CHAR_UUID = 0xC922
CCCD_UUID            = 0x2902
TF_UUID = 0x5D22



# Notification handles used in notification delegate
m_motion_handle = None




class MotionServiceHRV():
    """
    Environment service module. Instance the class and enable to get access to the Environment interface.
    """
    serviceUUID         =   MotionSense_UUID(MOTION_SERVICE_UUID)
    motion_char_uuid   =   MotionSense_UUID(MOTION_ACCELERO_CHAR_UUID)
    
    def __init__(self, periph):
        self.periph             = periph
        self.motion_service     = None
        self.motion_char        = None
        self.motion_cccd        = None

    def enable(self):
        global m_motion_handle

        """ Enables the class by finding the service and its characteristics. """
        if self.motion_service is None:
            self.motion_service = self.periph.getServiceByUUID(self.serviceUUID)
        if self.motion_char is None:
            self.motion_char = self.motion_service.getCharacteristics(self.motion_char_uuid)[0]
            m_motion_handle = self.motion_char.getHandle()
            print(m_motion_handle)
            print(self.motion_char.getDescriptors())
            self.motion_cccd = self.motion_char.getDescriptors(forUUID=CCCD_UUID)[0]
        
    def set_motion_notification(self, state):
        if self.motion_cccd is not None:
            if state == True:
                self.motion_cccd.write(b"\x01\x00", True)
            else:
                self.motion_cccd.write(b"\x00\x00", True)


    def disable(self):
        self.set_motion_notification(False)

class MotionSenseHRVplus(Peripheral):
    def __init__(self, addr):
        Peripheral.__init__(self, addr, addrType=ADDR_TYPE_RANDOM)

        # Thingy configuration service not implemented
        self.motionHRVplus = MotionServiceHRV(self)

class MyDelegate(DefaultDelegate):
    ts = None;

    def handleNotification(self, hnd, data):
        if (hnd == m_motion_handle):
            self.ts = round(time.time()*1000)
            
            #print(data)
            data2Format = struct.unpack('>BH', data)
            #print("printing unformatted {}".format(binascii.b2a_hex(data).decode('utf-8')))
            #print(binascii.b2a_hex(data).decode('utf-8'))
            print("data={}, counter={}".format( data2Format[0], data2Format[1],))
          
        


class ScanDelegate(DefaultDelegate):

    def handleDiscovery(self, dev, isNewDev, isNewData):
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), dev.addr, dev.getScanData())
        sys.stdout.flush()
    
    def handleNotification(self, cHandle, data):
        print("data recived!")
        print("data = ", data)
        parsed = struct.pack('f', data)
        new_num = struct.unpack('16f', parsed)
        print(new_num)

        
def main():
    scanner = Scanner().withDelegate(ScanDelegate())

# listen for ADV_IND packages for 10s, then exit
    devices = scanner.scan(5.0, passive=True)

    for dev in devices:
         uu=dev.getScanData()
         if len(uu) >1:
              if uu[1][2] == "MotionSenseHRV3":
                   print(dev.addr)
                   mac_address1 = dev.addr
    e1 = 'sudo echo 8 > /sys/kernel/debug/bluetooth/hci0/conn_min_interval'
    e2 = 'sudo echo 13 > /sys/kernel/debug/bluetooth/hci0/conn_max_interval'
    subprocess.call(e1,shell=True);
    subprocess.call(e2,shell=True);
	
   # mac_address1 = "df:8f:a1:f5:23:84"
    #msHrv1 = MotionSenseHRVplus(mac_address1)
    #mac_address2 = bigmacs[int(sys.argv[1])] #"D4:F7:FA:85:56:AA"
    #mac_address1 = bigmacs[int(sys.argv[2])] #"DD:44:77:53:96:0E"
    #mac_address2 = sys.argv[1]

    msHrv1 = MotionSenseHRVplus(mac_address1)
    print('Connected sensor 1 ...')
    
    md1 = MyDelegate()
        
    
    msHrv1.motionHRVplus.enable()
        
    msHrv1.setDelegate(md1)    
        
    services = getServices()     
    msHrv1.motionHRVplus.set_motion_notification(True)
    #msHrv1.motionHRVplus.set_magneto_notification(True)   
    tf_sercive_UUID = 'DA395D22-1D81-48E2-9C68-D0AE4BBD351F'
    print("Connecting to Tf service UUID")

    print('Now collecting measurements...')     
    while 1:
         msHrv1.waitForNotifications(30)
         print("notification recived!")
    
         
         
    
#    sensor_t1 = threading.Thread(target=run_sensor1,args=(msHrv1,))  
#    sensor_t2 = threading.Thread(target=run_sensor2,args=(msHrv2,)) 
#    threads =[]
#    threads.append(sensor_t1)
#    threads.append(sensor_t2)
#
#
# 
#    
#       
#    sensor_t1.start()
#    sensor_t2.start()
    
        


if __name__ == "__main__":
    main()
