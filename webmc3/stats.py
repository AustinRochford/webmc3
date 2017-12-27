import numpy as np
import pymc3 as pm


def autocorr(trace, varname, max_lag=100):
    return np.array([
        [pm.autocorr(chain_samples, lag) for lag in range(1, max_lag + 1)]
        for chain_samples in trace.get_values(varname, combine=False)
    ])
