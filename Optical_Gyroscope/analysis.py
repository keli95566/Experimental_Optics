import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot as mp
from scipy import stats



def linear_fit(data,error):
    

    x = np.arange(1,len(data)+1)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,data)
    line = slope*x+intercept
    plt.figure()
    plt.errorbar(x,data, yerr = error,fmt='x')
    plt.plot(x,line)
    #plt.errorbar(x,data,yerr = error)

    plt.title('Linear Fit of Scaling Factor from Data of Frequency Counter')
    plt.ylabel('frequency(Hz)')
    plt.xlabel('Angular velocity: degree/s')
    mp.savefig('./linear_fit_counter_.png')
    print(slope, intercept, r_value, p_value, std_err)

def threshold_velocity_plot():

    angular_velocity = np.array([1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1])
    value = np.array([7,6,5.5,4,3.5,3.5,2.5,0,0,0])
    error = np.array([4,2.5,2,1,1,1,0.5,0,0,0])

    plt.figure()
    plt.errorbar(angular_velocity,value,yerr=error,fmt='x')
    plt.plot(angular_velocity,value)
    plt.title('Threshold Velocity Measurement')
    plt.ylabel('Frequency (kHz)')
    plt.xlabel('Angular Velocity: degree/s')
    mp.savefig('./threshold_velocity_plot.png')

def main():

    threshold_velocity_plot()

    #data_counter = np.array([4.8,12.7,20.1,26.2,32.9,40.7,46,52.5,59.4,66])*(10**3)
    #error_counter = np.array([0.4,0.2,0.1,0.1,0.3,0.3,0.4,0.4,0.8,1])*(10**3)
    #linear_fit(data,error)

main()