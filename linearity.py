import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#Calibrazione con i segnali test per simulare segnali dalla sorgente
#di energie 27-30-40-50-60 keV

V_meas, Channel, FWHM = np.loadtxt('energie.txt', usecols = (2, 4, 5), unpack = True)

#per le incertezze sulle misure di potenziali si sommano in quadratura
#il 3% del valore misurato con 0.05*numero di divisioni
dV = 0.05*np.array([4., 4., 5., 6., 6.]) #numeri delle divisioni per ogni misura
dV = np.sqrt((3/100 * V_meas)**2 + dV**2)

sigma = FWHM/2.35

def retta(x, a, b):
    return a*x + b

init_values = [1., 0.]
pars, covm = curve_fit(retta, Channel, V_meas, init_values, dV)

a0, b0 = pars
da, db = np.sqrt(covm.diagonal())

dy = np.sqrt((a0*sigma)**2  + dV**2)
pars1, covm1 = curve_fit(retta, Channel, V_meas, init_values, dy)

a1, b1 = pars1
da1, db1 = np.sqrt(covm.diagonal())

chisq = (((V_meas - retta(Channel, *pars1))/dy)**2).sum()
ndof = len(V_meas) - 2
print(f'a = {a1:.4f} +- {da1:.4f} mV/canale')
print(f'b = {b1:.3f} +- {db1:.3f} mV')
print(f'chisq/ndof = {chisq:.3f}/{ndof}')

correlation = covm1[0][1]/(da1*db1)
peak = 18
volt_calibration = a1*peak + b1  #voltaggio ottenuto dalla calibrazione
dvolt_calibration = np.sqrt(
    covm1[0][0]*peak**2 + covm1[1][1] + 2*peak*correlation*da1*db1)

e = 1.6e-19 #carica elettrone in coulomb
w = 3.6 #energia in eV per creare coppie di portatori
C = 1e-12 #capacità test in farad

#calibrazione dell'energia in keV dal voltaggio ottenuto 
ener_calibration = volt_calibration * C * w/e * 1e-6
dener_calibration = dvolt_calibration * C * w/e * 1e-6

plt.title('Calibrazione dei segnali test')
plt.xlabel('Canali')
plt.ylabel('Potenziali misurati [mV]')
xx = np.linspace(Channel[0], Channel[-1], 100)
plt.plot(xx, retta(xx, *pars), color = 'red')
plt.errorbar(Channel, V_meas, dV, sigma, marker = 'o', linestyle = '')
print(f'calibrazione energia (al canale {peak}): {ener_calibration:.2f} +- {dener_calibration:.2f} keV\n')
plt.minorticks_on()
plt.show()