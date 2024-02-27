"""
Numcodecs Codec implementation for Poisson noise calibration
"""
import numpy as np
import numcodecs
from numcodecs.abc import Codec
from numcodecs.compat import ndarray_copy
from . import estimate

### NUMCODECS Codec ###
class Poisson(Codec):
    """Codec for 3-dimensional Delta. The codec assumes that input data are of shape:
    (time, x, y).

    Parameters
    ----------
    zero_level : float
        Signal level when no photons are recorded. 
        This should pre-computed or measured directly on the instrument.
    photon_sensitivity : float
        Conversion scalor to convert the measure signal into absolute photon numbers.
        This should pre-computed or measured directly on the instrument.
    """
    codec_id = "poisson"

    def __init__(self, 
                 zero_level, 
                 photon_sensitivity, 
                 encoded_dtype='int8', 
                 decoded_dtype='int16',
                 ): 
        self.zero_level = zero_level
        self.photon_sensitivity = photon_sensitivity
        self.encoded_dtype = encoded_dtype
        self.decoded_dtype = decoded_dtype

    def encode(self, buf):
        lookup = estimate.make_anscombe_lookup(self.photon_sensitivity)
        encoded = estimate.lookup(buf, lookup)
        return encoded.astype(self.encoded_dtype)

    def decode(self, buf, out=None):
        lookup = estimate.make_anscombe_lookup(self.photon_sensitivity)
        inverse = estimate.make_inverse_lookup(lookup)
        decoded = estimate.lookup(buf, inverse)
        return decoded.astype(self.decoded_dtype)


numcodecs.register_codec(Poisson)