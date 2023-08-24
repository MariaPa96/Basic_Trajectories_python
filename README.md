This repository contains a code (Trajectories_AOD.py) for calculating back and forward trajectories from the basic theory, this is recommended for operational work and a general overview of scalars transport. The code Trajectories_AOD has shown high versatility, for its use only four key steps are needed. The third step is actually optional if you do not want to run the code recognizing the AOD then you can skip this.   

1. Clone the Trajectories_AOD.py code.

2. Download the wind components U-wind, V-wind and Omega 4X Daily, pressure levels from NCEP-NCAR Reanalysis 1 data provided by the NOAA PSL, Boulder, Colorado, USA, from their website at https://downloads.psl.noaa.gov/Datasets/ncep.reanalysis/pressure/

3. Optional: Download monthly Total Aerosol Optical Depth at 550nm, step 0, Time  00:00 y 12:00 provided by CAMS-COpernicus from their website at https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-atmospheric-composition-forecasts?tab=overview
Name the files as AOD_%m-%Y.nc (example: AOD_08-2019.nc)

4. Change the self.path in the .py for the file where you store the data downloaded on steps 2 and 3. 

Now an example, imagine I want to calculate the trajectories for every day in January 2022 without AOD, then I need to ensure to have in my path the files uwnd.2022.nc, vwnd.2022.nc and omega.2022.nc. The following script in Python language should work: 

### Import the packets, pickle is really useful for storing the resulting dictionary; however I know also pandas have that function now
### but is really not needed for running the trajectories

import Trajectories_AOD  #### line 0
import pickle            #### line 1

### Trajectories_AOD has the class Follow there you should add the initial and final date for running the trajectories
### Note: Your data should cover the period of time selected.
self=Trajectories_AOD.Follow(Fechai='2022-01-01',Fechaf='2022-02-01')  #### line 2

### The function Trajectories is the entrance of any other option needed for your tractories:
### AOD: is a (boolean, default=False), ndays: (number, default=8) ending number of days back or forward for calculating trajectories  
### delta_d: (number, default=8) number of hours for calculating every step back or forward
### back: is a (boolean, default= True), True for back-trajectories, false for Forward-trajectories
### plevels: presion levels for staring trajectories calculation (array, np.array([850,800,750,700,650,600,550,500]))
self.Trajectories(AOD=False)                                           #### line 3

### The results will be presented in a nested dictionary with the name self.BT

### The following lines are for storing the dictionary self.BT 
f = open("Trajectories/BT_"+date.strftime('%Y%m')+".pkl","wb")         #### line 4
pickle.dump(self.BT,f)                                                 #### line 5






