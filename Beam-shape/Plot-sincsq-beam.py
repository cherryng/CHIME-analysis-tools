import numpy as np
import sys
import matplotlib as mpl
import pylab as plt
import math

SPEED_OF_LIGHT = 3e8
R2D = 180./math.pi

def beam_fwhm(N_feed, feed_sep, freq):
    airy_diameter = (N_feed - 1) * feed_sep / 0.87
    wavelength = SPEED_OF_LIGHT / (freq * 1.0e6)
    return 180.0 / np.pi * np.arcsin(wavelength / airy_diameter)

def sincsq(yoff, FWHM):
    sincsq_halfmax = 0.44295
    return np.sinc(sincsq_halfmax*2 * yoff /  FWHM)** 2

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(1, 1, 1)

yoffs = np.arange(-2,2,0.01) #Range of offsets in deg
beamshape = np.zeros(len(yoffs))

#CHIME beam
FWHM = beam_fwhm(256, 0.3, 600)
print(f'Freq=600MHz  FWHM={FWHM:2}')
for y in range(len(yoffs)):
    beamshape[y] = sincsq(yoffs[y],FWHM)
ax.plot(yoffs,beamshape,label='chime zenith beam in NS',c="k")
x1 = find_nearest(beamshape,0.5)
x2 = len(beamshape)-x1
ax.plot((yoffs[x1],yoffs[x2]),(0.5,0.5),c="k")
ax.annotate("FWHM="+str(np.around(FWHM,1))+"deg",(0,0.5),ha="center")

ax.plot(yoffs,np.sinc(yoffs)**2,label='sinc$^{2}$')
ax.set_ylabel('Normalized intensity')
ax.set_xlabel('Offset in degree')
plt.title('Synthesized beam shape approximated by sinc$^{2}$')
plt.grid()
plt.legend()
#plt.show()
plt.savefig('CHIME-synthesized-sincsq-beam.png',bbox_inches='tight')
