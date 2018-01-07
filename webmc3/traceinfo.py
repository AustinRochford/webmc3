import numpy as np
import pymc3 as pm


class TraceInfo:
    def __init__(self, trace):
        self._trace = trace
        self.nchains = trace.nchains
        
        if trace.nchains > 1:
            self.effective_n = pm.effective_n(trace)
            self.gelman_rubin = pm.gelman_rubin(trace)

    def __len__(self):
        return len(self._trace)

    def autocorr(self, varname, ix_slice=None, max_lag=100):
        return np.array([
            [
                pm.autocorr(chain_samples, lag)
                for lag in range(1, min(max_lag + 1, chain_samples.size))
            ]
            for chain_samples in self.get_values(
                varname, combine=False, ix_slice=ix_slice
            )
        ])

    def get_values(self, varname, combine=True, ix_slice=None):
        if ix_slice is None:
            return self._trace.get_values(varname, combine=combine)
        else:
            chain_values = [
                self._trace.get_values(varname, chains=chain)[ix_slice]
                for chain in self._trace.chains
            ]

            if combine:
                return np.concatenate(chain_values)
            else:
                return chain_values

    def get_varnames(self, include_transformed=False):
        return [
            varname for varname in self._trace.varnames
            if not varname.endswith('__') or include_transformed
        ]
