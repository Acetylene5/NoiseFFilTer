import scipy
import scikits.audiolab as AL
#import pysox
import matplotlib.pyplot as pyplot
import pyaudio
import sys
import array
import numpy
import scipy.signal as signal

fig = pyplot.figure(0)

nFFT = 512
BUF_SIZE = 4*nFFT
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

p = pyaudio.PyAudio()

MAX_y = 2.0**(p.get_sample_size(FORMAT) * 8 - 1)

s1 = p.open(format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=False,
            frames_per_buffer=chunk)

print "* Recording"
data = []#numpy.array([], dtype=numpy.int16)

for i in range(0, RATE/chunk*RECORD_SECONDS):
    #d1 = array.array('h', s1.read(chunk))
    d1 = numpy.fromstring(s1.read(chunk), dtype=numpy.short)
    data.extend(d1.tolist())

s1.stop_stream()
background = numpy.array(data)/32768.0
#background /= numpy.median(background)
raw_input("Enter to continue")

s1.start_stream()
print "* Recording"
data = []

for i in range(0, RATE/chunk*RECORD_SECONDS):
    #d1 = array.array('h', s1.read(chunk))
    d1 = numpy.fromstring(s1.read(chunk), dtype=numpy.short)
    data.extend(d1.tolist())

data = numpy.array(data)/32768.0
#data /= numpy.median(data)
s1.stop_stream()
s1.close()
p.terminate()

#hanning = signal.hanning(200)
#data_hanning = signal.convolve(data, hanning)
sp_data_power = numpy.abs(numpy.fft.fft(data)**2.0)
sp_bkg_power = numpy.abs(numpy.fft.fft(background)**2.0)
sp_data = numpy.fft.fft(data)
sp_bkg = numpy.fft.fft(background)
#sp_data = numpy.abs(numpy.fft.fft(data)**2.0)
#sp_bkg = numpy.abs(numpy.fft.fft(background)**2.0)
#sp_hanning = numpy.abs(numpy.fft.fft(data_hanning)**2.0)
freq_bkg = numpy.fft.fftfreq(background.shape[-1], d=1.0/RATE)
freq_data = numpy.fft.fftfreq(data.shape[-1], d=1.0/RATE)
#freq_hanning = numpy.fft.fftfreq(data_hanning.shape[-1], d=1.0/RATE)

sp_bkgsub = sp_data/sp_bkg
sp_bkgsub_power = numpy.abs(sp_bkgsub**2.0)
bkgsub_data = numpy.fft.ifft(sp_bkgsub)

fig.clear()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
#ax.plot(freq_bkg, numpy.abs(sp_data-sp_bkg))
ax.plot(freq_bkg, sp_bkg_power)
ax.plot(freq_data, sp_data_power)
ax.plot(freq_data, sp_bkgsub_power)
#ax.plot(freq_hanning, sp_hanning)
#ax.plot(data)
#ax.plot(bkgsub_data)
#ax.plot(freq, sp.real, freq, sp.imag)
ax.set_xbound(0.1, 10000)
ax.set_yscale('log')
#ax.set_xscale('log')
fig.show()

raw_input()
fig.clear()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax.plot(data)
ax.plot(background)
ax.plot(bkgsub_data)
fig.show()

