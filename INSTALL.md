
# Install

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




