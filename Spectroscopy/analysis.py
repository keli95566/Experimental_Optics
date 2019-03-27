import math
import numpy as np 
import glob
from matplotlib import pyplot as mp
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import matplotlib.ticker as ticker
from scipy import stats


def import_files():

    data_dict={}

    for name in glob.glob('./Data/emissions/*.txt'):

        data_file = open(name,'r',encoding='latin-1')
        name = name.rstrip('.txt')
        name = name.lstrip('.//Data//emissions//')
        info = name.split(' ')
        light_source = info[0] + ' ' + info[1]
        spectrum_type = info[2] + ' ' + info[3]
        lines = data_file.readlines()
        intensity_arry,wavelength_arry= get_data(lines)

        data = {}; data['wavelength'] = wavelength_arry;data['intensity'] = intensity_arry
        data['source'] = light_source; data['spectrum'] = spectrum_type
        key = light_source + ' ' + spectrum_type
        data_dict[key] = data

    for name in glob.glob('./Data/dyes/*.txt'):

        data_file = open(name,'r',encoding='latin-1')
        name = name.rstrip('.txt')
        name = name.lstrip('.//Data//dyes//')
        info = name.split(' ')
        light_source = info[0] + ' ' + info[1] + ' ' + info[2]+ ' ' + info[3]
        spectrum_type = 'Absorbnce Spectrum'
        lines = data_file.readlines()
        intensity_arry,wavelength_arry= get_data(lines)
        data = {}; data['wavelength'] = wavelength_arry;data['intensity'] = intensity_arry
        data['source'] = light_source; data['spectrum'] = spectrum_type
        key = light_source + ' ' + spectrum_type
        data_dict[key] = data

    for name in glob.glob('./Data/Task1/*.txt'):

        data_file = open(name,'r',encoding='latin-1')
        name = name.rstrip('.txt')
        name = name.lstrip('.//Data//Task1//')
        info = name.split('_')
        light_source = info[0]
        if info[1] == 'A':
            spectrum_type = 'Absorbance Spectrum'
        elif info[1] == 'T':
            spectrum_type = 'Transmission Spectrum'
        else:
            spectrum_type = info[1]
        lines = data_file.readlines()
        intensity_arry,wavelength_arry= get_data(lines)
        data = {}; data['wavelength'] = wavelength_arry;data['intensity'] = intensity_arry
        data['source'] = light_source; data['spectrum'] = spectrum_type
        key = light_source + ' '+ spectrum_type
        data_dict[key] = data

   #print(data_dict)
    return data_dict

def get_data(lines):
            
    index = 1;intensity_arry  = []; wavelength_arry = []

    for line in lines:

        if index < 18:
            pass
        else:
                    #print(line)
            line = line.rstrip()
            info = line.split('\t')

            try:

                wavelength = info[0].split(',')
                intensity = info[1].split(',')
                wavelength = wavelength[0]+'.'+wavelength[1]
                intensity = intensity[0] + '.' + intensity[1]
                wavelength_arry.append(float(wavelength))
                intensity_arry.append(float(intensity))
                    
            except:

                pass
        index = index + 1

    
    return intensity_arry, wavelength_arry

