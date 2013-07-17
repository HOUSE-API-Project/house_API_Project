#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
import time
import spectrum
import json
import numpy as np

#import pylab
from pprint import pprint


class noiseLevel(object):

	__apiurl = "http://0x00.be/echo.pl"

	def __init__(self, apiurl = None):
		if(apiurl):
			self.__apiurl = apiurl


	def getNoiseLevelByJson(self):
		deviceIndex = 1L
		sp = spectrum.Spectrum(device=deviceIndex)
		deviceInfo = sp.getDeviceInfo(deviceIndex)
	
		sp.capture()
		(freq, power) = sp.getSpectrum()
		totalpower = sp.getPower()
		bandpower = sp.getBandPower()
		
	
		status={}
		status["status"] = "OK"
		status["name"] = None
		status["device"] = deviceInfo["name"]
		status["signal_db"] = totalpower
		status["peak_hz"] = freq[power.argmax()]
		status["time"] = int(time.time())
		status["powerperband"] = dict(zip(["low", "mid", "high",], bandpower))
#		status["spectrum"] = dict(zip(list(freq),list(power)))

		# pylab.plot(freq, power)
		# pylab.show()
		return json.dumps(status, indent=4)


def usage():
	pass


def main():
	web = noiseLevel()
	payload = web.getNoiseLevelByJson() 
	print payload



if __name__ == "__main__":
	main()
	sys.exit(0)


