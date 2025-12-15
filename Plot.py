import matplotlib.pyplot as plt
import csv

log1 = open ('Uden_skærm.csv', 'r')
log2 = open ('Med_skræm.csv', 'r')
log3 = open ('Uden_skærm_uden_storlys.csv', 'r')
log4 = open ('Med_skræm_udenStorlys.csv', 'r')


plt.figure(figsize=(10,5))

plt.ylabel("Value")
plt.xlabel("seconds")
#plt.title("med og uden skærm")

x1 = []
y1 = []

for line in log1:
    x1.append(len(x1)/10)
    line = line.strip()
    line = float(line)
    y1.append(line)
log1.close()
plt.plot(x1, y1, marker='o', label='Uden skærm med storlys')

""" 
x3 = []
y3 = []

for line in log3:
    x3.append(len(x3)/10)
    line = line.strip()
    line = float(line)
    y3.append(line)
log3.close()
plt.plot(x3, y3, marker='x', label='Uden skærm uden storlys')



x2 = []
y2 = []

for line in log2:
    x2.append(len(x2)/10)
    line = line.strip()
    line = float(line)
    y2.append(line)
log2.close()
plt.plot(x2, y2, marker='o', label='Med skærm med storlys')



x4 = []
y4 = []

for line in log4:
    x4.append(len(x4)/10)
    line = line.strip()
    line = float(line)
    y4.append(line)
log4.close()
plt.plot(x4, y4, marker='x', label='Med skærm uden storlys')
""" 

#plot a line
lx = [0,8]
ly = [1.5,1.5]

plt.plot(lx, ly, ls = '--')

plt.legend()
plt.show()