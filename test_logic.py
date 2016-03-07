import pandas as pd
import numpy as np

from logic import sample_sim, gen_square_cov, gen_mn_cov, haversine
from params import TRAIN_CSV, PREDICT_CSV, OUTPUT_CSV
from params import RHO, SIGMA2, M_REALIZE

TRAIN_DATA = pd.read_csv(TRAIN_CSV, nrows=20)
PREDICT_DATA = pd.read_csv(PREDICT_CSV, nrows=15)

def test_hav_distance():
	lat1 = 52.2296756
	lon1 = 21.0122287
	lat2 = 52.406374
	lon2 = 16.9251681
	assert haversine(lon1_DEG=lon1,
		lat1_DEG=lat1,
		lon2_DEG=lon2,
		lat2_DEG=lat2) == 278.54558935106695

def test_square_cov():
	cov_matrix = gen_square_cov(lon_DEG=TRAIN_DATA.long,
		lat_DEG=TRAIN_DATA.lat,
		sigma2=SIGMA2,
		rho=RHO)
	n = len(TRAIN_DATA.index)
	assert cov_matrix.shape[0] == cov_matrix.shape[1] == n

def test_mn_cov():
	cov_matrix = gen_mn_cov(lon1_DEG=TRAIN_DATA.long,
		lat1_DEG=TRAIN_DATA.lat,
		lon2_DEG=PREDICT_DATA.long,
		lat2_DEG=PREDICT_DATA.lat,
		sigma2=SIGMA2,
		rho=RHO)
	n = len(TRAIN_DATA.index)
	m = len(PREDICT_DATA.index)
	assert (cov_matrix.shape[0] == n) & (cov_matrix.shape[1] == m)

def test_mn_square_conv():
	cov_matrix_sq = gen_square_cov(lon_DEG=TRAIN_DATA.long,
		lat_DEG=TRAIN_DATA.lat,
		sigma2=SIGMA2,
		rho=RHO)
	cov_matrix_mn = gen_mn_cov(lon1_DEG=TRAIN_DATA.long,
		lat1_DEG=TRAIN_DATA.lat,
		lon2_DEG=TRAIN_DATA.long,
		lat2_DEG=TRAIN_DATA.lat,
		sigma2=SIGMA2,
		rho=RHO)
	assert np.array_equal(cov_matrix_mn.all(), cov_matrix_sq.all())

def test_setup_sample():
	n = len(TRAIN_DATA.index)
	m = len(PREDICT_DATA.index)
	mu_0 = np.zeros(n)
	mu_1 = np.zeros(m)

	Sigma_00 = gen_square_cov(lon_DEG=TRAIN_DATA.long,
		lat_DEG=TRAIN_DATA.lat,
		sigma2=SIGMA2,
		rho=RHO)
	Sigma_11 = gen_square_cov(lon_DEG=PREDICT_DATA.long,
		lat_DEG=PREDICT_DATA.lat,
		sigma2=SIGMA2,
		rho=RHO)
	Sigma_01 = gen_mn_cov(lon1_DEG=TRAIN_DATA.long,
		lat1_DEG=TRAIN_DATA.lat,
		lon2_DEG=PREDICT_DATA.long,
		lat2_DEG=PREDICT_DATA.lat,
		sigma2=SIGMA2,
		rho=RHO)
	Sigma_10 = Sigma_01.transpose()
	mu_cond = mu_1 + np.dot(Sigma_10, TRAIN_DATA.temperature - mu_0)
	sigma_cond = Sigma_11 + np.dot(Sigma_10,  np.dot(np.linalg.inv(Sigma_00), Sigma_01))
	assert mu_cond.shape[0] == sigma_cond.shape[0] == sigma_cond.shape[1] == m

def test_sample_shape():
	m = len(PREDICT_DATA.index)
	rv = sample_sim(x0=TRAIN_DATA.temperature,
		long0=TRAIN_DATA.long,
		lat0=TRAIN_DATA.lat,
		long1=PREDICT_DATA.long,
		lat1=PREDICT_DATA.lat,
		sigma2=SIGMA2,
		rho=RHO,
		m_realiz=1)
	assert(rv.shape[0] == 1) & (rv.shape[1] == m)

# def test_sample_quality():
# 	m = len(PREDICT_DATA.index)
# 	rv = sample_sim(x0=TRAIN_DATA.temperature,
# 		long0=TRAIN_DATA.long,
# 		lat0=TRAIN_DATA.lat,
# 		long1=PREDICT_DATA.long,
# 		lat1=PREDICT_DATA.lat,
# 		sigma2=SIGMA2,
# 		rho=RHO,
# 		m_realiz=1)
# 	print(rv.min())
# 	print(rv.max())
# 	assert(rv.min() > 0)
# 	assert(rv.max() < 200)