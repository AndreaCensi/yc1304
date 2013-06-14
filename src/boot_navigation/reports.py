from .navigation_map import NavigationMap
from .plots import plot_arrow_SE2, plot_arrow_se2
from contracts import contract
from geometry import se2_from_linear_angular
from reprep import Report, rgb_zoom, scale
import numpy as np
import warnings

__all__ = ['display_nmap']


@contract(report=Report, nmap=NavigationMap)
def display_nmap(report, nmap):
    
    with report.subsection('sensing') as sub:
        display_nmap_sensing(sub, nmap)
        
    f = report.figure()        
    with f.plot('map') as pylab:
        for bd, pose in nmap.data:
            commands = bd['commands']
            warnings.warn('redo this properly')
            if len(commands) == 3:
                x, y, omega = commands
            else:
                x, y = commands
                omega = 0
            vel = se2_from_linear_angular([x, y], omega)
            plot_arrow_SE2(pylab, pose)
            plot_arrow_se2(pylab, pose, vel, length=0.04, color='g')
        pylab.axis('equal')
        

@contract(report=Report, nmap=NavigationMap)
def display_nmap_sensing(report, nmap):
    obss = list(nmap.get_all_observations())
    map1 = np.vstack(obss)
    
    nreps = 4
    nspaces = 1
    obss2 = []
    for o in obss:
        for _ in range(nreps):
            obss2.append(o)
        for _ in range(nspaces):
            obss2.append(o * np.nan)
    map2 = np.vstack(obss2)
    

    f = report.figure(cols=1)
    f.data_rgb('observations', _nmapobs_to_rgb(map1))
    f.data_rgb('observations2', _nmapobs_to_rgb(map2))
    
    
def _nmapobs_to_rgb(m):
    print m.shape
    m = m.T
    rgb = scale(m, min_value=0, max_value=1, nan_color=[.6, 1, .6])
    return rgb_zoom(rgb, 4)
    
@contract(obss='list(array)')
def _nmapobslist_to_rgb(obss):
    map2 = np.vstack(obss)
    return _nmapobs_to_rgb(map2)
    
    
    
