import wave
import struct
import sys
import os
import cv2
import numpy as np
import numpy.fft as fft

def calc_fft(data, sample_rate):
	fft_vals  =	fft.fft(data)
	fft_freqs = fft.fftfreq(len(data), sample_rate)

	return (fft_freqs[:int(len(data)/2)], fft_vals[:int(len(data)/2)])

def get_bins(data, count):
	return [sum(bin_arr) for bin_arr in np.array_split(data, count)]

def processFile(filename):
	if not os.path.exists(filename):
		print("%s does not exist" % filename)
		return

	with wave.open(filename) as wav:
		(nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
		print("Channels: %d" % nchannels)
		print("Sample width (bytes): %d" % sampwidth)
		print("Frame rate: %d" % framerate)
		print("Frames number: %d" % nframes)

		frames_to_read = min(10 * framerate * nchannels, int(nframes * nchannels))

		length_sec = frames_to_read*1.0/framerate/nchannels
		print("Length: %fs" % length_sec)

		frames = wav.readframes(frames_to_read)
		out = struct.unpack_from("%dh" % frames_to_read, frames)

		if nchannels == 2:
			left  = list(out[0::2])
			right = list(out[1::2])
		else:
			left  = out
			right = left

		bins = 256
		chunksize = 1024 # frames
		chunks = int(len(left)/chunksize)

		bin_height = 2
		img = np.zeros((bins * bin_height, chunks), np.uint8)

		for i in range(chunks):		
			(fft_freqs, fft_amps) = calc_fft(left[i*chunksize:(i+1)*chunksize], 1/framerate)
			fft_bins = get_bins(np.abs(fft_amps), bins)
			for freq_idx, freq_amp in enumerate(fft_bins):
				for j in range(bin_height):
					img[freq_idx*bin_height+j][i] = int(255.0*freq_amp/(max(fft_bins)+1))

		cv2.imshow("test", img)
		cv2.waitKey(0)
		#cv2.destroyAllWindows()








if __name__ == "__main__":
	processFile(sys.argv[1])