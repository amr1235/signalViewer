import numpy as np  # for multi-dimensional containers
import pandas as pd  # for DataFrames
import matplotlib.pyplot as plt
import wave
import struct
frequency = [
    200, 210, 310, 410, 510, 610, 710, 810, 910, 1000, 1110, 1210, 1310, 1410,
    1510, 1610, 1710, 1810, 1910, 2000
]
amplitude = 20
sample_rate = 44100
start_time = 0
end_time = 10
theta = 0

fname = "WaveTest.wav"
time = np.arange(start_time, end_time, 1 / sample_rate)
data_size = len(frequency)
for i in range(20):
    sinewave = amplitude * np.sin(2 * np.pi * frequency[i] * time + theta)
sinewave = np.empty(len(time))
for i in range(20):
    sinewave += amplitude * np.sin(2 * np.pi * frequency[i] * time + theta)
list1 = sinewave.tolist()
wav_file = wave.open(fname, "w")
nchannels = 1
sampwidth = 2
framerate = int(sample_rate)
nframes = data_size
comptype = "NONE"
compname = "not compressed"
wav_file.setparams(
    (nchannels, sampwidth, framerate, nframes, comptype, compname))
print(len(list1))
for i in range(len(list1)):
    # write the audio frames to file
    wav_file.writeframes(struct.pack('h', int(list1[i] * amplitude / 2)))

plt.plot(time, list1)
plt.show()
wav_file.close()