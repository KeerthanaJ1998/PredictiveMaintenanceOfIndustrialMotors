import time
import sys
import ibmiotf.application
import ibmiotf.device
import random

#IBM Watson Device Credentials
organization="nzrc3j"
deviceType="RaspberryPi3"
deviceId="Raspikeethu"
authMethod="token"
authToken="keerthanaj98"

def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data)
    print(type(cmd.data))
    i=cmd.data("command")
    if i=="motor on":
        print("Motor on")
    elif i=="motor off":
        print("Motor off")

try:
    deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token":authToken}
    deviceCli=ibmiotf.device.Client(deviceOptions)

except Exception as e:
    print("Caught exception connecting deviced: %s" % str(e))
    sys.exit()

#Connect and send Datapoint
deviceCli.connect()

while True:
    #Sending Sensor Values to IBM Platform
    temperature=random.randint(50,100)
    humidity=random.randint(50,80)
    vibration=random.randint(0,1)
    current=random.randint(5,55)
    data={'Temperature':temperature, 'Humidity' : humidity, 'Vibration': vibration, 'Current': current}

    #Printing the Data
    def myOnPublishCallback():
        print("Published Temperature= %s C" %temperature, "Humidity= %s %%" %humidity, "Vibration= %s Hz" %vibration, "Current=%s AMP" % current)
    success=deviceCli.publishEvent("SensorData","json",data, qos=0, on_publish=myOnPublishCallback)
    if not success:
        print("Not Connected to IBM platform")
    time.sleep(2)

    deviceCli.commandCallback=myCommandCallback

#Disconnect the device and application from the cloud
deviceCli.disconnect()
