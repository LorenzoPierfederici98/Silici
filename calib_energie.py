import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#Calibrazione energie-canali utilizzando i flitri di Gd62, Mo40, Sn50, Zr40 con emissioni note

energy = np.array([15.7, 17.4, 25.2, 42.7, 48.7, 59.5]) #keV
picchi = np.array([72., 81., 124., 218., 252., 309.]) #il canale a 59.5 keV è stato mediato su tutti i filtri
sigma = np.array([4.0, 4.9, 6., 6.1, 10., 6.5])

def retta(x, a, b):
    return a*x + b

init_values = [1,0]
pars, covm = curve_fit(retta, picchi, energy, init_values, sigma)

a0, b0 = pars
da, db = np.sqrt(covm.diagonal())


chisq = (((energy - retta(picchi, *pars))/sigma)**2).sum()
ndof = len(energy) - 2
print(f'chisq/ndof = {chisq:.3f}/{ndof}\n')
x = np.linspace(picchi[0], picchi[-1], 1000)
print(f'a = {a0:.3f} +- {da:.3f} keV/canale\n')
print(f'b = {b0:.2f} +- {db:.2f} keV\n')


plt.title('Calibrazione energie-canali')
plt.errorbar(picchi[0], energy[0], 0., sigma[0], marker = 'o', linestyle = '', label = f'Zr40 E = {energy[0]} keV')
plt.errorbar(picchi[1], energy[1], 0., sigma[1], marker = 'o', linestyle = '', label = f'Mo42 E = {energy[1]} keV')
plt.errorbar(picchi[2], energy[2], 0., sigma[2], marker = 'o', linestyle = '', label = f'Sn50 E = {energy[2]} keV')
plt.errorbar(picchi[3:6], energy[3:6], np.zeros(len(energy[3:6])), sigma[3:6], marker = 'o', linestyle = '',label = f'Gd64 E = {energy[3]} keV, {energy[4]} keV, {energy[5]} keV')
plt.plot(x, retta(x, a0, b0), color = 'r')
plt.xlabel('Channels [UA]')
plt.ylabel('Energy [keV]')

correlation = covm[0][1]/(da*db)
peak = 126
y = retta(peak, a0, b0)
dy = np.sqrt((peak*da)**2 + db**2 + 2*peak*correlation*da*db)
print(f'E (canale picco: {peak}) = {y:.2f} +- {dy:.2f} keV\n')

plt.legend()
plt.minorticks_on()
plt.show()