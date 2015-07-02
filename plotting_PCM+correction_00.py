# coding: utf-8

#import numerical python module
import numpy as np
#import matlab style plotting module
import matplotlib.pyplot as plt
#import sys module : for sys.stdin
import sys


# local variables
energy_singlets = []
energy_triplets = []
wavelength_singlets = []
wavelength_triplets = []
osc_str_singlets = []
osc_str_triplets = []
input_list = []
read_in = []
ISC_TRIPLETS = []
plot_abs = False
Lowest_Lying_Singlet = 100.00
Lowest_Absorbing_Singlet = 100.00
Lowest_Lying_Triplet = 100.00
Sing_shift = 0.0
Trip_shift = 0.0
deltaE = 0.5
Emin_Singlets=0.0
Emax_Singlets=0.0
Emin_Triplets=0.0 
Emax_Triplets=0.0

# read input file containing plot title and filenames and for each line read parse input line and store filenames in argument[*] array and execute the big loop
read_in = sys.stdin 
for line in read_in:
    arguments=line.split()
    if arguments[0]=="EOF": # poor programming: I know an use the fact that there are 6 arguments below
       print 'leaving'
       break

# clear lists and local variables, initialize variables for each iteration
    plot_abs = False
    del energy_singlets[:]
    del energy_triplets[:]
    del wavelength_singlets[:]
    del wavelength_triplets[:]
    del osc_str_singlets[:]
    del osc_str_triplets[:]
    del input_list[:]
    del ISC_TRIPLETS[:]

# assign elements of arguments to local variables
    title                 = arguments[0]
    singlets_X_filename   = arguments[1]
    triplets_X_filename   = arguments[2]
    singlets_SCF_filename = arguments[3]
    triplets_SCF_filename = arguments[4]
    singlet_corr_filename    = arguments[5] 
    triplet_corr_filename    = arguments[6] 

# open above files with assigned handles
    file_singlets = open(singlets_X_filename,'r')
    file_triplets = open(triplets_X_filename,'r')
    file_singlets_scf = open(singlets_SCF_filename,'r')
    file_triplets_scf = open(triplets_SCF_filename,'r')
    file_sing_shift   = open(singlet_corr_filename,'r')
    file_trip_shift   = open(triplet_corr_filename,'r')

# get the number of lines
    num_lines_singlets = sum(1 for line in open(singlets_X_filename))
    num_lines_triplets = sum(1 for line in open(triplets_X_filename))

#   read scf energies and any corrections
    singlet_scf_energy = float(file_singlets_scf.readline())
    sing_shift = float(file_sing_shift.readline()) 
    triplet_scf_energy = float(file_triplets_scf.readline())
#    trip_shift = float(file_trip_shift.readline()) 
    trip_shift = 0.0

# compute the corrected lowest lying triplet energy
    t1_energy=27.211*(triplet_scf_energy - singlet_scf_energy) + float(trip_shift) # all triplet energies are based off of T1_energy and so from here all contain the correction

# loop over singlets correcting singlet and triplet energies: working on singlet and triplet data! this works because there the same number of states for each. poor programming as this would fail for unequal numbers of singlet and triplet states
    for index in range(0,num_lines_singlets):
        readfile_singlets = file_singlets.readline()
        readfile_triplets = file_triplets.readline()
        line_singlets = readfile_singlets.split()
        line_triplets = readfile_triplets.split()
        energy_singlets.append(round((sing_shift + float(line_singlets[0])),2))# corrected - OK
        energy_triplets.append(round((float(line_triplets[0])  + t1_energy),2)) #corrected - OK
        wavelength_singlets.append(round(1240.0 / (sing_shift + 1240.0/float(line_singlets[1]) ),2))#corrected - OK
        wavelength_triplets.append(round(1240.0 / (t1_energy  + 1240.0/float(line_triplets[1]) ),2))#corrected - OK
        osc_str_singlets.append(float(line_singlets[2].strip( 'f=' )))
        osc_str_triplets.append(float(line_triplets[2].strip( 'f=' ))) 
        # OK all data should be corrected from here on out

# get min and max energies for singlets and triplets
    Emin_Singlets = min(energy_singlets)
    Emax_Singlets = max(energy_singlets)
    Emin_Triplets = min(energy_triplets)
    Emax_Triplets = max(energy_triplets)

# set global min (0) and global max energies
    emin=0.0
    emax = max(Emax_Singlets,Emax_Triplets)


