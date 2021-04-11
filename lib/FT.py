import numpy as np
import matplotlib.pyplot as plt
import struct

class fourierTransform : 

    def __init__(self,data,sampling_rate) :
        self.data_fft = np.fft.fft(data)
        # we will devide the range of freq into 10 ranges 
        # fmax = fsample / 2 
        self.maxFrequancy = sampling_rate / 2 
        self.frequencies = (np.abs(self.data_fft[:int(self.maxFrequancy)]))
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
        for i in range(10) :
            bandWidth = self.rangesOfFrequancy[i]
            start = bandWidth[0]
            end = bandWidth[1]
            gain = locals()['g' + str(i + 1)]
            arr = self.data_fft[start:end + 1]
            # write positive and negative part part
            print(start,end,self.maxFrequancy)
            for j in range(start,end + 1) : 
                self.data_fft[j] = self.data_fft[j] * gain
                self.data_fft[j + int(self.maxFrequancy)] = self.data_fft[j + int(self.maxFrequancy)] * gain
        
        return self.data_fft
