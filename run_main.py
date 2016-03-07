import pandas as pd
import numpy as np

from logic import sample_sim
from lplot import plot_latlon_tri
from lplot import plot_latlon_scat

from params import TRAIN_CSV
from params import PREDICT_CSV
from params import OUTPUT_CSV
from params import RHO
from params import SIGMA2
from params import M_REALIZE

## Part 1 
train_data = pd.read_csv(TRAIN_CSV)#, nrows=10)
predict_data = pd.read_csv(PREDICT_CSV)#, nrows=75)

train_temp = train_data.temperature.values.tolist()
train_long = train_data.long.values.tolist()
train_lat = train_data.lat.values.tolist()
pred_long = predict_data.long.values.tolist()
pred_lat = predict_data.lat.values.tolist()

realize_array = sample_sim(x0=train_temp, long0=train_long, lat0=train_lat,
 long1=pred_long, lat1=pred_lat, sigma2=SIGMA2, rho=RHO, m_realiz=M_REALIZE)

# Part 2
# TODO: Tests
# Part 3
predict_data['cond_mean'] = np.mean(realize_array, axis=0).T;
predict_data['cond_stddev'] = np.std(realize_array, axis=0).T;
predict_data['realize_1'] = realize_array[0,:].T;
predict_data['realize_2'] = realize_array[1,:].T;
predict_data['realize_3'] = realize_array[2,:].T;
predict_data['realize_4'] = realize_array[3,:].T;
predict_data.to_csv(OUTPUT_CSV, header=True, index=False)

fhandle = plot_latlon_tri(lon=train_long, lat=train_lat, data=train_temp, title='Temp by Lon/Lat (Training)')
fhandle.savefig('tempMap_Training.png')
# fhandle = plot_latlon_tri(lon=pred_long, lat=pred_lat, data=predict_data.cond_stddev, title='Temp by Lon/Lat (Standard Dev Sim)')
# fhandle.savefig('tempMap_stddev.png')
fhandle = plot_latlon_tri(lon=pred_long, lat=pred_lat, data=predict_data.cond_mean, title='Temp by Lon/Lat (Mean Sim)')
fhandle.savefig('tempMap_mean.png')
fhandle = plot_latlon_tri(lon=pred_long, lat=pred_lat, data=predict_data.realize_1, title='Temp by Lon/Lat (Sim 1)')
fhandle.savefig('tempMap_Sim1.png')
fhandle = plot_latlon_tri(lon=pred_long, lat=pred_lat, data=predict_data.realize_2, title='Temp by Lon/Lat (Sim 2)')
fhandle.savefig('tempMap_Sim2.png')
fhandle = plot_latlon_tri(lon=pred_long, lat=pred_lat, data=predict_data.realize_3, title='Temp by Lon/Lat (Sim 3)')
fhandle.savefig('tempMap_Sim3.png')
fhandle = plot_latlon_tri(lon=pred_long, lat=pred_lat, data=predict_data.realize_4, title='Temp by Lon/Lat (Sim 4)')
fhandle.savefig('tempMap_Sim4.png')
fhandle = plot_latlon_scat(lon=pred_long, lat=pred_lat, data=predict_data.realize_4, title='Temp by Lon/Lat (Sim 4)')
fhandle.savefig('tempMapScat_Sim4.png')