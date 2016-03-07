import pandas as pd
import numpy as np
import TCC_SSWE_functions as tccF
import TCC_SSWE_plots as tccP
import matplotlib.pyplot as plt

## Part 1 
train_data = pd.read_csv('./train.csv')#, nrows=10)
predict_data = pd.read_csv('./predict.csv')#, nrows=75)

in_sigma2 = 1.1
in_rho = 15
in_realiz_m = 6

train_temp = train_data.temperature.values.tolist()
train_long = train_data.long.values.tolist()
train_lat = train_data.lat.values.tolist()
pred_long = predict_data.long.values.tolist()
pred_lat = predict_data.lat.values.tolist()

realize_array = tccF.sampleSim(train_temp, train_long, train_lat, pred_long, pred_lat, in_sigma2, in_rho, in_realiz_m)

## Part 2
predict_data['cond_mean'] = np.mean(realize_array, axis=0).T;
predict_data['cond_stddev'] = np.std(realize_array, axis=0).T;
predict_data['realize_1'] = realize_array[0,:].T;
predict_data['realize_2'] = realize_array[1,:].T;
predict_data['realize_3'] = realize_array[2,:].T;
predict_data['realize_4'] = realize_array[3,:].T;
predict_data.to_csv('.\predict_out.csv', header=True, index=False)

#fig.savefig('testmap.png')

fhandle = tccP.plotLonLatDataTri(train_long, train_lat, train_temp, 'Temp by Lon/Lat (Training)')
fhandle.savefig('tempMap_Training.png')
fhandle = tccP.plotLonLatDataTri(pred_long, pred_lat, predict_data.realize_1, 'Temp by Lon/Lat (Sim 1)')
fhandle.savefig('tempMap_Sim1.png')
fhandle = tccP.plotLonLatDataTri(pred_long, pred_lat, predict_data.realize_2, 'Temp by Lon/Lat (Sim 2)')
fhandle.savefig('tempMap_Sim2.png')
fhandle = tccP.plotLonLatDataTri(pred_long, pred_lat, predict_data.realize_3, 'Temp by Lon/Lat (Sim 3)')
fhandle.savefig('tempMap_Sim3.png')
fhandle = tccP.plotLonLatDataTri(pred_long, pred_lat, predict_data.realize_4, 'Temp by Lon/Lat (Sim 4)')
fhandle.savefig('tempMap_Sim4.png')

fhandle = tccP.plotLonLatDataScatter(pred_long, pred_lat, predict_data.realize_4, 'Temp by Lon/Lat (Sim 4)')
fhandle.show()