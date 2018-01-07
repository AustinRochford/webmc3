import numpy as np


def get_values(trace, varname, combine=True, ix_slice=None):
    if ix_slice is None:
        return trace.get_values(varname, combine=combine)
    else:
        chain_values = [
            trace.get_values(varname, chains=chain)[ix_slice]
            for chain in trace.chains
        ]

        if combine:
            return np.concatenate(chain_values)
        else:
            return chain_values


def get_varname_options(trace, include_transformed=False):
    return [
        {
            'label': varname,
            'value': varname
        }
        for varname in get_varnames(
            trace, include_transformed=include_transformed
        )
    ]


def get_varnames(trace, include_transformed=False):
    return [
        varname for varname in trace.varnames
        if not varname.endswith('__') or include_transformed
    ]
