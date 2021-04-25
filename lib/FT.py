from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft
import struct
from soundfile import SoundFile as sf
import soundfile as sff
import winsound
import sys
import random
import os

class fourierTransform() : 
    def __init__(self,data,sampling_rate) :
        self.data = data 
        self.sampling_rate = sampling_rate
        self.data_fft = np.fft.fft(self.data) # 20 30 40 fmax = 50hz 
        # we will devide the range of freq into 10 ranges 
        # fmax = fsample / 2 
        self.maxFrequancy = self.sampling_rate / 2
        bandWidthOfEachRange = int(self.maxFrequancy / 10)
        self.rangesOfFrequancy = [] # [[0,49],[50,99],...,[]] 10 elements
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
            # write positive and negative part part
            #print(start,end,self.maxFrequancy)
            for j in range(start,end + 1) :
                self.data_fft[j] = self.data_fft[j] * gain
                self.data_fft[numbersOfData - 1 - j ] = self.data_fft[numbersOfData - 1 - j] * gain
        return self.data_fft
    # get complex-number array and do inverse transform on it
    def fn_InverceFourier(self, complex_arr):
        invrs = np.fft.ifft(complex_arr) #[21.0,0.00000j] so we remove imaginary part
        real_data = list(invrs.real) #sound file data
        return real_data
    
    def deleteRangeOfFrequancy(self,min,max) :
        numbersOfData = len(self.data_fft)
        for j in range(min,max + 1) :
                self.data_fft[j] = self.data_fft[j] * 0.0
                self.data_fft[numbersOfData - 1 - j ] = self.data_fft[numbersOfData - 1 - j] * 0.0
        return self.data_fft

# offers utility need in sound file package
class soundfileUtility():
    # read wav file
    # returns sampling rate and sound data 
    @staticmethod
    def fn_ReadFile(file_name):
        data, samplerate = sff.read(file_name)
        return data, samplerate

    # create new sound file
    @staticmethod 
    def fn_CreateSoundFile(arr_of_realNum, samplrate):
        file_handle = sf("Tdfgjdli.wav", mode='w' ,samplerate= samplrate
        ,channels=1, subtype=None, endian='FILE', format='WAV', closefd=True)
        file_handle.write(arr_of_realNum)
        file_handle.close()

    @staticmethod
    def fn_PlaySoundFile(file_name="Tdfgjdli.wav"):
        winsound.PlaySound(file_name, winsound.SND_FILENAME)
        os.remove(file_name)