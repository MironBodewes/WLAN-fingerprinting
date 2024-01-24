from winsdk.windows.devices.wifi import WiFiAdapter
import subprocess

WiFiAdapter.request_access_async()
myWifi = WiFiAdapter.find_all_adapters_async()
while (myWifi.status == False): 
    pass #sleep would be better

if (myWifi.status == True): # this if-clause is redundant
    print("myWifi=", myWifi.id, myWifi.status)
    myWifi = myWifi.get_results()[0]
    WiFiAdapter.scan_async(myWifi)
