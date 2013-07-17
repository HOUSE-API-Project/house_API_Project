#!/usr/bin/env python
#
# -*- coding: utf-8 -*-

import sys
import os
import signal
import time
import pyaudio
import optparse
import atexit
import math
import numpy as np


class Spectrum(object):

	DEVICE = 2 # PyAudio device index
	CHANNELS = 1
	RATE = 44100
	FRAME_LEN = 512
	FFT_SAMPLES = FRAME_LEN / 2
	PEAK_HOLD_FRAMES = 100
	FORMAT = pyaudio.paInt16
	__calls = 0
	__volume = []
	__debug = 0


	def __init__(self, device=None):
		signal.signal(signal.SIGINT, self.terminateHandler)
		self.pa = pyaudio.PyAudio()
		atexit.register(self.pa.terminate)
		self.FFT_SAMPLES = self.FRAME_LEN/2
		if(device and int(device) > 0):
			self.DEVICE = int(device)

		self.__peak = np.array(np.ones(self.FFT_SAMPLES, np.float64), dtype=np.float64)
		self.__peak *= -512


	def terminateHandler(self, signal, frame):
		print("Caught signal %d Terminating..." % signal)
		try:
			self.pa.terminate()
		except Exception as e:
			print str(e)

		sys.exit(2)



	def fft(self, samples):
		samples = samples / 2.0**15
		n = len(samples)
		win = np.hanning(len(samples))
		res = np.abs(((np.fft.fft(samples*win, self.FFT_SAMPLES*2)[0:n/2])/86.0)**2)
		freq = np.arange(0, self.FFT_SAMPLES, 1.0) * (self.RATE / n)
		return freq, (10*np.log10(res))


	def streamCallback(self, payload, frame_count, time_info, status):
		(self.__freq, vr) = self.fft(np.fromstring(payload, np.int16))
		np.putmask(self.__peak, vr > self.__peak, vr)
		power = vr[vr.argmax()]
		self.__volume.append(power)
		self.__calls += 1

		if(self.__debug):
			print "peak: ", self.__freq[vr.argmax()], " Hz, ", power

		return (payload, self.recording)


	def capture(self):
		self.recording = pyaudio.paContinue
		stream = self.pa.open(format = self.FORMAT,
						input_device_index = self.DEVICE,
						channels = self.CHANNELS, 
						rate = self.RATE, 
						input = True,
						output = False,
						frames_per_buffer = self.FRAME_LEN,
					    stream_callback = self.streamCallback
						)
		stream.start_stream()

		self.__calls = 0
		while stream.is_active():
			try:
				time.sleep(.5)
				if self.__calls > self.PEAK_HOLD_FRAMES:
					break
			except KeyboardInterrupt:
				self.recording = pyaudio.paAbort
				break

		stream.close()
		self.pa.terminate()


	def getBandPower(self):
		low = [80, 300]
		mid = [300,4000]
		high =[4000, 10000]

		lowindex = np.where((self.__freq > low[0]) & (self.__freq < low[1]))
		midindex = np.where((self.__freq > mid[0]) & (self.__freq < mid[1]))
		highindex = np.where((self.__freq > high[0]) & (self.__freq < high[1]))

		return (self.__peak[lowindex].mean(), self.__peak[midindex].mean(), self.__peak[highindex].mean())


	def getSpectrum(self):
		return (self.__freq, self.__peak)

	def getPower(self):
		return np.array(self.__volume).mean()

	def getDeviceList(self):
		counts = self.pa.get_device_count()
		return [self.pa.get_device_info_by_index(i) for i in range(counts)]

	def getDeviceInfo(self, index):
		if(index>0):
			return self.pa.get_device_info_by_index(index)


def main():
	spe = Spectrum(device=2)
	spe.capture()
	(freq, power) = spe.getSpectrum()


if __name__ == '__main__':
	main()


