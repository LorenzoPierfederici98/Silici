import logging
import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

"""
======================================================================================================
Fit gaussiano nell'intorno dei picchi, per ricavare media (posizione del canale), deviazione standard,
ampiezza ed offset.
======================================================================================================
"""

PATH = 'C:/Users/Lorenzo/Desktop/Lab/Silici/24.11'  # percorso dei file .txt
NOME_SPETTRO = '60k_Gd180s.txt'  # modificare con il nome del file
PATH = os.path.join(PATH, NOME_SPETTRO)

# salta i commenti ed acquisice i conteggi dei canali 0-2047
counts = np.loadtxt(PATH, skiprows=12, max_rows=2048, unpack=True)
channels = np.array([i for i in range(0, 2048)],
                    dtype=float)  # numero di canali

#capacità 4.4, 6.9, 0.5ns, 11.4, 18.6, 27.1
#peaks = np.array([298.01, 292.19, 293.56, 290.45, 291.33, 293.34])
#FWHM = np.array([13.46, 13.41, 13.63, 13.96, 17.14, 16.09])
#s = FWHM/2.35
#peak = 298
#FWHM = 13.56
#s = FWHM/2.35

peak = 308.
s = 6.5
init_values = [peak, s, 50000., 600.]

#canali vicino al picco, da n a n_max-1
channels1 = np.array([channels[i] for i in range(283, 333)])
counts1 = np.array([counts[i] for i in range(283, 333)])

def gaussiana(x, mu, sigma, A, B):
    """Funzione per fit gaussiano channels-counts. A è l'ampiezza della gaussiana
    B è l'offset."""
    return A*(1/(sigma*np.sqrt(2*np.pi)))*np.exp(-0.5*((x-mu)/sigma)**2) + B


def log_results(channel, mu, dmu, sigma, dsigma, A, dA, B, dB):
    """Inserisce i risultati del fit nel file NOME_SPETTRO_bckg.log.txt ."""
    logging.info(f'Range di canali: {channel[0]}-{channel[-1]}\n')
    logging.info(f'media = {mu:.3f} +- {dmu:.3f}\n')
    logging.info(f'dev. std = {sigma:.3f} +- {dsigma:.3f}\n')
    logging.info(f'A = {A:.3f} +- {dA:.3f}\n')
    logging.info(f'B = {B:.3f} +- {dB:.3f}\n')


def plot_results(channels, counts, mu, sigma, A, B, NOME_SPETTRO):
    """Plotta i risultati del fit nell'intervallo counts1, channels1."""
    plt.plot(channels, gaussiana(channels, mu, sigma, A, B), color='red')
    plt.plot(channels, counts, marker='o')
    NOME_SPETTRO = NOME_SPETTRO.replace('_1.txt', '')
    plt.title('Channels vs counts' + ' ' + NOME_SPETTRO)
    plt.xlabel('Channels')
    plt.ylabel('Counts')
    plt.minorticks_on()
    plt.show()


class Fit_iterator:
    """Iteratore di FitGauss."""

    def __init__(self, classe):
        self.classe = classe
        self.i = 0

    def __next__(self):
        if self.i < len(self.classe.Fit()[0]):
            result = self.classe.Fit()[0][self.i]
            self.i += 1
            return result
        raise StopIteration


class FitGauss:
    """Classe per il fit gaussiano. Prende in input gli array di canali,
    conteggi e valori iniziali e restituisce i parametri ottimali e la matrice
    di correlazione."""

    def __init__(self, x, y, init):
        self.init = init
        self.x = x
        self. y = y
        self.pars = np.array([])
        self.covm = np.array([], [])

    def Fit(self):
        self.pars, self.covm = curve_fit(gaussiana, self.x, self.y, self.init)
        return self.pars, self.covm

    def __iter__(self):
        return Fit_iterator(self)


def risultati(F):
    """"Restituisce i risultati del fit, in ordine: media, sigma, A, B.
    Prende in input la classe per il fit."""
    elem = np.array([])
    iterator = iter(F)
    while True:
        try:
            # Get next element from TeamIterator object using iterator object
            elem = np.append(elem, [next(iterator)])
        except StopIteration:
            break
    return elem


if __name__ == '__main__':

    #mette i risultati del fit nel file NOME_SPETTROlog.txt
    logging.basicConfig(filename=NOME_SPETTRO.replace('txt', '_log.txt'),
    level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    #logging.basicConfig(filename=NOME_SPETTRO.replace('.Spe', '_log.txt'),
    #level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    F = FitGauss(channels1, counts1, init_values)
    risultati = risultati(F)
    mu0 = risultati[0]
    sigma0 = risultati[1]
    A0 = risultati[2]
    B0 = risultati[3]
    dm, dsigma, dA, dB = np.sqrt(F.covm.diagonal())
    #print('C = 8.7 pf\n')
    print(f'Range canali: {channels1[0]}-{channels1[-1]}\n')
    print(f'Canale picco = {mu0:.3f} +- {dm:.3f}\n')
    print(f'sigma = {sigma0:.3f} +- {dsigma:.3f}\n')
    print(f'A = {A0:.3f} +- {dA:.3f}\n')
    print(f'B = {B0:.3f} +- {dB:.3f}\n')
    log_results(channels1, mu0, dm, sigma0, dsigma, A0, dA, B0, dB)
    plot_results(channels1, counts1, mu0, sigma0, A0, B0, NOME_SPETTRO)
