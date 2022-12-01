print('Loading modules')
import stellarnet_driver3 as sn
import datetime, json
dt = datetime
import matplotlib.pyplot as plt
from gpiozero import PWMOutputDevice as PWM
from gpiozero import Button as gpioButton
from gpiozero import OutputDevice
from gpiozero import RGBLED
from tkinter import (Tk, Frame, Button, Entry, Label, Message, StringVar)
# import matplotlib
# matplotlib.use('TkAgg')
import numpy as np
import pandas as pd
from time import sleep
  
print('...done loading modules')


################################################# FUNCTIONS

# FUNCTION THAT READS PARAMETERS
# def readPars(aFN):
    # aFL=open(aFN,'r')                       # OPEN FILE, READ ONLY
    # iPars=aFL.readlines()                   # READ ALL LINES IN THE FILE
    # aFL.close()                             # CLOSE FILE
    # print(len(iPars),'parameters found')
    # parDict={} # 
    # for p in iPars:                         # ...FOR EVERY LINE
        # p=p.strip()                         # ...STRIP OUT SPACES
        # #print(p,len(p))
        # if p=='' or p[0]=='#' or len(p)==0: # IGNORE COMMENTS, OR BLANK LINES
            # pass
        # else:
            # parDict[p.split('=')[0]]=p.split('=')[1]    # SPLIT THE PARAMETER BY THE '=' SIGN, STORES PARAMS IN DICTIONARY
    # print(parDict)
    # return(parDict)                         # RETURN DICTIONARY TO CALLING FUNCTION

# We need to keep this or add in a different way to save the power spectrum as a csv file
## can change csv file saving to pandas##
def writeCSV(iWVL,iSPEC,oFN):
    oFL=open(oFN,'w')
    oFL.write('WVL,INT\n')
    aItems=len(iWVL)
    for i in range(aItems):
        oStr=','.join([str(x) for x in [iWVL[i],iSPEC[i]]])
        oFL.write(oStr+'\n')
    oFL.close()

#function to get spectrum
def getSpectrum(spectrometer, wav):
    spectrum = sn.array_spectrum(spectrometer, wav)
    return spectrum
#function to set parameters
def setparam(spectrometer, wav, inttime, xtiming, scansavg, smooth):

    spectrometer['device'].set_config(
        int_time=inttime,
        x_timing=xtiming,
        scans_to_avg=scansavg,
        x_smooth=smooth)
    
spectrometer,wav = sn.array_get_spec(0)

##UNKNOWN VARIABLES NEED TO BE SET##
#red_pin = ?
#green_pin = ?
#blue_pin = ?
red_led_pin = 2
green_led_pin = 3
check_ref_sleep = 1000
ref_checks_lim = 4
## found from descriptive statistics on past references
allow_ref_min_intensity = 1780*(1-0.16)
allow_ref_max_intensity = 63000*(1+0.09)
allow_ref_avg_intensity = 27700
percent_diff_ref_mean = 0.19
allow_ref_std_intensity = 13800
percent_diff_ref_std = 0.18


# global scansavg
# global smooth
# global xtiming

scansavg = 1
smooth = 1
xtiming = 1


#global PMWfreq
#global delay_ms


PMWfreq = 50

# Variables to be used in spectroscopy functions
# global intTime
# global delay_ms

intTime = 1
delay_ms = 8.8

ref_col = False


def analyze_ref():

    # Variables to be used in function and elsewhere
    global power_spec_ref
    global wavelengths_ref
    global wavelengths
    global ref_col
    
    sample_name = 'ref'
    datetime_an = datetime.datetime.now().isoformat()
    
    # Collect spectrum

    # LIGHT SOURCE FREQUENCY SHOULD BE BETWEEN 10 AND 80 HZ!
    lightSource = PWM(lamp_pin,initial_value=0,frequency=PMWfreq)  # Activate light source
