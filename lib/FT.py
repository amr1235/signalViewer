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
        #filtering data 
        for i in range(int(self.sampling_rate),len(self.data_fft)) : 
            self.data_fft[i] = self.data_fft[i] * 0 
        self.dataAfterAmplification = list(self.data_fft).copy()
        # we will devide the range of freq into 10 ranges 
        # fmax = fsample / 2 
        self.maxFrequancy = self.sampling_rate / 2 
        #self.frequencies = (np.abs(self.data_fft[:int(self.maxFrequancy)]))
        self.frequencies = list( np.fft.fftfreq(len(self.data),1/self.sampling_rate) )
        bandWidthOfEachRange = int(self.maxFrequancy / 10)
        self.rangesOfFrequancy = [] # [[0,49],[50,99],...,[]] 10 elements
        self.numberOfSeconds = int(len(self.data_fft) / self.sampling_rate)
        
        start = 0
        end = 0
        for r in range(0,10) : 
            start = r * bandWidthOfEachRange
            end = start + bandWidthOfEachRange 
            self.rangesOfFrequancy.append([start,end])
    # gain function takes 10 gains and it multiply each gain with the corresponding band  
    def gain(self,g1,g2,g3,g4,g5,g6,g7,g8,g9,g10) :
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
                self.dataAfterAmplification[j + int(self.maxFrequancy) - 1 ] = self.data_fft[j + int(self.maxFrequancy) - 1] * gain
        # if g1 ==0 and g2 ==0 and g3 == 0 and g4 == 0 and g5 == 0 and g6 == 0 and g7 == 0 and g8 == 0 and g9 == 0 and g10 == 0 :
        # #     # print(len(self.dataAfterAmplification))
        #     print(np.abs(np.fft.ifft(self.dataAfterAmplification[0 : int(self.maxFrequancy) * 2 + 5 ])))
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
    def fn_CreateSoundFile(file_name, arr_of_realNum, samplerate):# Error is here
        sf.write(file_name, arr_of_realNum, int(samplerate))
        sf.write(file_name, arr_of_realNum, int(samplerate))
       
    @staticmethod
    def fn_PlaySoundFile(file_name):
        playsound(file_name)
