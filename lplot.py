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