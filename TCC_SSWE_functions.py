import numpy as np
import math
import pandas as pd
from scipy.stats import multivariate_normal

def sampleSim(x0, long0, lat0, long1, lat1, sigma2, rho, m_realiz):
# This function that simulates m realizations 
# from a conditional probability distribution 
# INPUT
# 		x0 			the observations, 
# 		long0 		the location of the observations, 
# 		lat0 		the location of the observations, 
# 		long1 		the locations we want to predict,  
# 		lat1 		the locations we want to predict, 
# 		σ2 			the parameter sigma squared
#		ρ 			the parameter rho the values of the parameters
# 		m_realiz	the number of realizations of the sim to compute
#
# OUTPUT 
# 		realize_array 	The output should be in the form of a m×n1 array
	N = len(x0)
	M = len(lat1)
	mu_0 = np.zeros(N)
	mu_1 = np.zeros(M)

	Sigma_00 = genSquareCovMatrix(long0, lat0, sigma2, rho)
	Sigma_11 = genSquareCovMatrix(long1, lat1, sigma2, rho)
	Sigma_01 = genMNCovMatrix(long0, lat0, long1, lat1, sigma2, rho)
	Sigma_10 = Sigma_01.transpose()

	mu_cond = mu_1 + np.dot(Sigma_10, x0 - mu_0)
	sigma_cond = Sigma_11 + np.dot(Sigma_10,  np.dot(np.linalg.inv(Sigma_00), Sigma_01))
	realize_array = np.random.multivariate_normal(mu_cond, sigma_cond, m_realiz)

	return realize_array

def genSquareCovMatrix(lon_DEG, lat_DEG, sigma, rho):
	# function assumes covariance fuction is of the form from the pdf:
	# 		[SIGMA_00]ij = sigma^2 * exp(-d0ij / rho)
	# INPUTS
	# 	lon_DEG		array* of longitude data in degrees
	# 	lat_DEG 	array* of latitude data in degrees
	# 	sigma 	 	parameter
	# 	rho 		parameter
	# *arrays of lat/lon must be the same length.
	#
	# OUTPUTS
	# 	cov_matrx 	a symmetric NxN covariance matrix where N is the length of the lat/lon array

	N = len(lat_DEG)
	cov_matrx = np.zeros((N,N))

	for i in range(N):
		for j in range(i, N):
			# E calculation: sigma square * exp(-dist / rho)
			E = math.pow(sigma,2)*math.exp(-1*haversine(lon_DEG[i], lat_DEG[i], lon_DEG[j], lat_DEG[j])/rho)
			cov_matrx[i][j] = cov_matrx[j][i] = E

	return cov_matrx


def genMNCovMatrix(lon1_DEG, lat1_DEG, lon2_DEG, lat2_DEG, sigma, rho):
	N = len(lon1_DEG)
	M = len(lon2_DEG)
	cov_matrx = np.zeros((N,M))
	
	for i in range(N):
		for j in range(M):
			# E calculation: sigma square * exp(-dist / rho)
			E = math.pow(sigma,2)*math.exp(-1*haversine(lon1_DEG[i], lat1_DEG[i], lon2_DEG[j], lat2_DEG[j])/rho)
			cov_matrx[i][j] = E

	return cov_matrx


def haversine(lon1_DEG, lat1_DEG, lon2_DEG, lat2_DEG):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    http://gis.stackexchange.com/a/56589/15183
    """
    # convert decimal degrees to radians 
    lon1_RAD, lat1_RAD, lon2_RAD, lat2_RAD = map(math.radians, [lon1_DEG, lat1_DEG, lon2_DEG, lat2_DEG])
    
    # haversine formula 
    del_lon_RAD = lon2_RAD - lon1_RAD
    del_lat_RAD = lat2_RAD - lat1_RAD
    a = math.sin(del_lat_RAD/2)**2 + math.cos(lat1_RAD) * math.cos(lat2_RAD) * math.sin(del_lon_RAD/2)**2
    c = 2 * math.asin(math.sqrt(a))
    dist_KM = 6367 * c
    
    return dist_KM