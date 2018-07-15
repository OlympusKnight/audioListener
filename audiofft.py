#!/usr/local/bin/python2.7
# _*_ coding: utf-8 _*_
# file: audiofft.py
# time: 2018/7/13 10:42 AM
# version: 1.0
# __author__: ChengChen
# contact: saicc4869@163.com
import numpy as np
from pyaudio import PyAudio, paInt16
from scipy import arange, fft, fromstring, roll, zeros

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets

fftLen = 2048
signal_scale = 1./1000
ch = 1
SAMPLING_RATE = 44100    #取样频率
NUM_SAMPLES = 2000      #pyaudio内置缓冲大小


def spectrumAnalyzer():
    app = QtWidgets.QApplication([])

    mainWindow = QtWidgets.QMainWindow()
    mainWindow.resize(800, 300)
    mainWindow.setWindowTitle('Spectrum Analyzer')

    centralWidget = QtWidgets.QWidget()
    mainWindow.setCentralWidget(centralWidget)

    lay = QtWidgets.QVBoxLayout()
    centralWidget.setLayout(lay)

    specWid = pg.PlotWidget(name='spectrum')
    specItem = specWid.getPlotItem()
    specItem.setYRange(0, 1000)
    specItem.setXRange(0, fftLen/2, padding=0)

    specAxis = specItem.getAxis("bottom")
    specAxis.setLabel('Frequency [Hz]')
    specAxis.setScale(SAMPLING_RATE/2./(fftLen/2+1))
    hz_interval = 500
    newXAxis = (arange(int(SAMPLING_RATE/2/hz_interval))+1)*hz_interval
    oriXAxis = newXAxis/(SAMPLING_RATE/2./(fftLen/2+1))
    specAxis.setTicks([zip(oriXAxis, newXAxis)])
    lay.addWidget(specWid)

    mainWindow.show()

    p = PyAudio()
    stream = p.open(format=paInt16, channels=ch, rate=SAMPLING_RATE,
                    input=True, frames_per_buffer=NUM_SAMPLES)
    signal = zeros(NUM_SAMPLES, dtype=float)

    while True:
        string_audio_data = stream.read(NUM_SAMPLES)
        data = fromstring(string_audio_data, dtype=np.int16)
        signal = roll(signal, -NUM_SAMPLES)
        signal[-NUM_SAMPLES:] = data
        fftspec = fft(signal)
        specItem.plot(abs(fftspec[1:int(fftLen/2+1)]*signal_scale), clear=True)
        app.processEvents()
        if not mainWindow.isActiveWindow():
            break


if __name__ == '__main__':
    spectrumAnalyzer()