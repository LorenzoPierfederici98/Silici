import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

energy = np.array([17.4, 19.6, 59.5]) #keV
picchi = np.array([81., 113., 308.])
sigma = np.array([5.9, 5., 6.71])

def retta(x, a, b):
    return a*x + b

init_values = [0,1]
pars, covm = curve_fit(retta, picchi, energy, init_values, sigma)

a0, b0 = pars
da, db = np.sqrt(covm.diagonal())


chisq = (((energy - retta(picchi, *pars))/sigma)**2).sum()
ndof = len(energy) - 2
print(f'chisq/ndof = {chisq:.3f}/{ndof}\n')
x = np.linspace(picchi[0], picchi[-1], 1000)
print(f'a = {a0:.3f} +-{da:.3f} keV/canale\n')
print(f'b = {b0:.3f} +- {db:.3f} keV\n')

plt.title('Calibrazione energia con filtro di Mo')
plt.errorbar(picchi, energy, np.zeros(len(energy)), sigma, marker = 'o', linestyle = '')
plt.plot(x, retta(x, a0, b0), color = 'r')
plt.xlabel('Channels [UA]')
plt.ylabel('Energy [keV]')

correlation = covm[0][1]/(da*db)
peak = 126
y = retta(peak, a0, b0)
dy = np.sqrt((peak*da)**2 + db**2 + 2*peak*correlation*da*db)
print(f'E (canale picco: {peak}) = {y:.3f} +- {dy:.3f} keV\n')
plt.show()