import wave
import struct
from array import array
import matplotlib.pyplot as plt
from math import ceil
import numpy as np
import numpy.fft as fft
import time
import pyaudio

def calc_fft(data, sample_rate):
	fft_vals  =	fft.fft(data)
	#for v in fft_vals:
	#	print(v, np.abs(v))
	fft_freqs = fft.fftfreq(len(data), sample_rate)

	return (fft_freqs[:len(data)/2], fft_vals[:len(data)/2])

def get_bins(data, count):
	return [sum(bin_arr) for bin_arr in np.array_split(data, count)]


with wave.open("audio.wav") as audio:
	(nchannels, sampwidth, framerate, nframes, comptype, compname) = audio.getparams()
	print("Channels: %d" % nchannels)
	print("Sample width (bytes): %d" % sampwidth)
	print("Frame rate: %d" % framerate)
	print("Frames number: %d" % nframes)

	frames_to_read = min(120 * framerate * nchannels, int(nframes * nchannels))

	length_sec = frames_to_read*1.0/framerate/nchannels
	print("Length: %fs" % length_sec)

	frames = audio.readframes(frames_to_read)
	out = struct.unpack_from("%dh" % frames_to_read, frames)

	if nchannels == 2:
		left  = list(out[0::2])
		right = list(out[1::2])
	else:
		left  = out
		right = left

	p = pyaudio.PyAudio()

	stream = p.open(format=p.get_format_from_width(sampwidth),
	                channels=1,
	                rate=framerate*nchannels,
	                output=True)

	
	v = []
	chunksize = 1024
	for i in range(int(len(left)/chunksize)):		
		v.append(calc_fft(left[i*chunksize:(i+1)*chunksize], 1/framerate))

	bins = 32
	upperbounds = []
	for b in range(bins):
		print(b, (b*1.0/bins)*(framerate*0.5), ((b+1)*1.0/bins)*(framerate*0.5))
		upperbounds.append(((b+1)*1.0/bins)*(framerate*0.5))

	fig = plt.figure()
	plt.ion()

	low_freq_hist = []

	beat_hist = []
	last_was_beat = False

	for idx, (fft_freqs, fft_vals) in enumerate(v):
		curr_bins = get_bins(np.abs(fft_vals)**2, bins)

		play = []
		for element in (np.array(left[idx*chunksize:(idx+1)*chunksize])):
			play.append( element 		& 255)
			play.append((element >> 8)  & 255)
			play.append((element >> 16) & 255)
			play.append((element >> 32) & 255)
		stream.write(bytes(play))				
		
		low_freq_hist.append(curr_bins[0])
		
		if len(low_freq_hist) > 2:
			hist = low_freq_hist[:-1]
			avgval = sum(hist)/len(hist)
			print(" " * 50, end="\r")
			if low_freq_hist[-1] > avgval:
				#print("BEAT", end="\r")								
				
				if not last_was_beat:
					beat_hist.append(True)
					last_was_beat = True
				else:
					beat_hist.append(False)
			else:
				print("-",end="\r")
				beat_hist.append(False)
				last_was_beat = False

			elements_per_sec = int(framerate / chunksize)
			histlen = 3 #sec			

			print(len([x for x in beat_hist[-(elements_per_sec*histlen):] if x])*int(60/histlen), end="\r")

		#plt.bar(upperbounds, curr_bins, width=int(0.75*upperbounds[0]))
		#plt.draw()
		#plt.pause(chunksize*1.0/framerate)		
		#plt.clf()	
	
	plt.close(fig)

	stream.stop_stream()
	stream.close()

	p.terminate()