#     highIntensity = True
#     # To make sure integration time is not too high
#     while highIntensity == True:
#         print('Intensity too high. Lowering integration time to')
#         intTime=0.9*intTime
#         spec.integration_time_micros(intTime)   # SET INTEGRATION TIME
#         print(intTime)
#         lightSource.value = 0.1 
#         power_spec=spec.intensities(correct_nonlinearity=True)        # CONDUCT NONLINEARITY AND DARK CORRECTIONS
#         lightSource.value = 0
#         if max(power_spec)<16500:
#             highIntensity = False
    ## start of spectrum collection##
    setparam(spectrometer, wav, intTime, xtiming, scansavg, smooth)
    #setparam(spectrometer, wav, intTime)
    
    sleep(0.01)
    #data = getSpectrum(spectrometer, wav) # collect power spectrum
    lightSource.value = 0.1 # turn on light source
    sleep(delay_ms/1000)
    data = getSpectrum(spectrometer, wav) # collect power spectrum
    lightSource.value = 0 # turn off light source
    power_spec = data[36:,1] # intensities
    wavelengths=data[36:,0] # wavelengths
    
    intTimeStr=str(intTime)    
    power_spec_ref = power_spec
    wavelengths_ref = wavelengths
    ##end of spectrum collection##
    # Write spectrum to csv and json files
    #oSpecFN=('spec_'+sample_name+"_"+meas_ang+'_'+
             #intTimeStr+'_'+parDict['locCode']+'_'+datetime_an+'.json') # CREATE OUTPUT JSON FILE FOR SPECTRA
             
     #check that reference is valid        
    ref_checks = 0
    while ref_checks < ref_checks_lim:
        ref_checks+=1
        if (min(power_spec_ref) < allow_ref_min_intensity) or (max(power_spec_ref) > allow_ref_max_intensity) or (np.mean(power_spec_ref)-allow_ref_avg_intensity)/allow_ref_avg_intensity>percent_diff_ref_mean or (np.std(power_spec_ref)-allow_ref_std_intensity)/allow_ref_std_intensity>0.18: ##SET ALLOW_MIN_INTENSITY and ALLOW_MAX_INTENSITY
            ##add average and standard deviation to be similar (within certain percentage)##
            ##find reference spectrum on raspberry pi##
            sleep(check_ref_sleep)
            setparam(spectrometer, wav, intTime, xtiming, scansavg, smooth)
            #setparam(spectrometer, wav, intTime)
            
            sleep(0.01)
            #data = getSpectrum(spectrometer, wav) # collect power spectrum
            lightSource.value = 0.1 # turn on light source
            sleep(delay_ms/1000)
            data = getSpectrum(spectrometer, wav) # collect power spectrum
            lightSource.value = 0 # turn off light source
            power_spec = data[36:,1] # intensities
            wavelengths=data[36:,0] # wavelengths
            
            intTimeStr=str(intTime)    
            power_spec_ref = power_spec
            wavelengths_ref = wavelengths      
            ref_err = 1
        else:
            ref_err = 0
            break
    if ref_err == 1:
        system_status.set('Error: reference invalid')
        
    oSpecFN=('spec_'+sample_name+"_"+
             intTimeStr+'_'+datetime_an+'.json') # CREATE OUTPUT JSON FILE FOR SPECTRA
    oSpecFNcsv=oSpecFN.replace('.json','.csv')
    oSpecFL=open(specDir+oSpecFN,'w')
    print(oSpecFN)
#     dSpec={'locCode':parDict['locCode'],'wavelengths':wavelengths.tolist(),'power_spec':power_spec.tolist()}  # GET SPECTRA FROM SPECTROMETER
    dSpec={'wavelengths':wavelengths.tolist(),'power_spec':power_spec.tolist()}  # GET SPECTRA FROM SPECTROMETER
    json.dump(dSpec,oSpecFL)                          # SAVE IN JSON FILE
    oSpecFL.close()                                         # WRITE JSON FILE
    writeCSV(wavelengths,power_spec,specDir+oSpecFNcsv)
        
    # Plot reference spectrum
    plt.figure(num=1,clear=True)
    plt.title('Power Spectrum')
    plt.plot(wavelengths,power_spec, label = 'reference')
    plt.xlabel('wavelength (nm)')
    plt.ylabel('intensity (counts)')
    plt.legend(loc='upper right')
    #plt.ylim([0,16000])
    plt.show(block=False)
    print('Reference collected.')
    ref_col = True

def analyze_sample_abs():

    if ref_col == False:
        print('Need reference.')
        return
    
    sample_name = sample_name_entry.get()
    datetime_an = datetime.datetime.now().isoformat()
    date_an = datetime_an.split('T')[0]
    time_an = datetime_an.split('T')[1]
    
    # Collect spectrum

    # LIGHT SOURCE FREQUENCY SHOULD BE BETWEEN 10 AND 80 HZ!
    lightSource = PWM(lamp_pin,initial_value=0,frequency=PMWfreq)  # Activate light source
