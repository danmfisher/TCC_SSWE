import matplotlib.tri as tri
import matplotlib.pyplot as plt
import matplotlib.cm as cm
	
CBAR_MINT = 50
CBAR_MAXT = 110
LONG_LABEL = 'Longitude [DEG]'
LAT_LABEL = 'Latitude [DEG]'
TEMP_LABEL = 'Temperature [DEG F]'

def plot_latlon_tri(lon=None, lat=None, data=None, title='Title'):
	triang = tri.Triangulation(lon, lat)
	fig, ax = plt.subplots()
	plt.gca().set_aspect('equal')
	plt.tripcolor(triang, data, cmap=cm.jet, vmin=CBAR_MINT, vmax=CBAR_MAXT)
	label_plot(fig, ax, title)
	return fig

def plot_latlon_scat(lon=None, lat=None, data=None, title='Title'):
	fig, ax = plt.subplots()
	plt.gca().set_aspect('equal')
	plt.scatter(lon, lat, c=data, s=100, cmap=cm.jet, vmin=CBAR_MINT, vmax=CBAR_MAXT)
	label_plot(fig, ax, title)
	return fig

def label_plot(fig, ax, title):
	cbar = plt.colorbar()
	cbar.set_label(TEMP_LABEL, rotation=270)
	plt.title(title)
	ax.set_xlabel(LONG_LABEL)
	ax.set_ylabel(LAT_LABEL)
	return 0

def publish_plots(train_long=None, train_lat=None, train_temp=None, pred_long=None, pred_lat=None, predict_data=None, save_fig=False):
	fhandle = plot_latlon_tri(lon=train_long, lat=train_lat, 
		data=train_temp, title='Temp by Lon/Lat (Training)')
	if(save_fig): fhandle.savefig('tempMap_Training.png')
	
	# fhandle = plot_latlon_tri(lon=pred_long, lat=pred_lat, 
	# 	data=predict_data.cond_stddev, title='Temp by Lon/Lat (Standard Dev Sim)')
	# fhandle.savefig('tempMap_stddev.png')
	
	fhandle = plot_latlon_tri(lon=pred_long, lat=pred_lat, 
		data=predict_data.cond_mean, title='Temp by Lon/Lat (Mean Sim)')
	if(save_fig): fhandle.savefig('tempMap_mean.png')

	fhandle = plot_latlon_tri(lon=pred_long, lat=pred_lat, 
		data=predict_data.realize_1, title='Temp by Lon/Lat (Sim 1)')
	if(save_fig):fhandle.savefig('tempMap_Sim1.png')
	
	fhandle = plot_latlon_tri(lon=pred_long, lat=pred_lat, 
		data=predict_data.realize_2, title='Temp by Lon/Lat (Sim 2)')
	if(save_fig):fhandle.savefig('tempMap_Sim2.png')
	
	fhandle = plot_latlon_tri(lon=pred_long, lat=pred_lat, 
		data=predict_data.realize_3, title='Temp by Lon/Lat (Sim 3)')
	if(save_fig):fhandle.savefig('tempMap_Sim3.png')
	
	fhandle = plot_latlon_tri(lon=pred_long, lat=pred_lat, 
		data=predict_data.realize_4, title='Temp by Lon/Lat (Sim 4)')
	if(save_fig):fhandle.savefig('tempMap_Sim4.png')
	
	fhandle = plot_latlon_scat(lon=pred_long, lat=pred_lat, 
		data=predict_data.realize_4, title='Temp by Lon/Lat (Sim 4)')
	if(save_fig): fhandle.savefig('tempMapScat_Sim4.png')