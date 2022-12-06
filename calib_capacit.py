import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

C = np.array([4.4, 8.7, 11.4, 21.7])
#sigma = np.array([5.83, 5.79, 6.00, 6.82])
FWHM = np.array([13.46, 13.63, 13.96, 16.09])
sigma = FWHM/2.35
#dsigma = np.array([0.04, 0.05, 0.04, 0.06])
dsigma = np.zeros(len(sigma))
dC = np.array([0.1 for i in range(len(C))])

#sigma in funzione di C; la sigma è la somma in quadratura
# di una componente di rumore elettronico che scala linearmente con la
#capacità e di un termine costante (statistico, drift, etc.)
def fit_func(x, a, b, d):
    return 1/a*np.sqrt(x**2 - d) - b/a

init_values = [0.1, 0., 30.]

pars,covm = curve_fit(fit_func, sigma, C, init_values, dC)

a0, b0, d0 = pars
da, db, dD = np.sqrt(covm.diagonal())

dy = np.sqrt((sigma*dsigma*1/a0*1/(np.sqrt(sigma**2 - d0)))**2 + dC**2)

pars, covm = curve_fit(fit_func, sigma, C, init_values, dy)

a0, b0, d0 = pars
da, db, dD = np.sqrt(covm.diagonal())

chisq = (((C - fit_func(sigma, *pars))/dy)**2).sum()
ndof = len(C) - 3
print(f'a = {a0:.4f} +- {da:.4f}\n')
print(f'b = {b0:.3f} +- {db:.3f}\n')
print(f'd = {d0:.3f} +- {dD:.3f}\n')
print(f'chisq/ndof = {chisq:.3f}/{ndof}\n')

correlation1 = covm[0][1]/(da*db)
correlation2 = covm[0][2]/(da*dD)
correlation3 = covm[1][2]/(db*dD)

sigma_calibration = sigma[1]
dsigma_calibration = 0.


#derivate
delta = abs(sigma_calibration**2 - d0)

dcs = (1/a0)*(1/(np.sqrt(delta)))*sigma_calibration*dsigma_calibration

dca = -(1/(a0**2))*(np.sqrt(delta) - b0)*da

dcd = -(1/(2*a0))*(1/(np.sqrt(delta)))*dD

dcb = -1/a0*db

#dc_calibration = np.sqrt(dcs**2 + dca**2 + dcd**2 + 2*dca*dcd*correlation)
c_calibration = 1/a0*np.sqrt(delta) - b0/a0

dc_calibration = np.sqrt(dcs**2 + dca**2 + dcb**2 + dcd**2 + 2*dca*dcd*correlation2 + 2*dca*dcb*correlation1 + 2*dcb*dcd*correlation3)

print(f'Calibrazione capacita: {c_calibration:.3f} +- {dc_calibration:.3f} pF \n')
plt.errorbar(sigma, C, dC, dsigma, marker = 'o', linestyle = '')
#plt.errorbar(sigma_calibration, 8.7, 0.1, dsigma_calibration, marker = 'o',linestyle = '', label = 'Capacità attesa')
plt.errorbar(sigma_calibration, c_calibration, dc_calibration, dsigma_calibration, marker = 'o', label = 'Capacità dalla calibrazione')
plt.xlabel('$\sigma$ [UA]')
plt.ylabel('Capacità [pF]')
xx = np.linspace(sigma[0], sigma[-1], 100)
plt.plot(xx, fit_func(xx, *pars), color = 'r')
plt.minorticks_on()
plt.legend()
plt.show()