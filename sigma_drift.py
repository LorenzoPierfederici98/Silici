import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#valutazione della componente di drift nel segnale
#da 60keV a 1k di amplificazione

t = np.array([0., 13.]) #tempo in minuti
sigma = np.array([5.83, 5.94])
dsigma = np.array([0.04, 0.04])

def fit_func(x, b):
    return np.sqrt(34. + (b*x)**2)

init_values = [0.]

pars, covm = curve_fit(fit_func, t, sigma, init_values, dsigma)

b0 = pars
db = np.sqrt(covm.diagonal())

#print(f'a = {a0:.3f} +- {da:.3f}\n')
#print(f'b = {b0:.3f} +- {db:.3f}\n')

sigma_drift = b0*t[1]
dsigma_drift = db*t[1]

print('sigma drift = %.3f +- %.3f\n' %(sigma_drift, dsigma_drift))
xx = np.linspace(t[0], t[-1], 100)
plt.errorbar(t, sigma, dsigma, marker = 'o', linestyle = '')
plt.plot(xx, fit_func(xx, *pars), color = 'r')
plt.xlabel('t [min]')
plt.ylabel('sigma [UA]')
plt.show()