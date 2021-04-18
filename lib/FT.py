from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
import struct
import soundfile as sf
from playsound import playsound
import sys
import random

class fourierTransform() : 
    def __init__(self,data,sampling_rate) :
        
        self.data = data 
        self.sampling_rate = sampling_rate
        self.data_fft = np.fft.fft(self.data)
        #filtering data 
        # for i in range(int(self.sampling_rate),len(self.data_fft)) : 
        #     self.data_fft[i] = self.data_fft[i] * 0
        self.dataAfterAmplification = list(self.data_fft).copy()
        # we will devide the range of freq into 10 ranges 
        # fmax = fsample / 2 
        self.maxFrequancy = self.sampling_rate / 2
        #self.frequencies = (np.abs(self.data_fft[:int(self.maxFrequancy)]))
        # self.frequencies = list( np.fft.fftfreq(len(self.data),1/self.sampling_rate) )
        bandWidthOfEachRange = int(self.maxFrequancy / 10)
        self.rangesOfFrequancy = [] # [[0,49],[50,99],...,[]] 10 elements
        self.numberOfSeconds = int(len(self.data_fft) / self.sampling_rate)
        print(len(self.data_fft))
        start = 0
        end = 0
        for r in range(0,10) : 
            start = r * bandWidthOfEachRange
            end = start + bandWidthOfEachRange 
            self.rangesOfFrequancy.append([start,end])
    # gain function takes 10 gains and it multiply each gain with the corresponding band  
    def gain(self,g1,g2,g3,g4,g5,g6,g7,g8,g9,g10) :
        numbersOfData = len(self.data_fft)
        for i in range(10) :
            bandWidth = self.rangesOfFrequancy[i]
            start = bandWidth[0]
            end = bandWidth[1]
            gain = locals()['g' + str(i + 1)]
            arr = self.data_fft[start:end + 1]
            # write positive and negative part part
            #print(start,end,self.maxFrequancy)
            for j in range(start,end + 1) :
                self.dataAfterAmplification[j] = self.data_fft[j] * gain
                self.dataAfterAmplification[numbersOfData - 1 - j ] = self.data_fft[numbersOfData - 1 - j] * gain
        return self.dataAfterAmplification
    # get complex-number array and do inverse transform on it
    def fn_InverceFourier(self, complex_arr):
        invrs = np.fft.ifft(complex_arr) #[21.0,0.00000j] so we remove imaginary part
        self.real_data = list(invrs.real) #sound file data
        return self.real_data

# offers utility need in sound file package
class soundfileUtility():
    # read wav file
    # returns sampling rate and sound data 
    @staticmethod
    def fn_ReadFile(file_name):
        data, samplerate = sf.read(file_name)
        return data, samplerate
      

    # create new sound file
    @staticmethod
    def fn_CreateSoundFile(arr_of_realNum, samplerate):# Error is here
        l = list(range(0, 10000))
        m = random.choice(l)
        sf.write(f'new_file_{m}.wav', arr_of_realNum, samplerate)
        playsound(f'new_file_{m}.wav')
       
    @staticmethod
    def fn_PlaySoundFile(file_name):
        playsound(file_name)
