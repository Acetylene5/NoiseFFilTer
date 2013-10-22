import scipy
import scikits.audiolab as AL
#import pysox
import matplotlib.pyplot as pyplot
import pyaudio
import sys
import array
import numpy

fig = pyplot.figure(0)

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

WAVE = 440.0

outdata = ''.join([chr(int(numpy.sin(x/((RATE/WAVE)/numpy.pi))*127+128)) for x in xrange(RATE)])

p = pyaudio.PyAudio()

s2 = p.open(format=pyaudio.paInt16,
            channels=CHANNELS,
            rate=RATE,
            input=False,
            output=True,
	    frames_per_buffer=chunk)

for DISCARD in xrange(7):
    s2.write(outdata)

s2.stop_stream()
s2.close()
p.terminate()

