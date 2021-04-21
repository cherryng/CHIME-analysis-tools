"""""""""
Read binary CHIME gain files for pulsar and FRB calibration
"""""""""
import struct
import sys
import numpy as np

DIR = sys.argv[1]
#Gains
gain = np.zeros((1024,2,4,256),dtype=complex)

for f in range(1024):
    gainfile = str(DIR)+"/quick_gains_"+str(f).zfill(4)+"_reordered.bin"
    with open(gainfile, 'rb') as inh:
        indata = inh.read()
    for p in range(2):
        for ew in range(4):
            for ns in range(256):
                start_real = ((p*512+ew*256+ns)*2)*4
                start_imag = ((p*512+ew*256+ns)*2+1)*4
                Real = struct.unpack('f', indata[start_real:start_real+4])[0]
                Imag = struct.unpack('f', indata[start_imag:start_imag+4])[0]
                gain[f,p,ew,ns] = Real + Imag*1j

print(str(DIR).split('_T')[0],':Real=[',np.round(np.min(gain.real),1),np.round(np.mean(gain.real),1),np.round(np.max(gain.real)
,1), "] Imag=[",np.round(np.min(gain.imag),1),np.round(np.mean(gain.imag),1),np.round(np.max(gain.imag),1),"]")
#print(str(DIR).split('_T')[0], np.round(np.mean(abs(gain*0.05)),1))
