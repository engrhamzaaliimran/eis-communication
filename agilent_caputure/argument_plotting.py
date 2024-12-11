import sys
import numpy as np
import matplotlib.pyplot as plt
import h5py

# Function to load data from the HDF5 file
def load_impedance_data(file_path):
    """
    Load impedance data from an HDF5 file.
    
    Parameters:
        file_path (str): Path to the HDF5 file.
    
    Returns:
        tuple: Frequency, magnitude, and phase arrays.
    """
    with h5py.File(file_path, 'r') as h5_file:
        frequency = np.array(h5_file['frequency'])
        magnitude = np.array(h5_file['magnitude'])
        phase = np.array(h5_file['phase'])
    return frequency, magnitude, phase

# Function to plot Bode and Nyquist plots for a specific sweep
def plot_sweep_data(sweep_number, frequency, magnitude, phase):
    """
    Plot Bode and Nyquist plots for a given sweep number.
    
    Parameters:
        sweep_number (int): Sweep index to plot (0-based).
        frequency (np.ndarray): Frequency data array.
        magnitude (np.ndarray): Magnitude data array.
        phase (np.ndarray): Phase data array.
    """
    if sweep_number < 0 or sweep_number >= frequency.shape[0]:
        print("Invalid sweep number! Please choose a valid sweep.")
        return

    # Extract data for the selected sweep
    freq = frequency[sweep_number]
    mag = magnitude[sweep_number]
    phs = phase[sweep_number]

    # Convert magnitude and phase to real and imaginary parts for Nyquist plot
    real = mag * np.cos(np.radians(phs))
    imag = mag * np.sin(np.radians(phs))

    # Bode plot: Magnitude vs Frequency
    plt.figure()
    plt.loglog(freq, mag)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (Ohms)')
    plt.title(f'Sweep {sweep_number+1}: Bode Plot (Magnitude)')
    plt.grid(True, which='both', linestyle='--')
    plt.show()

    # Bode plot: Phase vs Frequency
    plt.figure()
    plt.semilogx(freq, phs)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Phase (Degrees)')
    plt.title(f'Sweep {sweep_number+1}: Bode Plot (Phase)')
    plt.grid(True, which='both', linestyle='--')
    plt.show()

    # Nyquist plot: Imaginary vs Real Impedance
    plt.figure()
    plt.plot(real, imag, label='Impedance')
    plt.xlabel('Real Part (Ohms)')
    plt.ylabel('Imaginary Part (Ohms)')
    plt.title(f'Sweep {sweep_number+1}: Nyquist Plot')
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.axvline(0, color='black', linewidth=0.8, linestyle='--')
    plt.grid(True, which='both', linestyle='--')
    plt.legend()
    plt.show()

# Main function to run the plotter for a specific sweep
def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <file_path> <sweep_number>")
        sys.exit(1)

    file_path = sys.argv[1]
    try:
        sweep_number = int(sys.argv[2])
    except ValueError:
        print("Error: Sweep number must be an integer.")
        sys.exit(1)

    # Load data and validate sweep number
    frequency, magnitude, phase = load_impedance_data(file_path)
    num_sweeps = frequency.shape[0]

    if 1 <= sweep_number <= num_sweeps:
        plot_sweep_data(sweep_number - 1, frequency, magnitude, phase)
    else:
        print(f"Invalid sweep number! Please choose a number between 1 and {num_sweeps}.")

# Entry point
if __name__ == "__main__":
    main()