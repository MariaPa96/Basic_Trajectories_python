# Basic trajectories calculator

*The base code of this package was given by Jhayron S. Pérez-Carrasquilla, who used it in different research, as in [Hoyos et al.(2019)](https://nhess.copernicus.org/articles/19/2635/2019/nhess-19-2635-2019.html). I constructed this code as a package to improve its versatility in work with the [Sistema de Alerta Temprana de Medellín y el Valle de Aburrá (SIATA)](https://siata.gov.co/siata_nuevo/).*

This repository contains a code (Trajectories_AOD.py) for calculating back and forward trajectories from the basic theory, represented by the following equation:

$X(t-\Delta t)=X(t)-V(X,t)\Delta t$

X is the location with vertical and horizontal coordinators, V is the wind vector, and t is the time. 

The code is recommended for operational work and general overviewing of mesoscale transport (this contains the possibility of following aerosols). The main code, Trajectories_AOD, has shown high versatility; only three steps are needed.

1. Clone the Trajectories_AOD.py code.

2. Download the wind components U-wind, V-wind, and Omega 4X Daily pressure levels from NCEP-NCAR Reanalysis 1 data provided by the NOAA PSL, Boulder, Colorado, USA, from their website at https://downloads.psl.noaa.gov/Datasets/ncep.reanalysis/pressure/.
   
   *Optional*: Download monthly Total Aerosol Optical Depth at 550nm, step 0, Time  00:00 y 12:00 provided by CAMS-Copernicus from their website at https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-atmospheric-composition-forecasts?tab=overview
Name the files as AOD_%m-%Y.nc (example: AOD_08-2019.nc)

3. Please ensure that everything in your environment, including the Requirements.txt, is properly set up. Make sure you know the location of your data and that all data is stored in the same folder.
   
This repository includes a Jupyter script to demonstrate how to use the code, but the following are the basic steps.
Imagine I want to calculate the trajectories for every day in January 2022 without AOD. Then, I need to ensure I have the files in my path for 2022.nc, vwnd.2022.nc and omega.2022.nc. The following script in Python language should work: 

## Let's start to code!

First, import the packets. Pickle is useful for storing the resulting dictionary; pandas also have that function now. Nonetheless, none of them are compulsory for running the code.
```ruby
import Trajectories_AOD  #### line 0
import pickle            #### line 1
```
Trajectories_AOD has the class Follow there; you should add the initial and final date for running the trajectories.
Note: Your data should cover the period selected.
```ruby
Tr=Trajectories_AOD.Follow(Fechai='2022-01-01',Fechaf='2022-02-01')  #### line 2
```

The function Trajectories is the entrance of any other option needed for your tractories:
- AOD: is a (boolean, default=False),
- ndays: (number, default=8) ending number of days back or forward for calculating trajectories
- delta_d: (number, default=3) number of hours for calculating every step back or forward.
- back: is a (boolean, default= True), True for back-trajectories, False for Forward-trajectories
- plevels: pressure levels [hPa] for staring trajectories calculation (array, np.array([850,800,750,700,650,600,550,500]))
```ruby
Tr.Trajectories(AOD=False)                                           #### line 3
```

The trajectories will be presented in a nested dictionary with the name Tr.BT
```ruby
Tr.BT.keys()
dict_keys(['lat_traj', 'lon_traj', 'plev_traj', 'datetime_traj', 'steps_traj','aod_traj'])
```
- lat_traj and lon_traj: have the latitude and longitude in degrees for every step of the trajectory 
- plev_traj: contains the pressure levels for every step in hPa units.
- datetime_traj: has the starting time of all trajectories ran.
- steps_traj: contains the date and time for every step.
- aod_traj: AOD information 
  
Those are also dictionaries with three dimensions: the first one references every starting pressure level, the second every starting date, and the last one the trajectories longitude in step time. 

The following lines are for storing the dictionary Tr.BT
```ruby
f = open("Trajectories/BT_"+date.strftime('%Y%m')+".pkl","wb")         #### line 4
pickle.dump(Tr.BT,f)                                                 #### line 5
```





