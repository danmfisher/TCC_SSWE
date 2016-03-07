import numpy as np
import math
from math import sin, cos, sqrt, atan2, radians, pow, exp
from scipy.stats import multivariate_normal

def sample_sim(x0=None, long0=None, lat0=None, long1=None, lat1=None, sigma2=1, rho=10, m_realiz=1):
	"""
	This function that simulates m realizations 
	from a conditional probability distribution 
	INPUT
			x0 				the observations, 
			long0 			the longitude location of the observations 
			lat0 			the latitude location of the observations 
			long1 			the N1 longitude locations we want to predict
			lat1 			the N1 latitude locations we want to predict 
			sigma2 			the parameter sigma squared
			rho				the parameter rho the values of the parameters
			m_realiz		the M number of realizations of the sim to compute
	
	OUTPUT 
			realize_array 	The output from simulating M realizations of the model 
							to determine a value for each of the N1 locations
	"""
	mu_0 = np.zeros(len(x0))
	mu_1 = np.zeros(len(lat1))

	Sigma_00 = gen_square_cov(lon_DEG=long0, lat_DEG=lat0, sigma2=sigma2, rho=rho)
	Sigma_11 = gen_square_cov(lon_DEG=long1, lat_DEG=lat1, sigma2=sigma2, rho=rho)
	Sigma_01 = gen_mn_cov(lon1_DEG=long0, lat1_DEG=lat0, lon2_DEG=long1, lat2_DEG=lat1, sigma2=sigma2, rho=rho)
	Sigma_10 = Sigma_01.transpose()

	mu_cond = mu_1 + np.dot(Sigma_10, x0 - mu_0)
	sigma_cond = Sigma_11 + np.dot(Sigma_10,  np.dot(np.linalg.inv(Sigma_00), Sigma_01))
	realize_array = np.random.multivariate_normal(mu_cond, sigma_cond, m_realiz)

	return realize_array

def gen_square_cov(lon_DEG=None, lat_DEG=None, sigma2=1, rho=10):
	"""
	function assumes covariance fuction is of the form from the pdf:
			[SIGMA_00]ij = sigma^2 * exp(-d0ij / rho)
	INPUTS
		lon_DEG		array* of longitude data in degrees
		lat_DEG 	array* of latitude data in degrees
		sigma2 	 	the parameter sigma squared
		rho 		the parameter rho
	*arrays of lat/lon must be the same length, N.
	
	OUTPUTS
		cov_matrx 	a symmetric NxN covariance matrix where 
					N is the length of the lat/lon array
	"""
	N = len(lat_DEG)
	cov_matrx = np.zeros((N,N))

	for i in range(N):
		for j in range(i, N):
			# E calculation: sigma square * exp(-dist / rho)
			E = sigma2*exp(-1*haversine(lon_DEG[i], lat_DEG[i], lon_DEG[j], lat_DEG[j])/rho)
			cov_matrx[i][j] = cov_matrx[j][i] = E

	return cov_matrx


def gen_mn_cov(lon1_DEG=None, lat1_DEG=None, lon2_DEG=None, lat2_DEG=None, sigma2=1, rho=10):
	"""
	function assumes covariance fuction is of the form from the pdf:
			[SIGMA_01]ij = sigma^2 * exp(-d0ij / rho)
	INPUTS
		lon1_DEG	array* of longitude for first set of data in degrees
		lat1_DEG 	array* of latitude for first set of data in degrees
		lon2_DEG	array* of longitude for second set of data in degrees
		lat2_DEG 	array* of latitude for second set of data in degrees
		sigma 	 	parameter
		rho 		parameter
	*arrays of lat/lon must be the same length, N, and M respectively,
	for each dataset.
	
	OUTPUTS
		cov_matrx 	a symmetric NxM covariance matrix 
					where N is the length the first set of location data
					and M is the length the second set of location data
	"""
	N = len(lon1_DEG)
	M = len(lon2_DEG)
	cov_matrx = np.zeros((N,M))
	
	for i in range(N):
		for j in range(M):
			# E calculation: sigma square * exp(-dist / rho)
			E = sigma2*exp(-1*haversine(lon1_DEG[i], lat1_DEG[i], lon2_DEG[j], lat2_DEG[j])/rho)
			cov_matrx[i][j] = E

	return cov_matrx


def haversine(lon1_DEG=None, lat1_DEG=None, lon2_DEG=None, lat2_DEG=None):
	"""
    Calculates the great circle distance between two points 
    on the earth (specified in decimal degrees)
    http://gis.stackexchange.com/a/56589/15183
    """
	R_KM = 6373.0 # approximate radius of earth in km

	lon1_RAD, lat1_RAD, lon2_RAD, lat2_RAD = map(math.radians, [lon1_DEG, lat1_DEG, lon2_DEG, lat2_DEG])
	dlon = lon2_RAD - lon1_RAD
	dlat = lat2_RAD - lat1_RAD

	a = sin(dlat / 2)**2 + cos(lat1_RAD) * cos(lat2_RAD) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))
	distance_KM = R_KM * c

	return distance_KM
