import os
import numpy as np
import matplotlib.pyplot as plt

PATH = 'C:/Users/Lorenzo/Desktop/Lab/Silici/24.11'#percorso dei file .txt
NOME_SPETTRO = '60k_Am180s.txt' #modificare con il nome del file
PATH = os.path.join(PATH, NOME_SPETTRO)

counts = np.loadtxt(PATH, skiprows=12, max_rows=2048, unpack = True) #salta i commenti ed acquisice i conteggi dei canali 0-2047
channels = np.array([i for i in range(0, 2048)], dtype = float) #numero di canali


plt.plot(channels, counts, marker = 'o')
#NOME_SPETTRO = NOME_SPETTRO.replace('.txt', 'eV')
#plt.title('Channels vs counts' + ' ' + NOME_SPETTRO)
plt.xlabel('Channels')
plt.ylabel('Counts')
plt.minorticks_on()
plt.show()