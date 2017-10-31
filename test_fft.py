import numpy as np
import numpy.fft as fft
import matplotlib.pyplot as plt

def calc_fft(data, sample_rate):
	fft_vals  =	fft.fft(data)
	fft_freqs = fft.fftfreq(len(data), sample_rate)

	return (fft_freqs[:len(data)/2], fft_vals[:len(data)/2])

fps = 1024
seconds = 10
frame_count = fps * seconds 
frame_rate = 1.0 / fps 
x = np.linspace(0.0, frame_rate * frame_count, frame_count)
freqs = [50]
y = np.zeros(frame_count)
for freq in freqs:
	y += np.sin(freq * np.pi * 2 * x)

(fft_freqs, fft_vals) = calc_fft(y, frame_rate)

#plt.plot(y)
plt.plot(fft_freqs, np.abs(fft_vals))
plt.show()