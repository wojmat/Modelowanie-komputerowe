import numpy as np
from scipy.stats import chisquare

# Dane z histogramów (załóżmy, że hist_x i hist_y to twoje histogramy)
hist_x = np.loadtxt("histogram_mersenne_twister.csv", delimiter=",")
hist_y = np.loadtxt("histogram_modulo.csv", delimiter=",")

# Liczba wszystkich elementów i kubełków
n = 1000000
bins = 10000

# Obliczanie oczekiwanej liczby wystąpień na kubełek
expected = n / bins

# Test chi-kwadrat dla Mersenne-Twister
chi2_stat_mt, p_val_mt = chisquare(hist_x, [expected] * bins)
print("Mersenne-Twister Chi-square Statistic:", chi2_stat_mt, "P-value:", p_val_mt)

# Test chi-kwadrat dla operacji modulo
chi2_stat_mod, p_val_mod = chisquare(hist_y, [expected] * bins)
print("Modulo Operation Chi-square Statistic:", chi2_stat_mod, "P-value:", p_val_mod)
