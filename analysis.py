import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot as mp
from scipy import stats



def linear_fit():
    # YAG LASER DATA
# Laser Resonator Data    
  #  x = np.array([250,300,350,400,450,500,550,560])*(0.001)
  #  y = np.array([0,0.468,1.1,1.68,2.36,2.7,3.26,3.36])
  #  error = np.array([0,0.1,0.1,0.1,0.2,0.2,0.2,0.2])


# Active Q Swiching, Pump rate and Pulse Energy Data

  #  y = np.array([364,330,285,215,130]) 
  #  x = np.array([550,525,500,475,450])
  #  error = np.array([10,10,10,10,10])


# Passive Q Switching, num of peaks and frequency
#x = np.array([427,399,375,349,324,300,290,275,250])
#    y = np.array([10,11,11,12,13,14,15,16,17])
#    error = np.array([0,0,0,0,0,0,0,0,0])

# Temperature vs Max Voltage Output 
   # x = np.arange(15,36,1)
   # y = np.array([17,14.8,13.6,11.6,640,560,544,576,576,520,496,392,352,228,232,285,520,800,1030,1360,1220])
   # error = np.array([2,2,2,2,40,40,40,40,20,20,20,40,40,40,20,20,40,100,40,200,100])
   
   # x = np.array([0,40,80,120,160,200,240,280,320,360,400,440,480,520,560])
   # y = np.array([0,0,0,0,0,0,0,0,0,1.4,3.8,10,18.6,40,72])
   # error = np.array([0,0,0,0,0,0,0,0,0,1,2,2,1,2,2])
   

   #HE NE LASER DATA
    #x = np.array([12,13,14,15,16,17])
    #y = np.array([8.65,8.85,9,9,8.95,8.83])
    #error_x = np.full((6),0.5); error_y = np.full((6),0.05)
    #print(error_x, error_y)
    #print(len(x),len(y),len(error))
   # x = np.arange(250,500,50)
    
    #Relation Between Laser Output Power and Current Supply

   # x = np.arange(5,6.6,0.1)
    #y_1 = np.array([3.96,4,4.04,4.08,4.13,4.15,4.16,4.17,4.18,4.19,4.21,4.23,4.25,4.25,4.24,4.25])
   # y_2 = np.array([3.96,4.01,4.05,4.08,4.12,4.15,4.16,4.20,4.21,4.23,4.21,4.23,4.24,4.24,4.25,4.25])
   # y_1 = np.array([7.06,7.13,7.19,7.24,7.29,7.34,7.36,7.40,7.44,7.46,7.48,7.51,7.52,7.54,7.56,7.56])
   # y_2 = np.array([7.07,7.13,7.18,7.24,7.28,7.32,7.38,7.42,7.45,7.43,7.45,7.47,7.49,7.50,7.51,7.50])
   # error = np.full(len(x),0.01)
    #print(len(y_1),len(y_2),len(x))
    
    # Relation Between Resonance Length and the Output Voltage Power
   # x = np.arange(50,86,2)
   # y_1 = np.array([5.6,5.6,5.67,6.00,5.78,6.41,6.73,6.9,7.05,7.45,8.12,8.1,8.06,8.02,8.06,8.15,8.26,8.28])
  #  error = np.full(len(x),0.05)
    
    # Same, but for R = 700 mm
   # x = np.arange(50,66,1)
   # y_1 = np.array([7.57,7.75,7.55,7.56,7.63,7.41,6.88,6.22,6.16,6.18,6.03,5.62,4.9,3.72,2.22,0.88])
   # error = np.full(len(x),0.03)
  

  # Optical Tweezers
  # Critical Velocity and Trapping force, 85% solution 
    eta = 0.022; r = 2 # um
    #x_1 = np.array([3.25,7.65,12.15,17.90,23.05]) # Critical Velocity , um/s
    #y_1 = 6*x_1*eta*r*np.pi
    #error_x = np.full(len(x_1),0.05)
    #error = y_1*(error_x/x_1)
    #x_1 = np.array([10.915,15.015,19.1,23.16]) # Efficient power
    #y_1 = np.array([4.05,5.6,6.9,8.3])

