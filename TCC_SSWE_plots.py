
import pandas as pd
import matplotlib.tri as tri#import Triangulation, TriAnalyzer, UniformTriRefiner
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
	
cbar_mintemp = 50;
cbar_maxtemp = 110;

def plotLonLatDataTri(lon, lat, data, title):
	triang = tri.Triangulation(lon, lat)
	
	fig, ax = plt.subplots()
	plt.gca().set_aspect('equal')
	plt.tripcolor(triang, data, cmap=cm.jet, vmin=cbar_mintemp, vmax=cbar_maxtemp)
	cbar = plt.colorbar()
	
	cbar.set_label('Temperature [DEG F]', rotation=270)
	plt.title(title)
	ax.set_xlabel('Longitude [DEG]')
	ax.set_ylabel('Latitude [DEG]')
	return fig

def plotLonLatDataScatter(lon, lat, data, title):
	fig, ax = plt.subplots()
	plt.gca().set_aspect('equal')
	plt.scatter(lon, lat, c=data, s=100, cmap=cm.jet, vmin=cbar_mintemp, vmax=cbar_maxtemp)
	plt.title(title)
	ax.set_xlabel('Longitude [DEG]')
	ax.set_ylabel('Latitude [DEG]')
	return fig