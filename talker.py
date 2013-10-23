import scipy
import matplotlib.pyplot as pyplot
import pyaudio
import numpy

fig = pyplot.figure(0)

# Sound Parameters
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
WAVE = 440.0
nsec = 10

# Generates a 1 second long sine wave
outdata = ''.join([chr(int(numpy.sin(x/((RATE/WAVE)/numpy.pi))*127+128)) for x in xrange(RATE)])

# Opens the output stream
p = pyaudio.PyAudio()
s2 = p.open(format=pyaudio.paInt16,
            channels=CHANNELS,
            rate=RATE,
            input=False,
            output=True,
	    frames_per_buffer=chunk)

# Plays the sound
for DISCARD in xrange(nsec):
    s2.write(outdata)

# Closes everything
s2.stop_stream()
s2.close()
p.terminate()

