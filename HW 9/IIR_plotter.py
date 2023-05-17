import csv
import matplotlib.pyplot as plt # for plotting
import numpy as np

t = [] # column 0
data = [] # column 1

with open("C:\\Users\enyab\Documents\GitHub\ME433\HW9\sigD.csv") as f:
    # open the csv file
    reader = csv.reader(f)
    for row in reader:
        # read the rows 1 one by one
        t.append(float(row[0])) # leftmost column
        data.append(float(row[1])) # second column

tot_time = t[-1]
Fs = len(data)/tot_time
Ts = 1.0/Fs; # sampling interval
ts = np.arange(0,t[-1],Ts) # time vector
y = data # the data to make the fft from
n = len(y) # length of the signal
k = np.arange(n)
T = n/Fs
frq = k/T # two sides frequency range
frq = frq[range(int(n/2))] # one side frequency range
Y = np.fft.fft(y)/n # fft computing and normalization
Y = Y[range(int(n/2))]

fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(t,y,'k',linewidth='1')
ax1.set_xlabel('Time')
ax1.set_ylabel('Amplitude')
ax2.loglog(frq,abs(Y),'k',linewidth='1') # plotting the fft
ax2.set_xlabel('Freq (Hz)')
ax2.set_ylabel('|Y(freq)|')

datanew = []
A = 0.95
B = 0.05
for dp in data:
    if len(datanew) == 0:
        datanew.append(0)
    else:
        datanew.append(datanew[-1]*A + dp*B)

tot_time = t[-1]
Fs = len(datanew)/tot_time
Ts = 1.0/Fs; # sampling interval
ts = np.arange(0,t[-1],Ts) # time vector
y = datanew # the data to make the fft from
n = len(y) # length of the signal
k = np.arange(n)
T = n/Fs
frq = k/T # two sides frequency range
frq = frq[range(int(n/2))] # one side frequency range
Y = np.fft.fft(y)/n # fft computing and normalization
Y = Y[range(int(n/2))]

ax1.plot(t,datanew,'r',linewidth='0.75')
ax2.loglog(frq,abs(Y),'r',linewidth='0.75') # plotting the fft
ax1.set_title(f'SigD With IIR Filter, A={A} and B={B}')

plt.show()

