from winsdk.windows.devices.wifi import WiFiAdapter
import subprocess

WiFiAdapter.request_access_async()
myWifi = WiFiAdapter.find_all_adapters_async()
while (True): # TODO
    if (myWifi.status == True):
        print("myWifi=", myWifi.id, myWifi.status)
        myWifi = myWifi.get_results()[0]
        break
WiFiAdapter.scan_async(myWifi)
