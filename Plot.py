import matplotlib.pyplot as plt
import csv

# mm = med skærm med storlys
# mu = med skærm uden storlys

log1 = open ('sensor_test_output_mm.csv', 'r')
log2 = open ('sensor_test_output_mu.csv', 'r')

# um = uden skærm med storlys
# uu = uden skærm uden storlys

log3 = open ('sensor_test_output_um.csv', 'r')
log4 = open ('sensor_test_output_uu.csv', 'r')


plt.figure(figsize=(10,5))

plt.ylabel("Value")
plt.xlabel("Samples")
plt.title("med og uden skærm")

x1 = []
y1 = []

for line in log1:
    x1.append(len(x1))
    line = line.strip()
    line = float(line)
    y1.append((line/65535)*3.3)  # Convert to voltage
log1.close()
plt.plot(x1, y1, marker='o', label='Med skærm med storlys')

x2 = []
y2 = []

for line in log2:
    x2.append(len(x2))
    line = line.strip()
    line = float(line)
    y2.append((line/65535)*3.3)  # Convert to voltage
log2.close()
plt.plot(x2, y2, marker='o', label='Med skærm uden storlys')



x3 = []
y3 = []

for line in log3:
    x3.append(len(x3))
    line = line.strip()
    line = float(line)
    y3.append((line/65535)*3.3)  # Convert to voltage
log3.close()
plt.plot(x3, y3, marker='x', label='Uden skærm med storlys')

x4 = []
y4 = []

for line in log4:
    x4.append(len(x4))
    line = line.strip()
    line = float(line)
    y4.append((line/65535)*3.3)  # Convert to voltage
log4.close()
plt.plot(x4, y4, marker='x', label='Uden skærm uden storlys')


#plot a line
lx = [0,2400]
ly = [1.7,1.7]

plt.plot(lx, ly, ls = '--')

plt.legend()
plt.show()