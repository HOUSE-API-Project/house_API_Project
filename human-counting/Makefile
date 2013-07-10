run:
	sudo python ./humancounter.py



all:
	gpio readall


setup:
	gpio -g mode 17 in


read:
	gpio -g read 17 in
	

watch:
	watch -n .1 gpio readall