def plot_all_spectrum(data_dict):

    for key, value in data_dict.items():
        plt.figure()
        x = value['wavelength'];y = value['intensity']; spectrum = value['spectrum']

        
        x, y = cut_lower_bound(380,x,y)


        if spectrum == 'Transmission Spectrum':
            x,y = cut_lower_bound(420,x,y)

        
        else:

            h = (max(y))*(0.6)
            peaks, props = find_peaks(y, height=h,width = 10, prominence=1)
            x_peaks = []; y_peaks = []
            for peak in peaks:
                x_peaks.append(round(x[peak]))
                y_peaks.append(round(y[peak]))
                string = '(' + str(x_peaks) + ' , ' + str(y_peaks) +')'
                plt.text(x[peak]+0.3, y[peak]+0.3, string, fontsize=8)
            plt.plot(x_peaks,y_peaks,'x')
            plt.legend(['peaks', 'signals'])
         
        plt.plot(x,y)
        #plt.semilogy(x,y)

        plt.xlabel('wavelength (nm)')
        plt.ylabel ('intensity (counts)')
        ax = plt.gca()

        ax.xaxis.set_major_locator(ticker.AutoLocator())
        ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
        ax.xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
        
        ax.yaxis.set_major_locator(plt.LinearLocator(4))
        #ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
        ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))

        if spectrum == 'Absorbance Spectrum':
            plt.legend(['peaks', 'signals'])
        fileName = './Result/' + key +'.png'
        plt.title(key);mp.savefig(fileName)
        value['peaks']= [x_peaks,y_peaks]
       # print(x,y)
    return 0

# cut off the noises and put all the spectrums in one graph
def dyes_analysis(data_dict):
    #plt.figure()
    plt.figure(num=None, figsize=(10, 6), dpi=80, facecolor='w', edgecolor='k')
    Maximum = {};reference_wavelength_arry=[];reference_intensity_arry=[];dark_intensity_arry=[];dark_wavelength_arry=[]
    for data_name, data in data_dict.items():
        info = data_name.split(' ')
        if info[1] == 'micro' and info[2] == 'Blue':
            wavelength_arry = data['wavelength']
            intensity_arry = data['intensity']
            
            # find the upper and lower bound to get rid of noises. 
            assert len(wavelength_arry) == len(intensity_arry)
            counter = 0; lower_bound = 0; upper_bound = 0; found_1 = False; found_2 = False
            for element in wavelength_arry:
                if round(element) > 590 and found_1 == False:
                    lower_bound = counter ; found_1 = True
                if round(element) > 670 and found_2 == False:
                    upper_bound = counter; found_2 = True
                counter = counter + 1 
            wavelength = wavelength_arry[lower_bound : upper_bound]
            intensity = intensity_arry[lower_bound : upper_bound]
            assert len(wavelength_arry) == len(intensity_arry)
            Maximum[data_name] = [wavelength[intensity.index(max(intensity))],max(intensity)]
            # find and plot the peaks of the rest of spectrum
            h = (max(intensity))*(0.8)
            peaks, props = find_peaks(intensity, height=h,width = 30)
            x_peaks =[] ; y_peaks = []
            for peak in peaks:
                x_peaks.append(round(wavelength[peak]))
                y_peaks.append(round(intensity[peak]))
                string = '(' + str(x_peaks) + ' , ' + str(y_peaks) +')'
                #plt.text(wavelength[peak]+0.3, intensity[peak]+0.3, string, fontsize=8)
            #plt.plot(x_peaks,y_peaks,'x')
            plt.semilogy(wavelength,intensity, label=info[0]+'uL')

        if info[0] == 'Reference':
            reference_wavelength_arry = data['wavelength']
            reference_intensity_arry = data['intensity']
        if info[0] == 'Dark_Spectrum':
            dark_wavelength_arry = data['wavelength']
            dark_intensity_arry = data['intensity']

    # [maximum wavelength original, max intensity original, ref wavelength, ref intensity, dark wavelength, dark inten]
            
    print(Maximum)

    plt.xlabel('wavelength (nm)')
    plt.ylabel ('log(intensity (counts))')
    ax = plt.gca()

    ax.xaxis.set_major_locator(ticker.AutoLocator())
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    ax.set_aspect('equal')

    ax.yaxis.set_major_locator(plt.LinearLocator(4))
    #ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useMathText=True))
    plt.legend()

            
    fileName = './Result/' + 'blue solution absorbance result' +'.png'
    plt.title('Absorbance Spectrums of Blue Solution of Different Concentration')
    mp.savefig(fileName)
    print(Maximum)

def cut_lower_bound(lower,x,y):
    count = 0
    for wl in x:
        if wl < lower:
            del x[count]; del y[count]
        count = count + 1

    return x,y

