import matplotlib.tri as tri
import matplotlib.pyplot as plt
import matplotlib.cm as cm
	
CBAR_MINT = 50
CBAR_MAXT = 110
LONG_LABEL = 'Longitude [DEG]'
LAT_LABEL = 'Latitude [DEG]'
TEMP_LABEL = 'Temperature [DEG F]'

def plot_latlon_tri(lon=None, lat=None, data=None, title='Title', 
	vmin_in=CBAR_MINT, vmax_in=CBAR_MAXT):
	triang = tri.Triangulation(lon, lat)
	fig, ax = plt.subplots()
	plt.gca().set_aspect('equal')
	plt.tripcolor(triang, data, cmap=cm.jet, vmin=vmin_in, vmax=vmax_in)
	label_plot(fig, ax, title)
	return fig

def plot_latlon_scat(lon=None, lat=None, data=None, title='Title',
	vmin_in=CBAR_MINT, vmax_in=CBAR_MAXT, data_label=TEMP_LABEL):
	fig, ax = plt.subplots()
	plt.gca().set_aspect('equal')
	plt.scatter(lon, lat, c=data, s=100, cmap=cm.jet, vmin=vmin_in, vmax=vmax_in)
	label_plot(fig, ax, title, data_label)
	return fig

def label_plot(fig=None, ax=None, title='Title', data_label=TEMP_LABEL):
	cbar = plt.colorbar()
	cbar.set_label(data_label, rotation=270)
	plt.title(title)
	ax.set_xlabel(LONG_LABEL)
	ax.set_ylabel(LAT_LABEL)
	return 0

def publish_plots(train_data=None,
		predict_data=None,
		save_fig=True):

	fhandle = plot_latlon_tri(lon=train_data.long, lat=train_data.lat, 
		data=train_data.temperature, title='Temp by Lon/Lat (Training)')
	if(save_fig): fhandle.savefig('tempMap_Training.png')
	
	fhandle = plot_latlon_tri(lon=predict_data.long, lat=predict_data.lat,  
		data=predict_data.cond_mean, title='Temp by Lon/Lat (Mean Sim)')
	if(save_fig): fhandle.savefig('tempMap_mean.png')

	fhandle = plot_latlon_tri(lon=predict_data.long, lat=predict_data.lat, 
		data=predict_data.realize_1, title='Temp by Lon/Lat (Sim 1)')
	if(save_fig):fhandle.savefig('tempMap_Sim1.png')
	
	fhandle = plot_latlon_tri(lon=predict_data.long, lat=predict_data.lat,  
		data=predict_data.realize_2, title='Temp by Lon/Lat (Sim 2)')
	if(save_fig):fhandle.savefig('tempMap_Sim2.png')
	
	fhandle = plot_latlon_tri(lon=predict_data.long, lat=predict_data.lat,  
		data=predict_data.realize_3, title='Temp by Lon/Lat (Sim 3)')
	if(save_fig):fhandle.savefig('tempMap_Sim3.png')
	
	fhandle = plot_latlon_tri(lon=predict_data.long, lat=predict_data.lat, 
		data=predict_data.realize_4, title='Temp by Lon/Lat (Sim 4)')
	if(save_fig):fhandle.savefig('tempMap_Sim4.png')
	
	fhandle = plot_latlon_scat(lon=predict_data.long, lat=predict_data.lat,  
		data=predict_data.realize_4, title='Temp by Lon/Lat (Sim 4)')
	if(save_fig): fhandle.savefig('tempMapScat_Sim4.png')

	fhandle = plot_latlon_scat(lon=predict_data.long, lat=predict_data.lat, 
		data=predict_data.cond_stddev, title='Temp by Lon/Lat (Standard Dev Sim)',
		vmin_in=0, vmax_in=3, data_label='Standard Deviation')
	if(save_fig): fhandle.savefig('tempMap_stddev.png')