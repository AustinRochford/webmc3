from functools import lru_cache

import numpy as np
import pymc3 as pm

from ..utils import get_values


def autocorr(trace, varname, ix_slice=None, max_lag=100):
    return np.array([
        [
            pm.autocorr(chain_samples, lag)
            for lag in range(1, min(max_lag + 1, chain_samples.size))
        ]
        for chain_samples in get_values(
            trace, varname, combine=False, ix_slice=ix_slice
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
