import numpy as np

e = 1.6e-19 #carica elettrone in coulomb
w = 3.6 #energia in eV per creare coppie di portatori
E = 4e4 #energia incidente in eV
C = 1e-12 #capacità test in farad
Q = (E/w)*e #carica dei portatori
V = Q/C #potenziale sulla capacità test in entrata al pre-ampl.

print(f'V = {1000*V:.3f} mV')

#il generatore invia un potenziale di tot V, voglio attenuare per avere
#un segnale in mV da mandare al pre-ampl.

'''
V_out = V
V_in =  #V in uscita dal generatore
attenuazione = 20*np.log(V_out/V_in)

print(f'attenuazione = {attenuazione:.3f} dB')
'''