def cut_lower_bound(lower, x, y):

    assert len(x) == len(y)
    count = 0; index = 0; found = False
    for wl in x:
        if wl > lower and found == False:
            index = count; found = True
        count = count + 1

    x = x[index:len(x)]; y = y[index:len(y)]
    return x, y

def cut_higer_bound(higher, x,y):

    assert len(x) == len(y)
    count = 0; index = 0; found = False
    for wl in x:
        if wl > higher and found == False:
            index = count; found = True
        count = count + 1

    x = x[0:index]; y = y[0:index]
    return x, y

def absorbance_calculation():

    I_a = np.array([0.857,1.743, 2.156, 2.579, 2.858]) * 1000
    I_0 = np.array([3.763,3.722,3.744,3.722, 3.753]) * 1000
    I_t = I_0 - I_a
    I_d = np.array([250.45,250.36,252.64,250.36,250.70])
    T_1 = (I_t-I_d) /(I_0 - I_d)  ; A_1 = np.log10(1/T_1)
    x = np.array([200,400,600,800,1000])
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,A_1)
    #slope2, intercept2, r_value2, p_value2, std_err2 = stats.linregress(x,A_2)
    line = slope*x+intercept
    #line2 = slope2*x+intercept2


    plt.figure()
    plt.plot(x,A_1,'x', x, line)
    plt.title('Blue Dye Solution Absorbance Linear Fit')
    plt.ylabel('Absorbance (%)')
    plt.xlabel('Amount of Blue Dye added into the solution(mL)')
    mp.savefig('./Result/Blue_Dye_Solution_Absorbance_Linear_Fit.png')
    print(slope, intercept, r_value, p_value, std_err)
    print(A_1)

"""     plt.figure()
    plt.plot(x,A_2,'o', x, line2)
    plt.title('Blue Dye Solution Absorbance Linear Fit')
    plt.ylabel('Absorbance (%)')
    plt.show()
    mp.savefig('./Result/Blue Dye Solution Absorbance Linear Fit2.png')
 """

def unkown_solution():

    data_file = open('./Data/dyes/unkown Blue Solution Halogen A.txt')
    lines = data_file.readlines()
    intensity_arry,wavelength_arry= get_data(lines)
    index = intensity_arry.index(max(intensity_arry))
    print('maximum of intensity: ', max(intensity_arry), 'at wavelength', wavelength_arry[index])
    
   # print(slope2, intercept2, r_value2, p_value2, std_err2)
def get_led_peaks(data_dict):
    
    for key, value in data_dict.items():
        info = key.split(' ')
        if info[1] == 'LED':
            plt.figure()
            x = value['wavelength']; y = value['intensity'];color = info[0]
            plt.plot(x,y);plt.title(key);plt.xlabel('wavelength');plt.ylabel('intensity')
            plt.show()
            
def get_other_peaks(data_dict):
    for key, value in data_dict.items():
        info = key.split(' ')
        if info[0] == 'Smartphone' or info[0] == 'Room':
            plt.figure()
            x = value['wavelength']; y = value['intensity']
            plt.plot(x,y);plt.title(key);plt.xlabel('wavelength');plt.ylabel('intensity')
            plt.show()

def plot_dark_spectrum(data_dict):
    for key, value in data_dict.items():
        info = key.split(' ')
        if info[1] == 'rk':
            plt.figure()
            x = value['wavelength']; y = value['intensity'];color = info[0]
            plt.plot(x,y);plt.title('Dark Spectrum');plt.xlabel('wavelength');plt.ylabel('intensity')
            fileName = './Result/' + key +'.png'
            mp.savefig(fileName)
def main():

    data_dict = import_files()
    plot_dark_spectrum(data_dict)
    #dyes_analysis(data_dict)
    #absorbance_calculation()
    #plot_all_spectrum(data_dict)
    #unkown_solution()
    #get_led_peaks(data_dict)
    #get_other_peaks(data_dict)
main()
