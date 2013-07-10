#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# 1wire Temperature sensor reader
# 
# Author: kuma at ultrasync.net
# 

import sys, time, re
import json


class w1TempSens(object):
	w1dir = "/sys/bus/w1/devices/w1_bus_master1/"
	slave_list = "w1_master_slaves"
	slave_name = "w1_slave"

	__slaves = []
	__temp = {}

	def __init__(self):
		self.__re_tempdetect = re.compile(r'^([a-zA-Z0-9]{2}\s+){9}t=(\d+)$')
		self.readSlaveList()


	def readSlaveList(self):
		"""Read w1 slave list"""
		self.__slaves = []
		with open(self.w1dir + self.slave_list) as slavelist:
			for line in slavelist:
				self.__slaves.append(line.rstrip("\r\n"))


	def parseW1Slave(self, input):
		"""Parse value from a slave"""
		if(input[0].rstrip("\r\n")[-3:] != "YES"):
			return None

		matches = self.__re_tempdetect.search(input[1].rstrip("\r\n"))
		if(matches):
			temp_c = int(matches.group(2)) / 1000.0
			if(-55.0 < temp_c and temp_c < 125.0): # see datasheet
				return temp_c
			else:
				return None


	def getTemperature(self):
		"""Get Temprature(s) from w1 sensor(s)"""
		self.__temp = {}
		for slave in self.__slaves:
			path = "%s/%s/%s" % (self.w1dir, slave, self.slave_name)	
			fp = open(path)
			result = fp.readlines()
			fp.close()

			temp = self.parseW1Slave(result)
			self.__temp[slave] = temp


	def getTemperatureListByJson(self):
		"""Get Temprature List By JSON"""
		response = []
		for slave in self.__slaves:
			sl = {}
			if(self.__temp[slave]):
				sl["status"] = "OK"
				sl["time"] = int(time.time())
				sl["sensor"] = {}
				sl["sensor"]["identifier"] = slave
				sl["sensor"]["resolution_bit"] = 12
				sl["sensor"]["type"] = "DS18B20"
				sl["sensor"]["offset"] = 0
				sl["temperatureC"] = self.__temp[slave]
				sl["name"] = ""
				sl["temperatureF"] = None
				sl["humidity"] = None
				sl["geometry"] = {}
				sl["geometry"]["location"] = {}
				sl["geometry"]["location"]["lat"] = None
				sl["geometry"]["location"]["lng"] = None
			else:
				sl["status"] = "N/A"
			
			response.append(sl)
		
		return json.dumps(response, indent=4)


	@property
	def getSlaveList(self):
		return self.__slaves

	def getTemperatureList(self):
		return self.__temp


if __name__ == "__main__":
	
	w1 = w1TempSens()
	w1.getTemperature()
	print w1.getTemperatureListByJson()

	sys.exit(1)


