
The code Trajectories_AOD has shown high versatility, for its use only four key steps are needed. The third step is actually optional if you do not want to run the code recognising the AOD then you can skip this.   

1. Clone the Trajectories_AOD.py code.

2. Download the wind components U-wind, V-wind and Omega 4X Daily, pressure levels from NCEP-NCAR Reanalysis 1 data provided by the NOAA PSL, Boulder, Colorado, USA, from their website at https://downloads.psl.noaa.gov/Datasets/ncep.reanalysis/pressure/

3. Optional: Download monthly Total Aerosol Optical Depth at 550nm, step 0, Time  00:00 y 12:00 provided by CAMS-COpernicus from their website at https://ads.atmosphere.copernicus.eu/cdsapp#!/dataset/cams-global-atmospheric-composition-forecasts?tab=overview
Name the files as AOD_%m-%Y.nc (example: AOD_08-2019.nc)

4. Change the self.path in the .py for the file where you store the data dowloaded on step 2 and 3. 

Now an example, imagine I want to calculate the trajectories for every day in January 2022 without AOD, then I need to ensure to have in my path the files uwnd.2022.nc, vwnd.2022.nc and omega.2022.nc. The follwing script in python language should work: 

import Trajectories_AOD
import pickle


self=Trajectories_AOD.Follow(Fechai='2022-01-01',Fechaf='2022-02-01')
self.Trajectories(AOD=False)
f = open("AInteres/Tj_"+date.strftime('%Y%m')+".pkl","wb")
pickle.dump(self.BT,f)




