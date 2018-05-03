from lights import Lights
from time import sleep
import numpy as np
import scipy.io.wavfile
from scipy import signal
from sys import argv
from os import system
from time import time

if __name__ == '__main__':
	lights = Lights(argv[1])
	
	rate, samples = scipy.io.wavfile.read(argv[2])
	frequencies, times, spectrogram = signal.spectrogram(samples, rate)
	times = times[::2].tolist()
	spec = spectrogram[1][::2]
	print("START!")
	start = time()
	system('open ' + argv[2])

	for i, freq_time in enumerate(times):
		while freq_time > (time() - start):
			print("Waiting " + str(time() - start))
		print("Offset by " + str((time() - start) - freq_time))
		volume = spec[i]
		level = max(int(255 * (volume / max(spec)) - 20), 0)
		print(level)
		lights.set(2, level)