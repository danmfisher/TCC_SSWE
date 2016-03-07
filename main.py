import pandas as pd
import numpy as np

from logic import sample_sim
from lplot import publish_plots
from params import TRAIN_CSV, PREDICT_CSV, OUTPUT_CSV
from params import RHO, SIGMA2, M_REALIZE

def main():
	## Part 1 
	train_data = pd.read_csv(TRAIN_CSV)
	predict_data = pd.read_csv(PREDICT_CSV)

	realize_array = sample_sim(x0=train_data.temperature,
		long0=train_data.long,
		lat0=train_data.lat,
		long1=predict_data.long,
		lat1=predict_data.lat, 
		sigma2=SIGMA2, 
		rho=RHO, 
		m_realiz=M_REALIZE)

	# Part 2
	# in a command window here, run "py.test"

	
	# Part 3
	predict_data['cond_mean'] = np.mean(realize_array, axis=0).T
	predict_data['cond_stddev'] = np.std(realize_array, axis=0).T
	predict_data['realize_1'] = realize_array[0,:].T
	predict_data['realize_2'] = realize_array[1,:].T
	predict_data['realize_3'] = realize_array[2,:].T
	predict_data['realize_4'] = realize_array[3,:].T
	
	predict_data.to_csv(OUTPUT_CSV, header=True, index=False)

	publish_plots(train_data=train_data,
		predict_data=predict_data,
		save_fig=True)

if __name__ == "__main__": 
	main()
