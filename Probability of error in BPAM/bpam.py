import numpy as np 
import matplotlib.pyplot as plt 
import math

# Generate the original signal
t = []
xt = np.random.normal(0, 1, 10000)
for i in xt:
    if i > 0.5:
        t.append(i)
    else:
        t.append(0)

s = []
for i in t:
    if i == 0:
        s.append(1)
    else:
        s.append(-1)

# Time axis
x = np.arange(0, len(s), 1)

# Plot the original signal
plt.step(x, s, where='mid')
zero_points = np.where(np.array(s) == 1)
plt.scatter(zero_points, np.ones_like(zero_points), color='red', marker='o', label='s=1')
one_points = np.where(np.array(s) == -1)
plt.scatter(one_points, -np.ones_like(one_points), color='red', marker='o', label='s=-1')
plt.xlim(0, 50)
plt.title("Original Signal")
plt.show()

# Initialize lists to store error probabilities
practical_error = []
theoretical_error = []

# Loop over different SNR values in dB (1 to 10)
for num in range(1, 11):
    # Calculate N0 and sigma (standard deviation of noise)
    N0 = 10 ** (-num / 10)
    sigma = np.sqrt(N0 / 2)

    # Add noise to the signal
    noise = np.random.normal(0, sigma, 10000)
    rt = s + noise  # Received signal

    # Plot the noisy signal
    plt.plot(x, rt)
    plt.xlim(0, 50)
    plt.title(f"Noisy signal with SNR = {num} dB")
    plt.show()

    # Demodulate the received signal
    demodulated = []
    for i in rt:
        if i > 0.4:
            demodulated.append(1)
        else:
            demodulated.append(-1)

    # Plot the demodulated signal
    plt.step(x, demodulated)
    plt.xlim(0, 50)
    plt.title(f"Demodulated signal with SNR = {num} dB")
    plt.show()

    # Calculate the number of errors (compare demodulated signal with original signal)
    error_count = 0
    for i in range(len(rt)):
        if demodulated[i] != s[i]:
            error_count += 1

    # Print the error count for the current SNR
    print(f"SNR = {num} dB, Error count: {error_count}")

    # Calculate practical probability of error
    practical = error_count / len(rt)
    practical_error.append(practical)

    # Calculate theoretical probability of error for PAM
    z = np.sqrt(2 * 0.45/ N0)
    theoretical = (1 / 2) * math.erfc(z / np.sqrt(2))
    theoretical_error.append(theoretical)

# Plot the error probabilities
plt.semilogy(range(1,11), practical_error, label="Practical Probability of Error")
plt.semilogy(range(1,11), theoretical_error, label="Theoretical Probability of Error")
plt.xlabel("SNR in dB")
plt.ylabel("Probability of Error (PAM)")
plt.legend()
plt.show()
