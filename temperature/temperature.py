#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
import ds18b20


class putTemperature(object):

	__apiurl = "http://0x00.be/echo.pl"

	def __init__(self, apiurl = None):
		if(apiurl):
			self.__apiurl = apiurl


	def pushTemperature(self, payload):
		headers = {'content-type': 'application/json'}
		r = requests.post(self.__apiurl, headers=headers, data=payload)

		if(r.status_code != 200):
			sys.stderr.write("%s %s\n" % (r.status_code, r.text))
			return 1

		return 0




if __name__ == "__main__":

	w1 = ds18b20.w1TempSens()
	w1.getTemperature()
	payload = w1.getTemperatureListByJson()
	
	web = putTemperature(apiurl = "http://0x00.be/echo.pl")
	exitcode = web.pushTemperature(payload)

	sys.exit(exitcode)
