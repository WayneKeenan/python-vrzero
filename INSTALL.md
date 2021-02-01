# Install
THese steps are for Pi4 and above.

git clone https://github.com/OpenHMD/OpenHMD
git clone https://github.com/WayneKeenan/python-vrzero

cd python-vrzero


## 1. Setup System (config.txt)

+ GPU Mem	256
+ Fake KMS Driver for OpenGL
+ Screen resolution to match PSVR

sudo cp /boot/config.txt /boot/config.txt.bak
sudo cp config/config_PSVR.txt /boot/

## 2. Install Pi3d 

sudo pip3 install pi3d==2.41


# 3. Install OpenHMD
```
cd ../OpenHMD
git checkout 71829a902b8135e8e5557faaa488dc800685c949
```

## Clean-up (optional)

If previous packages have been installed, remove them:
```
sudo apt-get remove libopenhmd0 libopenhmd-dev
```

## Build from source 

The pre-built packages do not have PSVR support enabled:

```
sudo apt-get install cmake libsdl2-dev libhidapi-dev libhidapi-hidraw0
mkdir build
cd build
cmake ..  -DOPENHMD_DRIVER_PSVR=ON -DOPENHMD_EXAMPLE_SIMPLE=ON  -DBUILD_BOTH_STATIC_SHARED_LIBS=ON
make  
sudo make install
sudo ldconfig
```

# 4. Install VRZero

```
cd ../../python-vrzero/
pip3 install --user  .
```

```
sudo reboot
```


# 5. Run demo

```
cd python-vrzero/demos
sudo -E python3 blockworld.py
```

The use of `sudo -E` is required because of OpenHMD device access and `vrzero` is installed into the `pi` users site libs.



---
# Other bits...

## PS4 Controller Setup

Pair using Bluetooth:

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





## Touch tests

### HMD tests

Using sudo as need to fix OmenHMD/USBHID permissions...

Native test:
```
cd OpenHMD
sudo ./examples/simple/simple
```

Python Test:
```
cd python
sudo -E python3 tests/test_openhmd.py 
```


### Joypad test

Assuming this is the only controller connected it will be `/dev/input/js0`

```
sudo apt-get install jstest-gtk
jstest /dev/input/js0
```

(Optional) xbox controller:
sudo apt-get install -y libhidapi-libusb0 xboxdrv


## OpenGL Test

in a terminal on the Desktop:
	
```
git clone https://github.com/pi3d/pi3d_demos.git
cd pi3_demos
python3 Earth.py
```



# PSVR Operational notes

Turn on the PSVR before starting the Pi.


The follow is from [RetroPie](https://retropie.org.uk/docs/PS4-Controller/).

## Powering PS4 controller off
The controller will not sleep on its own if left idle, it will remain on until the battery goes flat.

To force the controller to go to sleep, hold the PS button for 10 seconds.

Once the light bar turns off, the controller is asleep.

## Powering PS4 controller on

Tap the PS button.

The light bar will turn on. 

The controller will automatically re-connect to anything it's already been paired to.


