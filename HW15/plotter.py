# get a line of raw bitmap and plot the components
import serial
ser = serial.Serial('COM7',230400) # the name of your Pico port
print('Opening port: ')
print(ser.name)

ser.write(b'hi\r\n') # send a newline to request data
data_read = ser.read_until(b'\n',50) # read the echo
data_read = ser.read_until(b'\n',50)

print(data_read)

# be sure to close the port
ser.close()