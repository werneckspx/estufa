import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import TransferFunction, bode
from sympy import symbols, sin, simplify
from sympy.integrals.transforms import laplace_transform
from scipy.signal import detrend

x = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190,
              200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370,
              380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550,
              560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710, 720, 730,
              740, 750, 760, 770, 780, 790, 800, 810, 820, 830, 840, 850, 860, 870, 880, 890, 900, 910,
              920, 930, 940, 950, 960, 970, 980, 990, 1000, 1010, 1020, 1030, 1040, 1050, 1060, 1070,
              1080, 1090])

y = np.array([28, 29, 29, 29, 30, 30, 30, 30, 31, 30, 31, 31, 31, 31, 31, 31, 31, 31, 30, 31, 31, 32,
              32, 31, 31, 31, 31, 30, 30, 30, 31, 30, 29, 28, 28, 27, 27, 27, 27, 26, 26, 26, 26, 26,
              25, 25, 25, 25, 23, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
              22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 21, 22, 21, 21, 21, 21,
              21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21])

def sinusoidal(x, A, B, C, D):
    return A * np.sin(B * x + C) + D

A_est = (np.max(y) - np.min(y)) / 2
D_est = np.mean(y)
B_est = 2 * np.pi / (np.max(x) - np.min(x))
C_est = 0

initial_guess = [A_est, B_est, C_est, D_est]


params, params_covariance = curve_fit(sinusoidal, x, y, p0=initial_guess)

A, B, C, D = params
print(f'Amplitude A: {A}, Frequência B: {B}, Fase C: {C}, Deslocamento D: {D}')


plt.title('Ajuste Senoidal dos Dados')
plt.scatter(x, y, label='Dados')
plt.plot(x, sinusoidal(x, *params), label='Ajuste Senoidal', color='red')
plt.xlabel('Tempo (min)')
plt.ylabel('Temperatura')
plt.show()

t, s, a = symbols('t s a')
f = A * sin(B * t + C) + D

F_s, _, _ = laplace_transform(f, t, s)
F_s = simplify(F_s)
print(F_s)

num, den = F_s.as_numer_denom()

num_coeffs = [float(coef) for coef in num.as_poly(s).all_coeffs()]
den_coeffs = [float(coef) for coef in den.as_poly(s).all_coeffs()]

system = TransferFunction(num_coeffs, den_coeffs)

w, mag, phase = bode(system)

y_detrended = detrend(y)

window = np.hanning(len(y_detrended))
y_windowed = y_detrended * window


y_fft = np.fft.fft(y_windowed)
freqs = np.fft.fftfreq(len(y_fft), d=600)


idx = np.where(freqs >= 0)
freqs = freqs[idx]
y_fft = y_fft[idx]

fig, ax = plt.subplots(figsize=(10, 5))

ax.semilogx(w, mag)
ax.set_title('Diagrama de Bode - Magnitude')
ax.set_ylabel('Magnitude (dB)')
ax.grid()

plt.tight_layout()
plt.show()

print(" ")

plt.figure(figsize=(12, 6))
plt.plot(freqs, np.abs(y_fft))
plt.xlabel('Frequência (Hz)')
plt.ylabel('Magnitude')
plt.title('Espectro de Frequência da Temperatura')
plt.grid(True)
plt.show()
