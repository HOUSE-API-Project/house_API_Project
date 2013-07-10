#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, signal, threading, time
import RPi.GPIO as GPIO
import requests
import json
import redis


#GPIO.setwarnings(False)


class humanCounter(object):

	IN  = 11
	INTERVAL = 60
	MAX_INTERVAL_SEC = 60*60*25
	__count = 0
	__interval = 0
	__count_min = __count_hour = __count_day = 0

	def __init__(self):
		signal.signal(signal.SIGINT, self.terminateHandler)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.IN,  GPIO.IN)
		GPIO.add_event_detect(self.IN, GPIO.BOTH, self.countEvent)
		self.__red = redis.Redis(host="127.0.0.1", db=0)

	def terminateHandler(self, signal, frame):
		print("Caught signal %d Terminating..." % signal)
		try:
			if self.pushTimerThread.isAlive():
				self.pushTimerThread.cancel()

			GPIO.remove_event_detect(self.IN)
		except Exception as e:
			print str(e)
		
		sys.exit(2)


	def countEvent(self, channel):
		input = GPIO.input(channel)
		status = 1 if(input) else 0
		print "detect : %s is %d" % (channel, input)

		if(status):
			key = int(time.time())
			self.__red.set(key, 1)
			self.__red.expire(key, self.MAX_INTERVAL_SEC)
			
		
	def getCountByJson(self):
		payload = {}
		payload["status"] = "OK"
		payload["sensor"] = {}
		payload["sensor"]["identifier"] = None
		payload["sensor"]["type"] = "Parallax PIR #910-28027"
		payload["name"] = None
		payload["count"] = []
		payload["count"].append({"count":self.__count_min, "interval": 60})
		payload["count"].append({"count":self.__count_hour, "interval": 3600})
		payload["time"] = int(time.time())
		payload["geometry"] = {}
		payload["geometry"]["location"] = {}
		payload["geometry"]["location"]["lat"] = None
		payload["geometry"]["location"]["lng"] = None

		return json.dumps(payload, indent=4)


	def selectCount(self):

		self.__count = 0
		self.__count_min = 0
		self.__count_hour = 0
		self.__count_day = 0
		timelimit  = int(time.time() - self.INTERVAL)
		timelimit_min  = int(time.time() - 60)
		timelimit_hour = int(time.time() - (60*60))
		timelimit_day  = int(time.time() - (60*60*24))

		res = self.__red.keys("*")
		for k in res:
			sec = int(k)
			if sec > timelimit_min:
				self.__count += 1
				self.__count_min += 1
			if sec > timelimit_hour:
				self.__count_hour += 1
			if sec > timelimit_day:
				self.__count_day += 1

		
		print self.getCountByJson()

		try:
			if self.pushTimerThread.isAlive():
				self.pushTimerThread.cancel()
		except Exception as e:
			pass

		self.pushTimerThread = threading.Timer(self.INTERVAL, self.selectCount)
		self.pushTimerThread.start()




if __name__ == "__main__":
	h = humanCounter()
	h.selectCount()

	while True:
		time.sleep(0.2)

	if(h.pushTimerThread.isAlive()):
		h.pushTimerThread.cancel()	
	
	sys.exit(0)