# 64 % Solution
  
    #x_1 = np.array([17.86,13.94,9.89,6.13,2.7])# Power f , mW
    #x_1 = x_1*0.5
    #y_1 = np.array([23.05,17.9,12.15,7.65,3.25]) # Critical velocity, um/s
    #error = np.full(len(x_1),0.05)
    
    
 # Adaptive Optics Analysis
    # Aberration compensation in a microscope using a deformable mirror
   
    x_1= np.array([1,3,4,5])  # number of slides
    x_2 = np.array([1,2,3,4,5])
    y_1 = np.array([0.729,0.339,0.159,0.109])           # Strehl without compensation
    y_2 = np.array([0.939,0.872,0.823,0.659,0.337])       # Strehl ratio with compensation
    error_1 = np.full(len(x_1),0.01)
    error_2 = np.full(len(x_2),0.01)
    slope_1, intercept_1, r_value_1, p_value_1, std_err_1 = stats.linregress(x_1,y_1)
    line_1 = slope_1*x_1+intercept_1
    slope_2, intercept_2, r_value_2, p_value_2, std_err_2 = stats.linregress(x_2,y_2)
    line_2 = slope_2*x_2+intercept_2
    
    plt.figure()
    #plt.plot(x,y,'x')
    plt.errorbar(x_1,y_1, yerr = error_1,fmt='x',label='Without Compensation Scatter')
    plt.plot(x_1,line_1,label = 'Without Compensation')
    plt.errorbar(x_2,y_2,yerr = error_2,fmt = 'x',label = 'With Compensation Scatter')
    plt.plot(x_2,line_2,label = 'With Compensation')
    plt.title('Number of Slides vs. Strehl Ratio')
    plt.xlabel('Number of Slides')
    plt.ylabel('Strehl Ratio')
    plt.legend(loc = 0)
    mp.savefig('strehl_slides.png')
    
    # calculate the standard errors of slope and intercept.
    mx = x_1.mean()
    sx2 = ((x_1-mx)**2).sum()
    sd_intercept_1 = std_err_1 * np.sqrt(1./len(x_1) + mx*mx/sx2)
    sd_slope_1 = std_err_1 * np.sqrt(1./sx2)
    
    sd_intercept_2 = std_err_2 * np.sqrt(1./len(x_2) + mx*mx/sx2)
    sd_slope_2 = std_err_1 * np.sqrt(1./sx2)
    # Measurement of threshold
   # calculate the stand error of the threshold of x and threshold x
   # t_x = (-intercept)/slope
   # t_x_err = (-intercept/(slope**2))*sd_slope + ((-1)/slope)*sd_intercept
   #  print("threshold of x is:",t_x,"error is:",t_x_err)

    print('Linear Fit Result: ')
    print('The slope is: %f, the intercept is: %f, R value is: %f, p value is: %f, standard error is: %f' % (slope_1,intercept_1,r_value_1,p_value_1,std_err_1))
    print('The slope is: %f, the intercept is: %f, R value is: %f, p value is: %f, standard error is: %f' % (slope_2,intercept_2,r_value_2,p_value_2,std_err_2))
   
    print("standard error intercept:",sd_intercept_1, "standard error slope:", sd_slope_1 )
    print("standard error intercept:",sd_intercept_2, "standard error slope:", sd_slope_2 )



def scatter():
    
    plt.figure()
   # x = np.array([0,20,40,60,70,80,90,100,120,140,160,180,200,250,280,320,360,400,440,480,530,580,620])
   # y = np.array([0,0,0,0,36.8,120,176,200,250,220,192,196,216,148,240,300,340,376,360,360,378,368,216])
   # error_y = np.array([0,0,0,0,4,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10])
    x = np.array([0,40,80,120,160,200,240,280,320,360,400,440,480,520,560])
    y = np.array([0,0,0,0,0,0,0,0,0,1.4,3.8,10,18.6,40,72])
    error = np.array([0,0,0,0,0,0,0,0,0,1,2,2,1,2,2])

    plt.errorbar(x,y,yerr= error, fmt= 'x')
    plt.title('Linear Fit of Injection Current vs. SHG output')
    plt.ylabel('Maximum of SHG Output(mV)')
    plt.xlabel('Injection Current (mA)')
    mp.savefig('SHG_Current.png')

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

    linear_fit()
    #scatter()
main()
