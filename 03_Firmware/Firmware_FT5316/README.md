# FT5316 - Firmware


This code is a form from [ft5x06-tool](https://github.com/boundarydevices/ft5x06-tool), largely inspired from the [Focaltech GitHub driver](https://github.com/focaltech-systems/drivers-input-touchscreen-FTS_driver).

## Requirements
### Equipments

- Raspberry Pi (+ USB power supply)
- Monitor + HDMI Cable
- Four female to female jumpers (for SDA/SCL & Power Supply)
- Capacitive Touch Shield with the soldered FT5316

### Software
The source code itself isn't depending any external library, so no build dependency.

As for runtime dependency, the kernel must have `i2c-dev` support enabled.

You need to have a physical access to the i2c ports, like Raspberry Pi. 

### Enable i2c-dev
- Turn ON the Raspberry Pi
- On the terminal, open Raspi-config: ```sudo raspi-config```
- The raspi-config utility will launch. Select ```Interfacing Options```.
- Highlight the ```I2C``` option and activate ```<Select>``` to enable the I2C.

### Hardware
- Power the capacitive touch shield with the 3.3V and GND pins of the Raspeberry Pi.
- Connect the GPIO2 (SDA) and GPIO3 (SCL) - the Raspberry Pi's I2C pins- to the shield. This will allow the two-wire communication. 

> Note: You can verify the address of connected I2C peripherals with a simple one-liner
```
sudo apt-get install i2c-tools
sudo i2cdetect -y 1 
```




## Build instructions

Very straight-forward:
```
$ git clone --single-branch -b PressureSensor https://github.com/CRI-MotionLab/SensitivePen.git
$ cd SensitivePen/03_Firmware/Firmware_FT5316
$ make
```


## Usage
To upload the firmware to the Capacitive Touch Shield (FT5316DME):

```
$ ./FT5316 -b 1 -c 0x0A -i FT5316Firmware.bin 
```

On a raspberry pi, the I2C bus is set to `1`. The chip id has to be forced because the firmware is empty. 

The tool has an help output which lists all the different parameters.
```
FT5x06 tool usage: ft5x06-tool [OPTIONS]
OPTIONS:
	-a, --address
		I2C address of the FT5x06 controller (hex). Default is 0x38.
	-b, --bus
		I2C bus the FT5x06 controller is on. Default is 1.
	-c, --chipid
		Force chip ID to the value (hex). Default is read from controller.
	-i, --input
		Input firmware file to flash.
	-o, --output
		Output firmware file read from FT5x06.
	-d, --debug
		Enable or disable I2C debug. Default 0, 1 to enable
	-h, --help
		Show this help and exit.
```