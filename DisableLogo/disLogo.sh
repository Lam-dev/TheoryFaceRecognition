echo "Y\n" | sudo -S -k  apt-get install plymouth-theme-*
echo "0\n" | sudo -S -k update-alternatives --config default.plymouth
sudo update-initramfs -u
sudo cp DisableLogo/boot.bmp /boot/boot.bmp 
