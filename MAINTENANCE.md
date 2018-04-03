## Bulding OpenHMD from source


```shell

sudo apt-get install autoconf libtool libhidapi-dev checkinstall

git clone https://github.com/OpenHMD/OpenHMD.git
cd OpenHMD

VERSION=0.3.0

#Optionally switch to version, e.g. git checkout tags/0.2.0  
#Note: library version and pkgname suffix is release dependant, i.e. change $VERSION, program-suffix & pkgname

./autogen.sh 
./configure --prefix=/usr --program-suffix=.0
make

sudo checkinstall --pkgname libopenhmd0 --pkgversion $VERSION --pkggroup libs --pkgsource https://github.com/OpenHMD/OpenHMD --requires libhidapi-libusb0,libc6
```
