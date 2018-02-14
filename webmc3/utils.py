from math import ceil, floor
from scipy.signal import fftconvolve

def get_ix_slice(relayoutData):
    if relayoutData is None:
        return None
    else:
        try:
            return slice(
                floor(relayoutData['xaxis.range[0]']),
                ceil(relayoutData['xaxis.range[1]'])
            )
        except KeyError:
            return None


def autocorr(x):
    """
    Compute autocorrelation using FFT for every lag for the input array
    https://en.wikipedia.org/wiki/Autocorrelation#Efficient_computation

    Parameters
    ----------
    x : Numpy array
        An array containing MCMC samples

    Returns
    -------
    acorr: Numpy array same size as the input array
    """
    if x.ndim > 1:
        xshape = x.shape
        x2 = x.reshape(xshape[0], -1)
        acorr = np.array([autocorr(x) for x in x2.T])
        return acorr.T.reshape(xshape)
    else:
        y = x - x.mean()
        n = len(y)
        result = fftconvolve(y, y[::-1])
        acorr = result[len(result) // 2:]
        # acorr /= np.arange(n, 0, -1)
        acorr /= acorr[0]
        return acorr
