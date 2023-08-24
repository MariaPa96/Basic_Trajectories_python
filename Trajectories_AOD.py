# -*- coding: utf-8 -*-
#!/usr/bin/env python
#

import matplotlib
#matplotlib.use('Template')
matplotlib.use('PDF')
import numpy as np
import datetime as dt
import os
import glob
#import utm
import pickle
import netCDF4 as nc
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import argrelextrema

import shapefile as shp
import matplotlib.font_manager as font_manager

### https://psl.noaa.gov/data/gridded/data.ncep.reanalysis.html
### https://downloads.psl.noaa.gov/Datasets/ncep.reanalysis/pressure/
#######################################################
def find_nearest_idx(array, value):
    # Encuentra la posición  más cercano en un array 1D
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


#######################################################
class Follow:

	def __init__(self,Fechai=None, Fechaf=None,path=None,lati=6.25,loni=-75.6):
		#os.system('mkdir Figuras')
		self.Fechai      = (dt.datetime.now()-relativedelta(months=1)).strftime('%Y-%m-')+'01 01:00' if (Fechaf == None) else Fechai
		self.Fechaf      = (pd.to_datetime(self.Fechai)+ relativedelta(months=1)-dt.timedelta(hours=1)).strftime('%Y-%m-%d %H:%M') if (Fechaf == None) else Fechaf
		self.path	=  'E:/ERA/Trayectorias/' if path==None else path
		self.lati	=  lati
		self.loni	=  loni

		self.fechas=pd.date_range(self.Fechai,self.Fechaf,freq='12h')

		try:
			self.dataset_u = nc.Dataset(self.path+'uwnd.%s.nc'%self.Fechaf[:4])
			self.dataset_v = nc.Dataset(self.path+'vwnd.%s.nc'%self.Fechaf[:4])
			self.dataset_omega = nc.Dataset(self.path+'omega.%s.nc'%self.Fechaf[:4])
			dataset_for_localization = nc.Dataset(self.path+'omega.%s.nc'%self.Fechaf[:4])
			self.lat_dataset = dataset_for_localization.variables['lat'][:].data
			self.lon_dataset = dataset_for_localization.variables['lon'][:].data
			self.levels = dataset_for_localization.variables['level'][:].data
			self.lon_dataset[self.lon_dataset>180] = self.lon_dataset[self.lon_dataset>180]-360

		except:
			print ('We did not find the file: %d'%unico)

		self.datetimes_dataset = np.array([dt.datetime(1800,1,1,0,0)+
				              dt.timedelta(hours = float(dataset_for_localization.variables['time'][:].data[i])) 
				              for i in range(len(dataset_for_localization.variables['time'][:].data))])


		self.levels_iter = np.array([850,800,750,700,650,600,550,500])
		self.region	 = {'valle':{'latmax':7,'latmin':5,'lonmax':-74.5,'lonmin':-76.58}}



	def Read_AOD(self,*args,**kwargs):
		var		= kwargs.get('Variable',None)
		self.month  = kwargs.get('month',np.unique(self.fechas.month)[0])
		self.year = kwargs.get('year',np.unique(self.fechas.year)[0])

		dataset_aod = nc.Dataset(self.path+'AOD_%s-%d.nc'%(str(self.month).zfill(2),self.year))
		self.dataset_aod = nc.Dataset(self.path+'AOD_%s-%d.nc'%(str(self.month).zfill(2),self.year))
		self.lat_aod = self.dataset_aod.variables['latitude'][:].data
		self.lon_aod = self.dataset_aod.variables['longitude'][:].data
		self.lon_aod[self.lon_aod>180] = self.lon_aod[self.lon_aod>180]-360
		self.datetimes_aod = np.array([dt.datetime(1900,1,1,0,0)+
                              dt.timedelta(hours = float(self.dataset_aod.variables['time'][:].data[i])) 
                              for i in range(len(self.dataset_aod.variables['time'][:].data))])



	def data_from_nc(self,level,dti,lati,loni):

		# Leo el viento que necesito del netcdf
		pos_date = find_nearest_idx(self.datetimes_dataset,dti)
		pos_lat = find_nearest_idx(self.lat_dataset,lati)
		pos_lon = find_nearest_idx(self.lon_dataset,loni)
		pos_level = find_nearest_idx(self.levels,level)

		u = self.dataset_u.variables['uwnd'][pos_date,pos_level,pos_lat,pos_lon].data[()]
		v = self.dataset_v.variables['vwnd'][pos_date,pos_level,pos_lat,pos_lon].data[()]
		omega = self.dataset_omega.variables['omega'][pos_date,pos_level,pos_lat,pos_lon].data[()]

		if self.AOD:
			if dti.month!=self.month:
				self.Read_AOD(month=dti.month,year=dti.year)

			pos_date = find_nearest_idx(self.datetimes_aod,dti)
			pos_lat = find_nearest_idx(self.lat_aod,lati)
			pos_lon = find_nearest_idx(self.lon_aod,loni)

			aod = self.dataset_aod.variables['aod550'][pos_date,pos_lat,pos_lon]#.data[()]

			return u,v,omega,aod
		return u,v,omega




	def compute_location(self,lat0,lon0,plev0,u,v,w,delta_t,*args,**kwargs):
		Backtrajectorie		= kwargs.get('Backtrajectorie',True)
		#Forward Trajectories
		dx = u*delta_t*60*60 ## meters
		dy = v*delta_t*60*60 ## meters
		dz = (w/100)*delta_t*60*60 ##hPa
		print ('I am running :)')
		plev = plev0+(-dz if Backtrajectorie else dz)
		r_earth = 6378000
		if Backtrajectorie:
			new_latitude  = lat0  - (dy / r_earth) * (180 / np.pi)
			new_longitude = lon0 - (dx / r_earth) * (180 / np.pi) / np.cos(lat0 * np.pi/180)
		else:
		    new_latitude  = lat0  + (dy / r_earth) * (180 / np.pi)
		    new_longitude = lon0 + (dx / r_earth) * (180 / np.pi) / np.cos(lat0 * np.pi/180)
		if plev>1000:
			plev = 1000
		return new_latitude, new_longitude, plev


	def compute_BT(self,*args,**kwargs): #datetime0,lat0,lon0,plev0='surface',delta_t=1,days_back=5): # plev0 en hPa, delta t en horas. #máximo 4 días
		datetime0 =	kwargs.get('datetime0',None)
		lat0	=	kwargs.get('lat0',None)
		lon0	=	kwargs.get('lon0',None)
		plev0	=	kwargs.get('plev0',None)
		self.AOD=	kwargs.get('AOD',True)
		#delta_t =	kwargs.get('delta_t',3)
		#days_back=	kwargs.get('days_back',8)

		if plev0=='surface':
			plev0 = 900
		if self.AOD:
			u0,v0,w0,aod0 = self.data_from_nc(plev0,datetime0,lat0,lon0)
			self.aod_traj = np.array([aod0])
			aod_temp = aod0
		else:
			u0,v0,w0 = self.data_from_nc(plev0,datetime0,lat0,lon0)
		
		self.lat_traj=np.array([lat0])
		self.lon_traj=np.array([lon0])
		self.plev_traj=np.array([plev0])
		self.datetime_traj=np.array([datetime0])
		self.steps_traj=np.array([0])

		#     q_traj=np.array([q0])

		N_hours_back=int(self.ndays*24)

		#     q_temp=q0
		lon_temp=lon0
		lat_temp=lat0
		plev_temp=plev0
		datetime_temp=datetime0
		u_temp=u0
		v_temp=v0
		w_temp=w0
		

		#     print lat0,lon0
	    
		for steps_back in range(self.delta_t,(N_hours_back)+1,self.delta_t):
			lat_temp,lon_temp,plev_temp=self.compute_location(lat0=lat_temp,lon0=lon_temp,plev0=plev_temp,u=u_temp,v=v_temp,w=w_temp,delta_t=self.delta_t)
			datetime_temp=datetime_temp-dt.timedelta(hours=self.delta_t)
			#         print plev_temp,datetime_temp
			if self.AOD:
				u_temp,v_temp,w_temp, aod_temp = self.data_from_nc(plev_temp,datetime_temp,lat_temp,lon_temp)
				self.aod_traj = np.hstack([self.aod_traj,np.array(aod_temp)])
			else:
				u_temp,v_temp,w_temp = self.data_from_nc(plev_temp,datetime_temp,lat_temp,lon_temp)

			self.lat_traj=np.hstack([self.lat_traj,np.array(lat_temp)])
			self.lon_traj=np.hstack([self.lon_traj,np.array(lon_temp)])
			self.plev_traj=np.hstack([self.plev_traj,np.array(plev_temp)])
			self.datetime_traj=np.hstack([self.datetime_traj,np.array(datetime_temp)])
			self.steps_traj=np.hstack([self.steps_traj,np.array(steps_back)])

			
			if ((lon_temp>np.nanmax(self.lon_dataset))|(lon_temp<np.nanmin(self.lon_dataset))) | ((lat_temp>np.nanmax(self.lat_dataset))|(lat_temp<np.nanmin(self.lat_dataset))):
				for i in range((int((24/self.delta_t)*self.ndays+1))-len(self.steps_traj)):
					self.lat_traj=np.hstack([self.lat_traj,np.array(np.nan)])
					self.lon_traj=np.hstack([self.lon_traj,np.array(np.nan)])
					self.plev_traj=np.hstack([self.plev_traj,np.array(np.nan)])
					self.datetime_traj=np.hstack([self.datetime_traj,np.array(np.nan)])
					self.steps_traj=np.hstack([self.steps_traj,np.array(np.nan)])
					if self.AOD:
						self.aod_traj = np.hstack([self.aod_traj,np.array(np.nan)])
						n1=(int((24/self.delta_t)*self.ndays+1))-len(self.lat_traj)
						#return self.lat_traj, self.lon_traj, self.plev_traj, self.datetime_traj, self.steps_traj, self.aod_traj 
						return np.array(list(self.lat_traj)+list(np.repeat(np.nan,n1))),np.array(list(self.lon_traj)+list(np.repeat(np.nan,n1))),np.array(list(self.plev_traj)+list(np.repeat(np.nan,n1))),np.array(list(self.datetime_traj)+list(np.repeat(np.nan,n1))),np.array(list(self.steps_traj)+list(np.repeat(np.nan,n1))),np.array(list(self.aod_traj)+list(np.repeat(np.nan,n1)))

				return self.lat_traj, self.lon_traj, self.plev_traj, self.datetime_traj, self.steps_traj
		
		if self.AOD:		
			return self.lat_traj, self.lon_traj, self.plev_traj, self.datetime_traj, self.steps_traj, self.aod_traj 
		else: 
			return self.lat_traj, self.lon_traj, self.plev_traj, self.datetime_traj, self.steps_traj



	def Trajectories(self,*args,**kwargs):
		self.ndays		= kwargs.get('ndays',8)
		self.delta_t		= kwargs.get('delta_t',3)
		self.AOD		= kwargs.get('AOD',True)

		self.datetimes_iter = np.array(pd.date_range(self.Fechai,self.Fechaf,freq='3H').to_pydatetime().tolist())
		tres = 3

		self.BT = {}
		self.BT['lat_traj'] = np.zeros([len(self.levels_iter),len(self.datetimes_iter),int((24/self.delta_t)*self.ndays+1)])
		self.BT['lon_traj'] = np.zeros([len(self.levels_iter),len(self.datetimes_iter),int((24/self.delta_t)*self.ndays+1)])
		self.BT['plev_traj'] = np.zeros([len(self.levels_iter),len(self.datetimes_iter),int((24/self.delta_t)*self.ndays+1)])
		self.BT['datetime_traj'] = np.zeros([len(self.levels_iter),len(self.datetimes_iter),int((24/self.delta_t)*self.ndays+1)]).astype(object)
		self.BT['steps_traj'] = np.zeros([len(self.levels_iter),len(self.datetimes_iter),int((24/self.delta_t)*self.ndays+1)])
		if self.AOD:
			self.BT['aod_traj'] = np.zeros([len(self.levels_iter),len(self.datetimes_iter),int((24/self.delta_t)*self.ndays+1)])

		for li,leveli in enumerate(self.levels_iter):
			for di,dti in enumerate(self.datetimes_iter):
				print (leveli,dti)
				if self.AOD:
					#try:
						self.compute_BT(datetime0=dti,lat0=self.lati,lon0=self.loni,plev0=leveli, AOD=self.AOD)
						self.BT['lat_traj'][li,di,:], self.BT['lon_traj'][li,di,:], self.BT['plev_traj'][li,di,:], self.BT['datetime_traj'][li,di,:],self.BT['steps_traj'][li,di,:], self.BT['aod_traj'][li,di,:] = self.compute_BT(datetime0=dti,lat0=self.lati,lon0=self.loni,plev0=leveli, AOD=self.AOD)
					#except:pass
				else:
					self.compute_BT(datetime0=dti,lat0=self.lati,lon0=self.loni,plev0=leveli, AOD=self.AOD)

					self.BT['lat_traj'][li,di,:], self.BT['lon_traj'][li,di,:], self.BT['plev_traj'][li,di,:], self.BT['datetime_traj'][li,di,:],self.BT['steps_traj'][li,di,:] = self.compute_BT(datetime0=dti,lat0=self.lati,lon0=self.loni,plev0=leveli, AOD=self.AOD)

		if self.AOD:
			self.Hots_Spot()