#     highIntensity = True
#     # To make sure integration time is not too high
#     while highIntensity == True:
#         print('Intensity too high. Lowering integration time to')
#         intTime=0.9*intTime
#         spec.integration_time_micros(intTime)   # SET INTEGRATION TIME
#         print(intTime)
#         lightSource.value = 0.1 
#         power_spec=spec.intensities(correct_nonlinearity=True)        # CONDUCT NONLINEARITY AND DARK CORRECTIONS
#         lightSource.value = 0
#         if max(power_spec)<16500:
#             highIntensity = False
    setparam(spectrometer, wav, intTime, xtiming, scansavg, smooth)
    #setparam(spectrometer, wav, intTime)
    
    sleep(0.01)
    #data = getSpectrum(spectrometer, wav) # collect power spectrum
    lightSource.value = 0.1 # turn on light source
    sleep(delay_ms/1000)
    data = getSpectrum(spectrometer, wav) # collect power spectrum
    lightSource.value = 0 # turn off light source
    power_spec = data[36:,1] # intensities
    wavelengths=data[36:,0] # wavelengths
    
    intTimeStr = str(intTime)

    # Compare to reference
    if max(power_spec)/max(power_spec_ref)<0.9 or max(power_spec)/max(power_spec_ref)>1.1:
        print('WARNING:Reference and sample may not be compatible!')

    # Write spectrum to csv and json
    
#     oSpecFN=('spec_'+sample_name+"_"+filtered+'_'+date_col+'_'+meas_ang+'_'+
#              intTimeStr+'_'+parDict['locCode']+'_'+datetime_an+'.json') # CREATE OUTPUT JSON FILE FOR SPECTRA
    oSpecFN=('spec_'+sample_name+"_"+
             intTimeStr+'_'+datetime_an+'.json') # CREATE OUTPUT JSON FILE FOR SPECTRA
    oSpecFNcsv=oSpecFN.replace('.json','.csv')
    oSpecFL=open(specDir+oSpecFN,'w')
    print(oSpecFN)
#     dSpec={'locCode':parDict['locCode'],'wavelengths':wavelengths.tolist(),'power_spec':power_spec.tolist()}  # GET SPECTRA FROM SPECTROMETER
    dSpec={'wavelengths':wavelengths.tolist(),'power_spec':power_spec.tolist()}  # GET SPECTRA FROM SPECTROMETER
    json.dump(dSpec,oSpecFL)                          # SAVE IN JSON FILE
    oSpecFL.close()                                         # WRITE JSON FILE
    writeCSV(wavelengths,power_spec,specDir+oSpecFNcsv)
        
    # Plot the sample and reference spectra
    plt.figure(num=1,clear=True)
    plt.title('Power Spectrum')
    plt.plot(wavelengths,power_spec, label = 'sample')
    plt.plot(wavelengths,power_spec_ref, label = 'reference')
    plt.xlabel('wavelength (nm)')
    plt.ylabel('intensity (counts)')
    plt.legend(loc='upper right')
    #plt.ylim([0,16000])
    plt.show(block=False)
    print('Sample analyzed.')
    
    # Calculate absorbance
    # ref_spec = np.fromstring(power_spec_ref)
    # sam_spec = np.fromstring(power_spec)

    # absorbance = np.log10(ref_spec/sam_spec)
    
    absorbance = np.log10(power_spec_ref/power_spec)
    
    # Plot absorbance spectrum
    plt.figure(num=2,clear=True)
    plt.title('Absorbance Spectrum')
    plt.plot(wavelengths,absorbance,label = sample_name)
    plt.xlabel('wavelength (nm)')
    plt.ylabel('absorbance')
    plt.legend(loc='upper right')
    plt.show(block=False)
    print('Absorbance calculated')
    
    new_row = [sample_name,filtered,date_col,date_an,time_an,intTime,meas_ang]
    new_row.extend(absorbance)
    row_df = pd.DataFrame(data = [new_row])
    row_df.to_csv(absDir+'abs_df.csv',mode = 'a',header=False,index=False)
    print('Absorbance recorded')

######################################################
## Code for autoanalysis loops
    
#GPIO variables

# global valve_pin 
# global loop_switch_pin 
# global pump_fwd_pin
# global pump_rev_pin
# global lamp_pin

valve_pin = int(17)
loop_switch_pin = int(22)
pump_fwd_pin = int(24)
pump_rev_pin = int(23)
lamp_pin = int(26)

