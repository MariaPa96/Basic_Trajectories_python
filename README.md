# Basic trajectories calculator
[![DOI](https://zenodo.org/badge/681665732.svg)](https://zenodo.org/doi/10.5281/zenodo.13730207)

This repository contains a code (Trajectories_AOD.py) for calculating back and forward trajectories from the basic theory, represented by the following equation:

$X(t-\Delta t)=X(t)-V(X,t)\Delta t$

Where $X$ is the location with vertical and horizontal coordinators, $V$ is the wind vector, and $t$ is the time. 

The code is recommended for operational work, general overviewing, and investigation of mesoscale transport (this includes the possibility of tracking aerosols). Now, to start:

1. Clone or Download this repository. The repository contains two files, each for two different options to set all needed packages for using the code: environment.yml and requirements.txt. The first includes everything required to create an environment for running the code (including all the packages), while the second only lists the packages needed. This last if you only want to install the packages that may remain uninstalled in your current environment.
   
```ruby
### So, in your terminal, you may want to use one of these lines if you are using conda:
## Option 1: creating an environment.
conda env create -f environment.yml
## Option 2: installing the needed packages.
conda install --yes --file requirements.txt
```

2. Download the wind components U-wind, V-wind, and Omega 4X Daily pressure levels from NCEP-NCAR Reanalysis 1 data provided by the NOAA PSL, Boulder, Colorado, USA, from their website at https://downloads.psl.noaa.gov/Datasets/ncep.reanalysis/pressure/ (last access: 1 October 2024). You will quickly identify them as uwnd.YYYY.nc, vwnd.YYYY.nc and omega.YYYY.nc, where YYYY is a four-number format of the year (e.g. 2024).
   
   *Optional*: Download monthly Total Aerosol Optical Depth at 550nm, step 0, Time  00:00 y 12:00 provided by CAMS-Copernicus from their website at https://ads.atmosphere.copernicus.eu/datasets/cams-global-reanalysis-eac4 (last access: 1 October 2024).
Name the files as AOD_%m-%Y.nc (e.g., AOD_08-2019.nc)

   Please ensure you know your data's location and that all data is stored in the same folder.
   
3. **Let's start to code!**. This repository includes the Jupyter script *BT_example.ipynb* to demonstrate how to use the code and some basic information about the options and outputs.

***Author contributions**. The base functions of this package were created by Dario A. Hernández and Jhayron S. Pérez-Carrasquilla; the original version of this code was used in different unpublished and published investigations as in [Hoyos et al.(2019)](https://nhess.copernicus.org/articles/19/2635/2019/nhess-19-2635-2019.html) and [Peréz-Carrasquilla et al.(2023)](https://ascmo.copernicus.org/articles/9/121/2023/). Maria P. Velázquez-García reorganized the spare functions into a class, added new functions and options to enhance its versatility, and documented it for open access. This version was used in the accepted publication [Velásquez-García et al. (2024)](https://egusphere.copernicus.org/preprints/2024/egusphere-2024-695/). The code was developed in collaboration with the [Sistema de Alerta Temprana de Medellín y el Valle de Aburrá (SIATA)](https://siata.gov.co/siata_nuevo/) and Universidad Nacional de Colombia - sede Medellín.*



