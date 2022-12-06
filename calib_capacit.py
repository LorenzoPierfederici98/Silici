import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#Fit sull'andamento fra capacità e larghezza
#dei picchi dovuta al rumore; calibrazione della capacità
#per il cavetto a 0.5 ns che collega il rivelatore al 
#pre amplificatore

C = np.array([4.4, 6.9, 11.4, 21.7])
#sigma = np.array([5.83, 5.87, 6.00, 6.82])
FWHM = np.array([13.46, 13.41, 13.96, 16.09])
sigma = FWHM/2.35
#dsigma = np.array([0.04, 0.05, 0.04, 0.06])
dsigma = np.zeros(len(sigma))
dC = np.array([0.1 for i in range(len(C))])

#sigma in funzione di C; la sigma è la somma in quadratura
# di una componente di rumore elettronico che scala linearmente con la
#capacità e di un termine costante (statistico, drift, etc.)
def fit_func(x, a, d):
    return 1/a*np.sqrt(x**2 - d)
    
init_values = [0.1, 30.]

pars,covm = curve_fit(fit_func, sigma, C, init_values, dC)

a0, d0 = pars
da, dD = np.sqrt(covm.diagonal())

dy = np.sqrt((sigma*dsigma*1/a0*1/(np.sqrt(sigma**2 - d0)))**2 + dC**2)

pars, covm = curve_fit(fit_func, sigma, C, init_values, dy)

a0, d0 = pars
da, dD = np.sqrt(covm.diagonal())

chisq = (((C - fit_func(sigma, *pars))/dy)**2).sum()
ndof = len(C) - 2
print(f'a = {a0:.4f} +- {da:.4f}\n')
#print(f'b = {b1:.3f} +- {db1:.3f}\n')
print(f'd = {d0:.3f} +- {dD:.3f}\n')
print(f'chisq/ndof = {chisq:.3f}/{ndof}\n')
correlation = covm[0][1]/(da*dD)

sigma_calibration = 5.79
dsigma_calibration = 0.05

c_calibration = fit_func(sigma_calibration, *pars)

#derivate
dcs = (1/a0)*(1/(np.sqrt(sigma_calibration**2 - d0)))*sigma_calibration*dsigma_calibration

dca = -(1/(a0**2))*np.sqrt(sigma_calibration**2 - d0)*da

dcd = -(1/2*a0)*(1/(np.sqrt(sigma_calibration**2 - d0)))*dD

dc_calibration = np.sqrt(dcs**2 + dca**2 + dcd**2 + 2*dca*dcd*correlation)

print(f'Calibrazione capacità: {c_calibration:.3f} +- {dc_calibration:.3f}\n')
plt.errorbar(sigma, C, dC, dsigma, marker = 'o', linestyle = '')
plt.errorbar(sigma_calibration, c_calibration, dc_calibration, dsigma_calibration, marker = 'o', label = 'Calibrazione capacità')
plt.xlabel('$\sigma$ [UA]')
plt.ylabel('Capacità [pF]')
xx = np.linspace(0, sigma[-1], 100)
plt.plot(xx, fit_func(xx, *pars), color = 'r')
plt.minorticks_on()
plt.legend()
plt.show()