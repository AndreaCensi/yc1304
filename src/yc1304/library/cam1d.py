from contracts import contract

from bootstrapping_olympics import (RepresentationNuisance,
     NuisanceNotInvertible)
import numpy as np
from streamels import check_streamels_range, make_streamels_1D_float, check_streamels_2D


__all__ = ['VertAverage', 'VertAverageFraction']


class VertAverage(RepresentationNuisance):

    def transform_streamels(self, streamels):
        check_streamels_2D(streamels)
        check_streamels_range(streamels, 0, 1)
        
        _, W = streamels.shape  
        streamels2 = make_streamels_1D_float(nstreamels=W, lower=0, upper=1)
        return streamels2
    
    def transform_value(self, values):
        return np.mean(values, axis=0)

    def inverse(self):
        raise NuisanceNotInvertible()


class VertAverageFraction(RepresentationNuisance):
    """ Only averages a strip around the middle line """
    
    @contract(fraction='float,>0,<1')
    def __init__(self, fraction):
        self.fraction = fraction
        
    def transform_streamels(self, streamels):
        check_streamels_2D(streamels)
        check_streamels_range(streamels, 0, 1)
        
        _, W = streamels.shape  
        streamels2 = make_streamels_1D_float(nstreamels=W, lower=0, upper=1)
        return streamels2
    
    def transform_value(self, values):
        H, _ = values.shape
        
        n = int(H * self.fraction)
        middle = H / 2
        low = middle - n / 2
        high = middle + n / 2
        
        values = values[low:high, :]
    
        return np.mean(values, axis=0)

    def inverse(self):
        raise NuisanceNotInvertible()
