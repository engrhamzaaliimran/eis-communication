import h5py
import matplotlib.pyplot as plt
import numpy as np

# File path
file_path = '/mnt/data/20241210_163650_Charakterisierung IIS Sensor leer und mit MOF.h5'

# Read the data
with h5py.File(file_path, 'r') as h5_file:
    frequency = h5_file['frequency'][:]
    magnitude = h5_file['magnitude'][:]
    phase = h5_file['phase'][:]

# Convert magnitude to dB
magnitude_dB = 20 * np.log10(magnitude)

# Plot Bode Plot
plt.figure(figsize=(12, 6))

# Magnitude plot
plt.subplot(2, 1, 1)
plt.plot(frequency, magnitude_dB, label='Magnitude (dB)', linewidth=1.5)
plt.title('Bode Plot')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.grid(True, which='both', linestyle='--')
plt.legend()

# Phase plot
plt.subplot(2, 1, 2)
plt.plot(frequency, phase, label='Phase (degrees)', linewidth=1.5, color='orange')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase (degrees)')
plt.grid(True, which='both', linestyle='--')
plt.legend()

plt.tight_layout()
plt.show()

# Plot Nyquist Plot
real_part = magnitude * np.cos(np.radians(phase))
imag_part = magnitude * np.sin(np.radians(phase))

plt.figure(figsize=(6, 6))
plt.plot(real_part, -imag_part, label='Nyquist Plot', linewidth=1.5)
plt.title('Nyquist Plot')
plt.xlabel('Real Part (Ω)')
plt.ylabel('Imaginary Part (Ω)')
plt.grid(True)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.legend()
plt.show()
