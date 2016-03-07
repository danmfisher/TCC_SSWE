
import pandas as pd
import numpy as np

from logic import sample_sim
from lplot import publish_plots#plot_latlon_tri, plot_latlon_scat

from params import TRAIN_CSV, PREDICT_CSV, OUTPUT_CSV
from params import RHO, SIGMA2, M_REALIZE

def main():
	## Part 1 
	train_data = pd.read_csv(TRAIN_CSV)#, nrows=10)
	predict_data = pd.read_csv(PREDICT_CSV)#, nrows=75)

	train_temp = train_data.temperature.values.tolist()
	train_long = train_data.long.values.tolist()
	train_lat = train_data.lat.values.tolist()
	pred_long = predict_data.long.values.tolist()
	pred_lat = predict_data.lat.values.tolist()

	realize_array = sample_sim(x0=train_temp,
		long0=train_long,
		lat0=train_lat,
		long1=pred_long,
		lat1=pred_lat, 
		sigma2=SIGMA2, 
		rho=RHO, 
		m_realiz=M_REALIZE)

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

	publish_plots(train_long=train_long, 
		train_lat=train_lat, 
		train_temp=train_temp, 
		pred_long=pred_long, 
		pred_lat=pred_lat,
		predict_data=predict_data,
		save_fig=True)