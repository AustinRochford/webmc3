from functools import lru_cache

import numpy as np
import pymc3 as pm


def autocorr(trace, varname, max_lag=100):
    return np.array([
        [pm.autocorr(chain_samples, lag) for lag in range(1, max_lag + 1)]
        for chain_samples in trace.get_values(
            varname, combine=False, squeeze=False
        )
    ])


def effective_n(trace, varname):
    return effective_n_all(trace)[varname]


# adding an LRU cache is a bit of a hack to memorize the effective sample size
# which may be slow to calculate for complex models
@lru_cache(maxsize=1)
def effective_n_all(trace):
    return pm.effective_n(trace)


def gelman_rubin(trace, varname):
    return gelman_rubin_all(trace)[varname]


# adding an LRU cache is a bit of a hack to memorize the Gelman-Rubin
# statistics which may be slow to calculate for complex models
@lru_cache(maxsize=1)
def gelman_rubin_all(trace):
    return pm.gelman_rubin(trace)
