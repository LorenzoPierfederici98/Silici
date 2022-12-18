import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

PATH = 'C:/Users/Lorenzo/Desktop/Lab/Silici/24.11'#percorso dei file .txt
#spettro con filtro di 120um di Gd
NOME_SPETTRO_GD = '60k_Gd180s.txt' #modificare con il nome del file
PATH_GD = os.path.join(PATH, NOME_SPETTRO_GD)

#spettro non filtrato
NOME_SPETTRO_AM = '60k_Am180s.txt'
PATH_AM = os.path.join(PATH, NOME_SPETTRO_AM)

counts_GD = np.loadtxt(PATH_GD, skiprows=12, max_rows=2048, unpack = True) #salta i commenti ed acquisice i conteggi dei canali 0-2047
channels = np.array([i for i in range(0, 2048)], dtype = float) #numero di canali

counts_AM = np.loadtxt(PATH_AM, skiprows=12, max_rows=2048, unpack = True)
#canali vicino al picco, da n a n_max-1
channels1 = np.array([channels[i] for i in range(283, 333)])
counts1 = np.array([counts_GD[i] for i in range(283, 333)])

def esponenziale(x, a, mu):
    return a*np.exp(-mu*x)

media = 308.
sigma = 6.6

r_GD = 7.95 #densità gadolinio g/cm^3
t_GD = (120e-4)*r_GD #spessore massico Gd in g/cm^2
mu_GD = 11.75 #mu del Gd a 60 keV in cm^2/g

sigma_step = 2 #di quante sigma mi sposto dal picco
#area totale a sigma_step sigma dal picco
gross_area_GD = counts_GD[int(media - sigma_step*sigma):int(media + sigma_step*sigma)].sum()
var_GD = gross_area_GD #varianza dell'area
gross_area_AM = counts_AM[int(media - sigma_step*sigma):int(media + sigma_step*sigma)].sum()
var_AM = gross_area_AM

area_attesa = esponenziale(t_GD, gross_area_AM, mu_GD)
sigma_area_attesa = (esponenziale(t_GD, gross_area_AM, mu_GD)/gross_area_AM)*np.sqrt(var_AM)

print(f'Attenuazione dell\'area a {sigma_step} sigma dal picco a 60 keV\n')
print(f'Area spettro non filtrato: {gross_area_AM} +- {np.sqrt(var_AM):.0f}\n')
print(f'Area con spessore di 120um di Gd: {gross_area_GD} +- {np.sqrt(var_GD):.0f}\n')
print(f'Area attesa dall\'attenuazione a 60 keV: {area_attesa:.0f} +- {sigma_area_attesa:.0f}\n')