# global loop_switch
loop_switch = gpioButton(loop_switch_pin)
pump_fwd = OutputDevice(pump_fwd_pin)
pump_rev = OutputDevice(pump_rev_pin)
valve = OutputDevice(valve_pin)

# global timestep
# global system_status

sample_timestep = dt.timedelta(minutes=5) # interval between sample analysis events
flush_timestep = dt.timedelta(minutes=1) # interval between flushes
#clean_timestep = dt.timedelta(minutes=5) #might not need this if cleaning is based on sample count
system_status = 'Loop is off.'

# global samples_per_rinse
# global flow_velocity
samples_per_rinse = 12
pump_flowrate = 200 #mL/min
tubing_ID = 3/16*2.54 #cm
cuvette_volume = 3 # mL
tubing_area = 3.14159/4*tubing_ID**2 #cm^2
flow_velocity = pump_flowrate/tubing_area #cm/min
flow_velocity = flow_velocity/2.54/12/60 #ft/s
flush_on_time = 3*cuvette_volume/pump_flowrate*60 #seconds

# Initial values of some variables

#loop_num = 0 # for determining how many loops occured since the program was turned on. May not be necessary or useful
loop_is_ON = False # for turning program on and off with virtual button
begin_time = dt.datetime.now() # for program timing
sample_loop_time = 0 # for determining the time since the last sample
flush_loop_time = 0 # for determining the time since the last flush
#clean_loop_time = 0 # might not need this if cleaning is based on sample count
sample_num = 12 # this is for cleaning/taking reference after every x number of samples


def loop_OFF():
    #global loop_num
    power_led = LED(green_led_pin)
    power_led.on()
    global loop_is_ON
    global loop_off_time
    global system_status
    #global current_loop_time
    #loop_num = 0
    loop_is_ON = False
    loop_off_time = dt.datetime.now()
    #current_loop_time = 0
    system_status.set(f'Loop OFF since {loop_off_time}.')
    

def loop_ON():
    program_led = LED(red_led_pin)
    program_led.on()
    global loop_is_ON
    #global sample_loop_time
    #global loop_num
    global loop_on_time
    global system_status
    #loop_num = 0 
    loop_is_ON = True
    #sample_loop_time = 0
    loop_on_time = dt.datetime.now()
    system_status.set(f'Loop ON since {loop_on_time}')
    
def pump_forward():
    
    pump_rev.off()
    pump_fwd.on()
    
def pump_reverse():
    
    pump_fwd.off()
    pump_rev.on()
    
def pump_off():
    
    pump_rev.off()
    pump_fwd.off()
    
def flowpath_sam:
    
    valve.on()
    
def flowpath_ref:
    
    valve.off()    
    

def analysis_loop():
    
    #global loop_num
    #global sample_timestep
    global sample_loop_time
    global begin_time
    global system_status
    global flush_loop_time
    
    tube_lengths = tube_len_entry.get()
    tube_lengths = tube_lengths.split(sep=',')
    tube_lengths = list(map(float,tube_lengths))
    
    sample_tube_length = sum(tube_lengths[0,1]) #total length of sample flow path (ft)
    ref_tube_length = sum(tube_lengths[2,3])
    
    sample_time = sample_tube_length/flow_velocity*1.5 # in seconds
    ref_time = ref_tube_length/flow_velocity*1.5
    
    if loop_is_ON and loop_switch.is_pressed:

        if sample_loop_time > sample_timestep.seconds:
            #loop_num += 1
            
            sample_loop_time = 0 # reset sample clock
            sample_num += 1 # count samples for determining when to clean
            flush_loop_time = 0 # reset flush clock
            led = RGBLED(red_pin, green_pin, blue_pin)
            led.color = (0, 0, 1)
            flowpath_sam() #turn on sample flow path
            pump_reverse() # turn pump on in reverse to clear the sample line
            sleep(sample_time) # let pump run for enough time to clear line
            pump_forward() # turn pump on to bring sample in
            sleep(sample_time) # let pump run for enought time to fill the lines with new sample
            pump_off()
            analyze_sample_abs() # collect absorbance data
            system_status.set(f'Sample analyzed at {dt.datetime.now()}')
            led.color = (0, 0, 0)
            
        if flush_loop_time > flush_timestep.seconds:
            
            flush_loop_time = 0 # reset flush clock
            
            flowpath_sam() # set sample flow path
            pump_forward() # pump sample in
            sleep(flush_on_time) # let pump run for short period of time
            pump_off() # turn pump off
            system_status.set(f'System flushed at {dt.datetime.now()}')
            
        if sample_num >= samples_per_rinse:
            
            sample_num = 0
            led = RGBLED(red_pin, green_pin, blue_pin)
            led.color = (1, 1, 0)
            flowpath_sam() # set sample flow path for clearing lines
            pump_reverse() # run pump in reverse for clearing lines
            sleep(sample_time) # run pump long enough for clearing lines
            pump_off()
            flowpath_ref() # set reference flow path for bringing in cleaning/reference solution
            pump_forward() # run pump forward for bringing in cleaning/reference solution
            sleep(ref_time) # wait for lines to fill
            pump_off() # turn pump off
            analyze_ref() # collect reference spectrum
            # may need to do some kind of test to check that the reference is good. If it's not, it should be redone.
            pump_reverse() # run pump in reverse to clear lines
            sleep(ref_time) # wait for lines to empty
            pump_off() # turn pump off
            flowpath_sam() # set sample flow path (needed for safety/contamination?)
            system_status.set(f'Reference collected at {dt.datetime.now()}')
            led.color = (0, 0, 0)
    
    if loop_is_ON==False:
        system_status.set(f'Loop off for {current_loop_time} seconds.')
    
    end_time = dt.datetime.now()
    time_diff = end_time - begin_time
    sample_loop_time += time_diff.seconds
    flush_loop_time += time_diff.seconds
    begin_time = dt.datetime.now()
    
    root.after(1000,analysis_loop)

    
    
    
    
