# Ankermake2Mqtt
This repo is based on the modifications of the fork https://github.com/anselor/ankermake-m5-protocol/ from the orginal project https://github.com/Ankermgmt/ankermake-m5-protocol
Thanks for this awsome projects!

The ankermake2mqtt project forward the raw mqtt traffic from the ankermake cloud to a local mqtt server. Current readonly is supported

I recommend linux for this project. Not tested in other os environments

# Examples
To check what the diffrent command types mean check this out: https://github.com/Ankermgmt/ankermake-m5-research/blob/master/mqtt/message-types.md


Topic for local mqtt: ```ankermake2mqtt/printers/<printer_serial>/data```

Example topic: ```ankermake2mqtt/printers/AK7ZRM0A0101010101/data```

## Example printer idle

```json
[{"commandType": 1003, "currentTemp": 2100, "targetTemp": 0}, {"commandType": 1004, "currentTemp": 2039, "targetTemp": 0}]
```

# Setup
### ankermake-m5-protocol
First you need to download the project https://github.com/anselor/ankermake-m5-protocol/ to setup the config and install all python modules
Generate the login config file using the ```python3 ankerctl.py config login```.

This project is only needed to setup the login configuration

### Ankermake2Mqtt
Set your local mqtt server data in the ankermake2Mqtt project
Config.ini
```ini
[MQTT]
username = your_local_mqtt_username
password = your_local_mqtt_password
ip = your.local.mqtt.ip
port = 1883
```

# Running
To run ankermake2mqtt use ```python3 AnkerConnect.py mqtt mirror```

This can be run in a screen or a own service

## Legal

This project is **<u>NOT</u>** endorsed, affiliated with, or supported by AnkerMake. All information found herein is gathered entirely from reverse engineering using publicly available knowledge and resources.
