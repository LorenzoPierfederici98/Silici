import os
import numpy as np
import matplotlib.pyplot as plt

PATH = 'C:/Users/Lorenzo/Desktop/Lab/Silici/24.11'#percorso dei file .txt
NOME_SPETTRO1 = 'Sign_2V.txt' #modificare con il nome del file
NOME_SPETTRO2 = 'Sign_4V.txt'
NOME_SPETTRO3 = 'Sign_6V.txt'
NOME_SPETTRO4 = 'Sign_8V.txt'
NOME_SPETTRO5 = 'Sign_10V.txt'
NOME_SPETTRO6 = 'Sign_12V.txt'
PATH1 = os.path.join(PATH, NOME_SPETTRO1)
PATH2 = os.path.join(PATH, NOME_SPETTRO2)
PATH3 = os.path.join(PATH, NOME_SPETTRO3)
PATH4 = os.path.join(PATH, NOME_SPETTRO4)
PATH5 = os.path.join(PATH, NOME_SPETTRO5)
PATH6 = os.path.join(PATH, NOME_SPETTRO6)

counts1 = np.loadtxt(PATH1, skiprows=12, max_rows=2048, unpack = True)
counts2 = np.loadtxt(PATH2, skiprows=12, max_rows=2048, unpack = True)
counts3 = np.loadtxt(PATH3, skiprows=12, max_rows=2048, unpack = True)
counts4 = np.loadtxt(PATH4, skiprows=12, max_rows=2048, unpack = True)
counts5 = np.loadtxt(PATH5, skiprows=12, max_rows=2048, unpack = True)
counts6 = np.loadtxt(PATH6, skiprows=12, max_rows=2048, unpack = True) #salta i commenti ed acquisice i conteggi dei canali 0-2047
channels = np.array([i for i in range(0, 2048)], dtype = float) #numero di canali

plt.subplot(2, 3, 1)
plt.plot(channels, counts1, marker = 'o')
plt.title('$V_{bias}$ 2V')
plt.xlabel('Channels')
plt.ylabel('Counts')
plt.subplot(2, 3, 2)

plt.plot(channels, counts2, marker = 'o')
plt.title('$V_{bias}$ 4V')
plt.xlabel('Channels')
plt.ylabel('Counts')

plt.subplot(2, 3, 3)
plt.plot(channels, counts3, marker = 'o')
plt.title('$V_{bias}$ 6V')
plt.xlabel('Channels')
plt.ylabel('Counts')

plt.subplot(2, 3, 4)
plt.plot(channels, counts4, marker = 'o')
plt.title('$V_{bias}$ 8V')
plt.xlabel('Channels')
plt.ylabel('Counts')

plt.subplot(2, 3, 5)
plt.plot(channels, counts5, marker = 'o')
plt.title('$V_{bias}$ 10V')
plt.xlabel('Channels')
plt.ylabel('Counts')

plt.subplot(2, 3, 6)
plt.plot(channels, counts6, marker = 'o')
plt.title('$V_{bias}$ 12V')
plt.xlabel('Channels')
plt.ylabel('Counts')

plt.tight_layout()
plt.show()