################################################# DEFAULTS

parFile='/home/water-gator/GSBT/specPars_v2.txt'  # LOCATION OF PARAMETER FILE
specDir='/home/water-gator/GSBT/spectra/SN/'      # LOCATION WHERE RAW SPECTRA ARE SAVED
absDir='/home/water-gator/GSBT/abs/SN/'      # LOCATION WHERE ABSORBANCE SPECTRA ARE SAVED
#refDir = '/home/water-gator/GSBT/spects/SN/' # can we add another folder for the references? #  #LOCATION FOR REFERENCE SPECTRA#


############################### Read parameters

#print('Reading parameters')
#parDict=readPars(parFile)

##### Making the GUI

root = Tk()
root.geometry("400x450")
root.title('GatorSpec - Auto')
 
frame = Frame(root)
frame.pack()

sample_name_lab = Label(frame,text ='Sample Name')
sample_name_lab.pack(padx = 2, pady = 2)
 
sample_name_entry = Entry(frame, width = 20)
sample_name_entry.insert(0,'test')
sample_name_entry.pack(padx = 5, pady = 5)

tube_len_lab = Label(frame,text ='Tube Length (ft)')
tube_len_lab.pack(padx = 2, pady = 2)
 
tube_len_entry = Entry(frame, width = 20)
tube_len_entry.insert(0,'S1,S2,C1,C2')
tube_len_entry.pack(padx = 5, pady = 5)
 
ref_Button = Button(frame, text = "Collect Reference", command = analyze_ref)
ref_Button.pack(padx = 5, pady = 5)

sample_Button = Button(frame, text = "Analyze Sample", command = analyze_sample_abs)
sample_Button.pack(padx = 5, pady = 5)

loop_ON_Button = Button(frame, text = "Loop ON", command = loop_ON)
loop_ON_Button.pack(padx = 5, pady = 5)

loop_OFF_Button = Button(frame, text = "Loop OFF", command = loop_OFF)
loop_OFF_Button.pack(padx = 5, pady = 5)

flowpath_1_Button = Button(frame, text = "Sample Flow Path", command = flowpath_sam)
flowpath_1_Button.pack(padx = 5, pady = 5)

flowpath_2_Button = Button(frame, text = "Reference Flow Path", command = flowpath_ref)
flowpath_2_Button.pack(padx = 5, pady = 5)

pump_forward_Button = Button(frame, text = "Pump Forward", command = pump_forward)
pump_forward_Button.pack(padx = 5, pady = 5)

pump_reverse_Button = Button(frame, text = "Pump Reverse", command = pump_reverse)
pump_reverse_Button.pack(padx = 5, pady = 5)

pump_stop_Button = Button(frame, text = "Stop Pump", command = pump_off)
pump_stop_Button.pack(padx = 5, pady = 5)

system_status = StringVar(value = system_status)
system_status_msg = Message(frame,textvariable =system_status)
system_status_msg.pack(padx = 2, pady = 2)

root.after(1000,analysis_loop)
 
root.mainloop()


