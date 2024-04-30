from cProfile import label
import numpy as np
import matplotlib.pylab as plt
from scipy.signal import firwin, lfilter

class AdaptiveFilter():
    def __init__(self, n, mu, w="random"):
        self.w = self.init_weights(w, n)
        self.n = n
        self.w_history = False
        self.mu = mu

    def learning_rule(self, e, x):
        return np.zeros(len(x))

    def init_weights(self, w, n=-1):
        if n == -1:
            n = self.n
        if isinstance(w, str):
            if w == "random":
                w = np.random.normal(0, 0.5, n)
            elif w == "zeros":
                w = np.zeros(n)
            else:
                raise ValueError('Impossible to understand the w')
        elif len(w) == n:
            try:
                w = np.array(w, dtype="float64")
            except:
                raise ValueError('Impossible to understand the w')
        else:
            raise ValueError('Impossible to understand the w')
        return w

    def predict(self, x):
        return np.dot(self.w, x)

    def pretrained_run(self, d, x, ntrain=0.8, epochs=10000):
        Ntrain = int(len(d)*ntrain)
        # train
        for _ in range(epochs):
            self.run(d[:Ntrain], x[:Ntrain])
        # test
        y, e, w = self.run(d[Ntrain:], x[Ntrain:])
        return y, e, w

    def adapt(self, d, x):
        y = self.predict(x)
        e = d - y
        self.w += self.learning_rule(e, x)

    def run(self, d, x):
        # measure the data and check if the dimension agree
        N = len(x)
        if not len(d) == N:
            raise ValueError('The length of vector d and matrix x must agree.')
        self.n = len(x[0])
        # prepare data
        try:
            x = np.array(x)
            d = np.array(d)
        except:
            raise ValueError('Impossible to convert x or d to a numpy array')
        # create empty arrays
        y = np.zeros(N)
        e = np.zeros(N)
        self.w_history = np.zeros((N, self.n))
        # adaptation loop
        for k in range(N):
            self.w_history[k, :] = self.w
            y[k] = self.predict(x[k])
            e[k] = d[k] - y[k]
            self.w += self.learning_rule(e[k], x[k])
        return y, e, self.w_history

class FilterLMS(AdaptiveFilter):
    kind = "LMS"

    def learning_rule(self, e, x):
        return self.mu * x * e

def apply_lowpass_filter(signal, cutoff_freq, sampling_freq, filter_order):
    # calculate filter parameter
    nyquist_freq = 0.5 * sampling_freq
    normalized_cutoff_freq = cutoff_freq / nyquist_freq
    filter_coefficients = firwin(filter_order, normalized_cutoff_freq)

    # apply filter
    filtered_signal = lfilter(filter_coefficients, 1.0, signal)

    return filtered_signal


def main():
    # creation of data
    N = 500
    input_signal = np.random.normal(0, 1, (N, 4)) # input matrix
    v = np.random.normal(0, 0.1, N) # noise
    d = 2*input_signal[:,0] + 0.1*input_signal[:,1] - 4*input_signal[:,2] + 0.5*input_signal[:,3] + v # target
    z = 1*input_signal[:,0] + 1*input_signal[:,1] - 1*input_signal[:,2] - 1*input_signal[:,3]

    # FIR filter
    # apply FIR filter
    cutoff_frequency = 10.0
    sampling_frequency = 100.0
    filter_order = 30
    fir = apply_lowpass_filter(z, cutoff_frequency, sampling_frequency, filter_order)

    # LMS filter
    # identification
    f = FilterLMS(n=4, mu=0.001, w="random")
    y, e, w = f.run(d, input_signal)

    # show results
    plt.figure(figsize=(15,9))
    # plt.subplot(211)
    plt.title("Filters Comparison")
    plt.xlabel("time")
    plt.plot(z,"b", label="input signal")
    plt.plot(y,"g", label="LMS filtered signal")
    plt.plot(fir, "r", label = "FIR filtered signal");plt.legend()
    plt.show()

if __name__ == '__main__':
    main()