##########################################################
# Plot Singlet Energy Levels: plot infor for lowest lying singlet state and lowest absorbint singlet (if different than lowest lying singlet)
##########################################################
    #set up plotting parameters - energy levels drawn as lines between x0 and x1
    # arrays Xposition and Yposition hold values for each excited state
    x0=0
    x1=3
    Yposition = [] # will hold energy values
    Xposition = [] # look unecessary...
    deltaY = 0.1   # threshold - plots lines within threshold

    # make a figure with title
    energy_figure = plt.figure()
    energy_figure.suptitle(title)

    # add axis labels
    energy_plot = energy_figure.add_subplot(111)
    energy_plot.set_ylabel('ev')
    energy_plot.axes.get_xaxis().set_visible(False)

    # plot ground singlet state at zero eV
    energy_plot.plot((x0,x1),(0.0,0.0),color='black') 

    # loop over singlet states: plot lines at singlet energies
    for index in range(len(energy_singlets)): 
        energy_plot.plot((x0,x1),(energy_singlets[index],energy_singlets[index]),color='black')
        Xposition.append(x1) # looks unecessary
        Yposition.append(energy_singlets[index])

        # label the lowest excited singlet
        if index == 0:
            Lowest_Lying_Singlet = energy_singlets[index]
            energy_plot.text(x0-2.0,Yposition[index],(energy_singlets[index],wavelength_singlets[index]),fontsize=10)

        #label the lowest lying absorbing singlet
        if osc_str_singlets[index]>0.0:
              if plot_abs == False:
                  energy_plot.text(x0-2.0,Yposition[index],(energy_singlets[index],wavelength_singlets[index]),fontsize=10)
                  energy_plot.annotate('pump',xy=(x0+0.2,Yposition[index]),xytext=(x0+0.2,0.0),arrowprops=dict(facecolor='red'), color='red',fontsize='20')
                  if Lowest_Lying_Singlet != Yposition[index]:
                   energy_plot.annotate('IC',xy=(float((x1-x0)/2.0),Lowest_Lying_Singlet),xytext=(float((x1-x0)/2.0),Yposition[index]),arrowprops=dict(facecolor='green'), color='green',fontsize='20')
                  plot_abs=True
                  Lowest_Absorbing_Singlet = energy_singlets[index]

##########################################################
# Plot Triplet Energy Levels: plot info for lowest lying triplet state and triplet states within threshold  
# TODO: this should be re-written so that the lowest triplet state and the nearest triplet state are labeled
##########################################################
    #set up plotting parameters - energy levels drawn as lines between x0 and x1
    # arrays Xposition and Yposition hold values for each excited state
    x2=4
    x3=7
    Yposition = [] # triplet energy - same array as for singlet energies. poor programming
    Xposition = [] # looks unecessary...
    deltay = 0.1

######label lowest lying tripLET : t1_Energy and if withing range label it as an ISC############
    energy_plot.plot((x2,x3),(t1_energy,t1_energy),color='black') 
    energy_plot.text(x3+1.0,t1_energy,(round(t1_energy,2),round(1240.0/t1_energy,2)),fontsize=10)
    print 't1_energy=',t1_energy
    if abs(t1_energy-Lowest_Lying_Singlet) <= deltaE:
       energy_plot.annotate('ISC',xy=(x2,t1_energy),xytext=(x1-float((x1-x0)/3.0),Lowest_Lying_Singlet),arrowprops=dict(facecolor='orange'), color='orange',fontsize='20')

######label triplets within deltaE THRESHOLD of Lowest_Lying_Singlet and if within range label as ISC############
    plot_text = 0.0
    plot_IC = 0.0

    for index in range(len(energy_triplets)): 
        print 'index = ',index
        energy_plot.plot((x2,x3),(energy_triplets[index],energy_triplets[index]),color='black')
        Xposition.append(x3)
        Yposition.append(energy_triplets[index])
        print 'debug triplets, lowest singlet, deltaE, thresh',energy_triplets[index],Lowest_Lying_Singlet,energy_triplets[index]-Lowest_Lying_Singlet, deltaE
        # we are looking at transitions to lower triplet states. no uphill transitions, no negative phonon modes ;-)
        if(energy_triplets[index]<=Lowest_Lying_Singlet):
          if abs(energy_triplets[index]-Lowest_Lying_Singlet) <= deltaE:
             if index == 0:
                    if abs((Yposition[index] + plot_text)  - t1_energy) < deltaY:
                           plot_text=plot_text+0.25 
                           print 'hello from inside this weird loop',plot_text
             else :
                    if abs((Yposition[index] + plot_text)  - (Yposition[index - 1] + plot_text)) < deltaY:
                           plot_text=plot_text+0.25 
                           print 'hello from inside this weird loop',plot_text
             print 'printing ',Yposition[index],Lowest_Lying_Singlet,deltaE,energy_triplets[index]-Lowest_Lying_Singlet
             energy_plot.text(x3+1.0,Yposition[index] + plot_text,(energy_triplets[index],wavelength_triplets[index]),fontsize=10)
             energy_plot.annotate('ISC',xy=(x2,Yposition[index]),xytext=(x1-float((x1-x0)/3.0),Lowest_Lying_Singlet),arrowprops=dict(facecolor='orange'), color='orange',fontsize='20')
             energy_plot.annotate('IC',xy=(plot_IC + x2 ,t1_energy),xytext=(plot_IC+ x2 ,Yposition[index]),arrowprops=dict(facecolor='green'), color='green',fontsize='20')
             # move arrow after each IC plot
             plot_IC = plot_IC + 0.75
######label transition back tO GROUND STATE
    energy_plot.annotate('ISC',xy=(x1,0.0),xytext=(x3+0.1,t1_energy),arrowprops=dict(facecolor='orange'), color='orange',fontsize='20')

#plt.axis('off')
    energy_plot.axis([x0-3,x3+3.2,emin-2,Lowest_Absorbing_Singlet+2])
    energy_plot.text(x0,-0.6,'singlets',color='blue',fontsize='20')
    energy_plot.text(x2,-0.6,'triplets',color='blue',fontsize='20')
#plt.setp(plt.get_xticklabels(),visible=False)
#plt.show()
    title+=".pdf"
    energy_figure.savefig(title)
    print " end of ", title
