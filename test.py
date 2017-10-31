import wave
import struct
from array import array
import matplotlib.pyplot as plt
from math import ceil

def block_energy(left, right, start, count):
	energy = 0
	for i in range(start, min(start+count, len(left))):
		energy += left[i]**2 + right[i]**2
	return energy

def energy_list(left, right, block_size):
	energylist = []	
	for i in range(ceil(len(left)/block_size)):
		energylist.append(block_energy(left, right, i * block_size, block_size))
	return energylist

def find_beats(energy_list, block_history_size):
	beats = [0]*len(energy_list)
	for i in range(block_history_size, len(energy_list)):
		avg_before = sum(energy_list[i-block_history_size:i]) / block_history_size
		if energy_list[i] > avg_before:
			beats[i] = 1

	return beats


with wave.open("100bpm.wav") as audio:
	(nchannels, sampwidth, framerate, nframes, comptype, compname) = audio.getparams()
	print("Channels: %d" % nchannels)
	print("Sample width (bytes): %d" % sampwidth)
	print("Frame rate: %d" % framerate)
	print("Frames number: %d" % nframes)

	frames_to_read = min(60 * framerate * nchannels, int(nframes * nchannels))

	length_sec = frames_to_read*1.0/framerate/nchannels
	print("Length: %fs" % length_sec)

	frames = audio.readframes(frames_to_read)
	out = struct.unpack_from("%dh" % frames_to_read, frames)

	if nchannels == 2:
		left = list(out[0::2])
		right = list(out[1::2])
	else:
		left = out
		right = left

	en = energy_list(left, right, 1024)
	beats = find_beats(en, 43)
	print(beats)
	print(len(en))

	beat_count = 0
	last = 0
	for beat in beats:
		if last == 0 and beat > 0:
			beat_count += 1
		last = beat
	
	print(beat_count/length_sec*60, "BPM")

	#for beat in beats:

	plt.plot([beat * 1.1 * max(en) for beat in beats])
	plt.plot(range(len(en)), en)
	plt.show()