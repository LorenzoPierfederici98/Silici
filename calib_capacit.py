import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

C = np.array([4.4, 6.9, 11.4, 21.7]) #capacità in pF
C = [c + 1 for c in C] #tutte le capacità sono in parallelo alla C test di 1 pF
#sigma = np.array([5.83, 5.87, 6.00, 6.82])
FWHM = np.array([13.46, 13.41, 13.96, 16.09])
sigma = FWHM/2.35
#dsigma = np.array([0.04, 0.05, 0.04, 0.06])
dsigma = np.zeros(len(sigma))
dC = np.array([0.1 for i in range(len(C))])

# C in funzione di sigma; la sigma è la somma in quadratura
# di una componente di rumore elettronico che scala linearmente con la
# capacità e di un termine costante (statistico, drift, etc.)
def fit_func(x, a, d):
    return 1/a*np.sqrt(x**2 - d)


init_values = [0.1, 30.]

pars, covm = curve_fit(fit_func, sigma, C, init_values, dC)

a0, d0 = pars
da, dD = np.sqrt(covm.diagonal())

dy = np.sqrt((sigma*dsigma*1/a0*1/(np.sqrt(sigma**2 - d0)))**2 + dC**2)

pars, covm = curve_fit(fit_func, sigma, C, init_values, dy)

a0, d0 = pars
da, dD = np.sqrt(covm.diagonal())

chisq = (((C - fit_func(sigma, *pars))/dy)**2).sum()
ndof = len(C) - 2
print(f'a = {a0:.4f} +- {da:.4f}\n')
print(f'd = {d0:.3f} +- {dD:.3f}\n')
print(f'chisq/ndof = {chisq:.3f}/{ndof}\n')

sigma_calibration = 13.63/2.35
dsigma_calibration = 0.

# derivate
delta = abs(sigma_calibration**2 - d0)

dcs = (1/a0)*(1/(np.sqrt(delta)))*sigma_calibration*dsigma_calibration

dca = -(1/(a0**2))*np.sqrt(delta)*da

dcd = -(1/(2*a0))*(1/(np.sqrt(delta)))*dD

correlation = covm[0][1]/(da*dD)

c_calibration = 1/a0*np.sqrt(delta)

dc_calibration = np.sqrt(dcs**2 + dca**2 + dcd**2 + 2*dca*dcd*correlation)

print(
    f'Calibrazione capacita: {c_calibration:.3f} +- {dc_calibration:.3f} pF \n')
plt.title('Capacità vs $\sigma$ dei picchi del segnale test a 60 keV')
plt.errorbar(sigma, C, dC, dsigma, marker='o', linestyle='')

plt.errorbar(sigma_calibration, c_calibration, dc_calibration, dsigma_calibration, marker='o',
             label=f'C dalla calibrazione {c_calibration:.1f} $\pm$ {dc_calibration:.1f} pF')
plt.errorbar(sigma_calibration, 8.7, 0.1, dsigma_calibration,
             marker='o', label='C attesa $8.7\pm 0.1$ pF')
plt.errorbar(17.14/2.35, 18.6, 0.1, marker='o',
             label='C outlier 18.6 $\pm$ 0.1 pF')
plt.xlabel('$\sigma$ [UA]')
plt.ylabel('Capacità [pF]')
xx = np.linspace(sigma[0] - 1, sigma[-1], 100)
plt.plot(xx, fit_func(xx, *pars), color='r')
plt.minorticks_on()
plt.legend()
plt.show()
