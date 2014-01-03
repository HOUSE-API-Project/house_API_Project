crontab edit

crontab -e

* * * * * /usr/bin/ruby /home/pi/cron/wifi_3f.rb
* * * * * python /home/pi/ayafuji_work/house_API_Project/temperature/ds18b20.py
* * * * * /usr/bin/ruby /home/pi/ayafuji_work/house_API_Project/temperature/temperature.rb
* * * * * /usr/bin/ruby /home/pi/cron/wifi_digiroom.rb
* * * * * /usr/bin/ruby /home/pi/cron/wifi_2f.rb
* * * * * /usr/bin/ruby /home/pi/cron/wifi_bf.rb
* * * * * sudo python /home/pi/cron/humidity_dht22.py