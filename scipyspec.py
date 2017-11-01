import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import sys
import numpy as np


sample_rate, samples = wavfile.read(sys.argv[1])
frequencies, times, spectogram = signal.spectrogram(samples, sample_rate)

print(np.array(spectogram).shape)

plt.imshow(spectogram)
plt.pcolormesh(times, frequencies, spectogram)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()