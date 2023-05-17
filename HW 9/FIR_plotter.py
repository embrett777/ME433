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
print(Fs)
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
weightedvals = [
    -0.000000000000000001,
    0.000282970589546487,
    0.001204877787865870,
    0.002941370083944624,
    0.005726606005070869,
    0.009797711077828329,
    0.015326522879102166,
    0.022352296249991133,
    0.030729748201279557,
    0.040104674753698104,
    0.049924704168249935,
    0.059486405988859063,
    0.068013147274924704,
    0.074752090746301278,
    0.079074740770195606,
    0.080564266846284163,
    0.079074740770195606,
    0.074752090746301264,
    0.068013147274924718,
    0.059486405988859098,
    0.049924704168249963,
    0.040104674753698111,
    0.030729748201279598,
    0.022352296249991150,
    0.015326522879102172,
    0.009797711077828329,
    0.005726606005070864,
    0.002941370083944625,
    0.001204877787865866,
    0.000282970589546489,
    -0.000000000000000001,
]

datanew = [None for x in range(len(data)-len(weightedvals))] #low pass filtered data
tnew = t[0:-(len(weightedvals))]

for i in range(len(data)-len(weightedvals)):
    datanew[i] = np.dot(data[i:i+len(weightedvals)],weightedvals)

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

ax1.plot(tnew,datanew,'r',linewidth='0.75')
ax2.loglog(frq,abs(Y),'r',linewidth='0.75') # plotting the fft
l = len(weightedvals)
ax1.set_title(f'SigD With FIR Filter Weights:{l}, Cutoff:25, Bandwidth:25')

plt.show()

