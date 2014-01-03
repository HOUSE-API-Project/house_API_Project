crontab edit

in case at the /home/pi directory.

git clone git@github.com:HOUSE-API-Project/house_API_Project.git

crontab -e

* * * * * /usr/bin/ruby /home/pi/house_API_Project/wifi/wifi_3f.rb

* * * * * python /home/pi/ayafuji_work/house_API_Project/temperature/ds18b20.py

* * * * * /usr/bin/ruby /home/pi/ayafuji_work/house_API_Project/temperature/temperature.rb

* * * * * /usr/bin/ruby /home/pi/house_API_Project/wifi/wifi_1f.rb

* * * * * /usr/bin/ruby /home/pi/house_API_Project/wifi/wifi_2f.rb

* * * * * /usr/bin/ruby /home/pi/house_API_Project/wifi/wifi_bf.rb

* * * * * sudo python /home/pi/house_API_Project/humidity/humidity_dht22.py
