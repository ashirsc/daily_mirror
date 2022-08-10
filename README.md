# daily_mirror


https://towardsdatascience.com/building-a-face-recognizer-in-python-7fd6630c6340


# Arducam setup
```
cd ~
sudo apt remove libcamera0
wget -O install_pivariety_pkgs.sh https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/install_pivariety_pkgs.sh
chmod +x install_pivariety_pkgs.sh
./install_pivariety_pkgs.sh -p libcamera_dev
./install_pivariety_pkgs.sh -p libcamera_apps
```
## imx519
```
./install_pivariety_pkgs.sh -p imx519_kernel_driver_low_speed

cd ~
sudo apt install git bc bison flex libssl-dev
sudo wget https://raw.githubusercontent.com/RPi-Distro/rpi-source/master/rpi-source -O /usr/local/bin/rpi-source && sudo chmod +x /usr/local/bin/rpi-source && /usr/local/bin/rpi-source -q --tag-update
rpi-source

cd ~
git clone https://github.com/umlaeute/v4l2loopback.git
cd v4l2loopback
make clean && make
make && sudo make install
sudo depmod -a
```
### after set up this is all that is need to run
```
sudo modprobe v4l2loopback video_nr=3
gst-launch-1.0 libcamerasrc ! 'video/x-raw,width=1920,height=1080' ! videoconvert ! tee ! v4l2sink device=/dev/video3
```
