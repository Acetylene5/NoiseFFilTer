import scipy
import matplotlib.pyplot as pyplot
import pyaudio
import numpy

fig = pyplot.figure(0)
p = pyaudio.PyAudio()

# Sound parameters
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 3
MAX_y = 2.0**(p.get_sample_size(FORMAT) * 8 - 1)



s1 = p.open(format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            output=False,
            frames_per_buffer=chunk)

print "* Recording"
data = []

# Listen, record background
for i in range(0, RATE/chunk*RECORD_SECONDS):
    d1 = numpy.fromstring(s1.read(chunk), dtype=numpy.short)
    data.extend(d1.tolist())

s1.stop_stream()

#Normalize the data
background = numpy.array(data)/MAX_y
raw_input("Enter to continue")

s1.start_stream()
print "* Recording"
data = []

# Listen, record sound of interest
for i in range(0, RATE/chunk*RECORD_SECONDS):
    d1 = numpy.fromstring(s1.read(chunk), dtype=numpy.short)
    data.extend(d1.tolist())

# Normalize the data
data = numpy.array(data)/MAX_y

# Close audio stream
s1.stop_stream()
s1.close()
p.terminate()

print 'Done recording!'

# Calculate FFT
sp_data = numpy.fft.fft(data)
sp_bkg = numpy.fft.fft(background)

# Calculate Power Spectrum (for plotting)
sp_data_power = numpy.abs(numpy.fft.fft(data)**2.0)
sp_bkg_power = numpy.abs(numpy.fft.fft(background)**2.0)

# Calculate Spectral frequencies
freq_bkg = numpy.fft.fftfreq(background.shape[-1], d=1.0/RATE)
freq_data = numpy.fft.fftfreq(data.shape[-1], d=1.0/RATE)

# Divide (?) Data spectrum by Background spectrum
sp_bkgdiv = sp_data/sp_bkg
sp_bkgdiv_power = numpy.abs(sp_bkgdiv**2.0)
bkgdiv_data = numpy.fft.ifft(sp_bkgdiv)

# Subtract (?) Background spectrum from Data spectrum
sp_bkgsub = sp_data - sp_bkg
sp_bkgsub_power = numpy.abs(sp_bkgsub**2.0)
bkgsub_data = numpy.fft.ifft(sp_bkgsub)

# Plot Power spectra
fig.clear()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

# Background
ax.plot(freq_bkg, sp_bkg_power, label='Background')

# Data
ax.plot(freq_data, sp_data_power, label='Data')


ax.set_xbound(0.1, 600)
ax.set_xlabel("Frequency - Hz")
ax.set_ylabel("Power")
ax.set_yscale('log')
ax.legend()
fig.savefig('Spectrum.png')
ax.set_xbound(350, 500)
fig.savefig('Spectrum_zoom.png')

fig.clear()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

# Background-Divided
ax.plot(freq_data, sp_bkgdiv_power, label='Divided', color = 'r')

# Background-Subtracted
ax.plot(freq_data, sp_bkgsub_power, label='Subtracted', color = 'c')

ax.set_xbound(0.1, 600)
ax.set_xlabel("Frequency - Hz")
ax.set_ylabel("Power")
ax.set_yscale('log')
ax.legend()
fig.savefig('Spectrum_clean.png')
ax.set_xbound(350, 500)
fig.savefig('Spectrum_clean_zoom.png')

npts = 3000
WAVE = 440
x = numpy.arange(npts)/float(RATE)
y = numpy.sin(x*WAVE*numpy.pi)*numpy.max(data) * 0.5

# Plot the background, observed, and cleaned data
fig.clear()

ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax.plot(x, background[0:npts], label = 'Background')
ax.plot(x, data[0:npts], label = 'Data')
ax.plot(x, bkgdiv_data[0:npts], label = 'Divided', color = 'r')
ax.plot(x, bkgsub_data[0:npts], label = 'Subtracted', color = 'c')
ax.plot(x, y, label = 'Expected', color = 'k')
ax.set_ylabel("Normalized Amplitude")
ax.set_xlabel("Time (s)")
ax.legend()

fig.savefig("timeseq.png")
