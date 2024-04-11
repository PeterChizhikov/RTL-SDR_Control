from MainProcessor import MainProcessor

if __name__ == "__main__":
    mainProc = MainProcessor()   

    
    # cF = 60e6
    # N = 256*1024
    # Fs = 2.048e6 / 1e6
    # PSD = np.abs(np.fft.fft(samples))**2/(N*Fs)
    # PSD_log = 10.0*np.log10(PSD)
    # PSD_shifted = np.fft.fftshift(PSD_log)

    
    # f = np.arange(Fs/-2.0, Fs/2.0, Fs/N) # start, stop, step
    # f+= cF

    # plt.plot(f, PSD_shifted)
    # plt.xlabel("Frequency [Hz]")
    # plt.ylabel("Magnitude [dB]")
    # plt.grid(True)
    # plt.show()