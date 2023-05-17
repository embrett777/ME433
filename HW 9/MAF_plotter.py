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

X = 90
datanew = [None for x in range(len(data)-X)] #low pass filtered data
tnew = t[0:-X]

for i in range(len(data)-X):
    datanew[i] = sum(data[i:i+X])/X

fig, (ax1, ax2) = plt.subplots(2, 1)
ax1.plot(t,y,'k',linewidth='1')
ax1.plot(tnew,datanew,'r',linewidth='0.75')
ax1.set_xlabel('Time')
ax1.set_ylabel('Amplitude')
ax2.loglog(frq,abs(Y),'k',linewidth='1') # plotting the fft
ax2.set_xlabel('Freq (Hz)')
ax2.set_ylabel('|Y(freq)|')
ax1.set_title(f'SigD With Moving Average Filter, X={X}')

tot_time = tnew[-1]
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

ax2.loglog(frq,abs(Y),'r',linewidth='0.75') # plotting the fft

plt.show()

