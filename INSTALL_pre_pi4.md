# Install

In sudo rasps-config:
GPU Mem	256
Fake KMS Driver

Required:
sudo apt-get install libopenhmd-dev
sudo pip3 install pi3d

(Optional) xbox controller:

sudo apt-get install -y libhidapi-libusb0 xboxdrv


(Recommended) Touch Test OPenGL and Pi3d are operations 

	(in a terminal on the Desktop):
	
	git clone https://github.com/pi3d/pi3d_demos.git
	cd pi3_demos
      	python3 Earth.py




===================
OpenHMD
git clone https://github.com/OpenHMD/OpenHMD			# commit id:  71829a902b8135e8e5557faaa488dc800685c949
cd OpenHMD
#sudo apt-get install meson libsdl2-dev
#meson ./build -Dexamples=simple


# Need to remove these packages as the current OpemHMD release/package has PSVR support disabled.
sudo apt-get remove libopenhmd0 libopenhmd-dev

sudo apt-get install cmake libsdl2-dev libhidapi-dev libhidapi-hidraw0
mkdir build
cd build
cmake ..  -DOPENHMD_DRIVER_PSVR=ON -DOPENHMD_EXAMPLE_SIMPLE=ON  -DBUILD_BOTH_STATIC_SHARED_LIBS=ON
make  
# Touchtest.  Using sudo as need to fix OmenHMD/USBHID permissions...
sudo ./examples/simple/simple
sudo make install
sudo ldconfig



git clone https://github.com/WayneKeenan/python-vrzero
cd python-vrzero
pip3 install --user --editable .
sudo -E python3 tests/test_openhmd.py 







# Legacy Install instructions 



Install the dependencies:

```bash
sudo apt-get update
sudo apt-get install -y xboxdrv
sudo pip3 install pi3d==2.23
sudo dpkg --install - <(curl -o- https://github.com/WayneKeenan/python-vrzero/install/libopenhmd0_0.3.0-1_armhf.deb)

```


Clone and install VR Zero:

```bash
git clone https://github.com/WayneKeenan/python-vrzero
cd python-vrzero
sudo python3 setup.py install
```

Settings for: root-less USB (HMD) access and and XBox Joypad:

```bash
sudo cp config/83-hmd.rules /etc/udev/rules.d/
sudo cp config/xboxdrv.init /etc/init.d/xboxdrv
sudo cp config/xboxdrv.defaults /etc/default/xboxdrv
```


If have a Rift DK1 or you want to test using a HDMI monitor then run:
```bash
sudo cp /boot/config.txt /boot/backup_config.txt
sudo cp config/config_DK1.txt /boot/config.txt
```


If you have a Rift DK2 then run:

```bash
sudo cp /boot/config.txt /boot/backup_config.txt
sudo cp config/config_DK2.txt /boot/config.txt
```



Run these commands, the first enables the root-less USB udev config setup earlier 
and the 2nd command disables BluetoothLE, which is currently needed to stop OpenGL ES hanging:
```bash
sudo udevadm control --reload-rules
sudo systemctl disable hciuart
```


Fix OpenGL ES

This is Raspbian release related, see Issue #8 for more info and the further link to Pi3D for more details on how to find these paths.

```shell
sudo ln -fs /opt/vc/lib/libEGL.so /usr/lib/arm-linux-gnueabihf/libEGL.so.1
sudo ln -fs /opt/vc/lib/libEGL.so /usr/lib/arm-linux-gnueabihf/libEGL.so.1.0.0 
sudo ln -fs /opt/vc/lib/libGLESv2.so /usr/lib/arm-linux-gnueabihf/libGLESv2.so.2
sudo ln -fs /opt/vc/lib/libGLESv2.so /usr/lib/arm-linux-gnueabihf/libGLESv2.so.2.0.0 
sudo ldconfig
```


Restart!

```bash
sudo reboot
```



# PS4 Controller Setup

Use long USB micro cable or pair using Bluetooth:

Run:
```
bluetoothctl
```

In the `bluetoothctl` shell:

```
scan on
```


Now put your Sony PlayStation 4 control pad into pairable mode by holding down the Share and PlayStation buttons until the light bar on the control pad flashes yellow. 
After a few seconds you should see at the `bluetoothctl` prompt that your control pad has been discovered, e.g

```
[NEW] Device DC:0C:2D:83:5F:A6 Wireless Controller
```

Then type, replacing what ever you see as `DC:0C:2D:83:5F:A6` for DEVICE_ADDRESS below:

```
scan off
pair DEVICE_ADDRESS
trust DEVICE_ADDRESS
```

You may get prompted, say yes:
```
[agent] Authorize service 00001124-0000-1000-8000-00805f9b34fb (yes/no): yes
```



## Quick test

Assuming this is the only controller connected it will be `/dev/input/js0`

```
sudo apt-get install jstest-gtk
jstest /dev/input/js0
```


# PSVR Operational notes

Turn on the PSVR before starting the Pi
Nothing will display until a demo is running 
The HMD will display black, you needd to 'wake' the PSVR up by putting it on or placeing your finger/hand neer the sensor between the lenses.
