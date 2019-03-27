import matplotlib.pyplot as plt
from matplotlib import pylab
import glob
import math
import numpy as np 
from scipy import stats
from matplotlib import pyplot as mp


def linear_fit(beam_diameters, name):

    p = np.arange(1,len(beam_diameters)+1)
    beam_diameters = (beam_diameters*(10**(-6)))**2
    slope, intercept, r_value, p_value, std_err = stats.linregress(p,beam_diameters)
    line = slope*p+intercept

    plt.plot(p,beam_diameters,'o',p, line)
    pylab.title('Linear Fit of Ring Diameters Relation, 305 Degrees')
    pylab.xlabel('order of rings')
    pylab.ylabel('Dp^2 (m^2)')
    mp.savefig('./'+name+'.png')
    print(slope, intercept, r_value, p_value, std_err)

    return 0
    
def f(x):
    return 1/x

def plot_stability():
  fx_name = r'$f(x)=\frac{1}{x}$'

  xfn=np.setdiff1d(np.linspace(-10,0,100),[0])
  xfp=np.setdiff1d(np.linspace(0,10,100),[0])
  yfn=f(xfn)
  yfp=f(xfp)

  yf = plt.plot(xfn, yfn, label=fx_name)
  plt.plot(xfp, yfp, color=yf[0].get_color())
  plt.legend(loc='upper left')
  plt.show()

def plot_visibility():
   plt.figure()
   IM = np.array([255,255,253,255])
   Im = np.array([93,80,107,88])
   V = (IM - Im)/(IM + Im)
   r = np.arange(1, len(V)+1)
   plt.plot(r, V); plt.xlabel('order of rings'); plt.ylabel('Visibility of the rings'); 
   plt.title('Visibility Relation with the Order of Rings')
   mp.savefig('./Visibility_r.png')

def main():

    # 1 um = 10^-6 m / micro meter 
    # [431.6, 738.4, 1008.8, 1196] um 
    # linear_fit(np.array([57.2, 473.2, 764.4, 988]),'Linear Fit 223 Degrees')
    #plot_stability()
    plot_visibility()
main()