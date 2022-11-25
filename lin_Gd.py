import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

energy = [43, 49, 60] #keV
picchi = [217, 253, 308]

def retta(x, a, b):
    return a*x + b

init_values = [0,1]
pars, covm = curve_fit(retta, picchi, energy, init_values)

a0, b0 = pars
da, db = np.sqrt(covm.diagonal())
x = np.linspace(picchi[0], picchi[-1], 1000)
print(f'{a0:.3f} +-{da:.3f}')
print(f'{b0:.3f} +- {db:.3f}')
plt.plot(picchi, energy, marker = 'o', linestyle = '')
plt.plot(x, retta(x, a0, b0), color = 'r')

peak = 120.3
y = retta(peak, a0, b0)
dy = np.sqrt((peak*da)**2 + db**2)
print(f'E (canale picco: {peak}) = {y:.3f} +- {dy:.3f}')
plt.show()