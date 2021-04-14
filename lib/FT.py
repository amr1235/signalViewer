from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import matplotlib.pyplot as plt
import struct
import soundfile as sf
from playsound import playsound
import sys

class fourierTransform() : 
    def __init__(self,data,sampling_rate) :
        
        self.data = data 
        self.sampling_rate = sampling_rate
        self.data_fft = np.fft.fft(self.data)
        # we will devide the range of freq into 10 ranges 
        # fmax = fsample / 2 
        self.maxFrequancy = self.sampling_rate / 2 
        #self.frequencies = (np.abs(self.data_fft[:int(self.maxFrequancy)]))
        self.frequencies = list( np.fft.fftfreq(len(self.data),1/self.sampling_rate) )
        bandWidthOfEachRange = int(self.maxFrequancy / 10)
        self.rangesOfFrequancy = [] # [[0,49],[50,99],...,[]] 10 elements
        start = 0
        end = bandWidthOfEachRange - 1
        for r in range(0,len(self.frequencies),bandWidthOfEachRange) : 
            self.rangesOfFrequancy.append([start,end])
            start = start + bandWidthOfEachRange
            end = end + bandWidthOfEachRange - 1
    
    # gain function takes 10 gains and it multiply each gain with the corresponding band  
    def gain(self,g1,g2,g3,g4,g5,g6,g7,g8,g9,g10) :
        self.dataAfterAmplification = self.data_fft
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
                self.dataAfterAmplification[j + int(self.maxFrequancy)] = self.data_fft[j + int(self.maxFrequancy)] * gain
        
        return self.dataAfterAmplification
    
    # get complex-number array and do inverse transform on it
    def fn_InverceFourier(self, complex_arr):
        invrs = np.fft.ifft(complex_arr) #[21.0,0.00000j] so we remove imaginary part
        real_data = list(invrs.real) #sound file data
        return real_data

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
    def fn_CreateSoundFile(file_name, arr_of_realNum, samplerate):# Error is here
        sf.write(file_name, arr_of_realNum, int(samplerate))
        sf.write(file_name, arr_of_realNum, int(samplerate))
       
    @staticmethod
    def fn_PlaySoundFile(file_name):
        playsound(file_name)

