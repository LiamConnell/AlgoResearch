import filterpy as fp
import pandas as pd
import numpy as np
from yahoo_finance import Share
import datetime
from datetime import datetime
import os, re
from numpy.random import uniform
from sklearn.linear_model import LinearRegression



def get_smooth_val(ser, lookback):
    ###does not include today so that residual is relevant for return
    ls = []
    bs = []
    lr = LinearRegression()
    for i in range(len(ser)):
        a = ser[i-lookback:i].tolist()
        #print(a)
        if len(a) == 0:
            ls.append(np.nan)
            bs.append(np.nan)
        else:
            a = lr.fit(np.array(range(lookback)).reshape(lookback,1),np.array(a).reshape((lookback,1)))
            ls.append(float(a.predict(lookback)[0]))
            bs.append(float(a.coef_))
    return ls, bs



def predict(pos, movement):
    return (pos[0] + movement[0], pos[1] + movement[1])

#gets the normal dist of two dists (prediction and measurement)
def gaussian_multiply(g1, g2):
    mu1, var1 = g1
    mu2, var2 = g2
    mean = (var1*mu2 + var2*mu1) / (var1 + var2)
    variance = (var1 * var2) / (var1 + var2)
    return (mean, variance)

#below: prior is a position and varience, likelyhood is measurement pos and var
def update(prior, likelihood):
    posterior = gaussian_multiply(likelihood, prior)
    return posterior

def kalman_filter(data, sensor_var, process_var):
    x0 = (data[0], 1)
    velocity = 0
    dt = 1.
    sensor_var = sensor_var
    process_var = process_var
    process_model = (velocity*dt, process_var)
    
    x = x0
    
    
    xs, predictions = [], []
    for z in data:
        prior = predict(x, process_model)
        #print(prior)
        likelihood = (z, sensor_var)
        x = update(prior, likelihood)

        # save results
        predictions.append(prior[0])
        xs.append(x[0])
    return predictions, xs


import filterpy as fp
from filterpy.kalman import predict, update

from filterpy.common import Q_discrete_white_noise
Q = Q_discrete_white_noise(dim=2, dt=1., var=0.0035)

from filterpy.kalman import KalmanFilter

def pos_vel_filter(x, P, R, Q=0., dt=1.0):
    """ Returns a KalmanFilter which implements a
    constant velocity model for a state [x dx].T
    """
    
    kf = KalmanFilter(dim_x=2, dim_z=1)
    kf.x = np.array([x[0], x[1]]) # location and velocity
    kf.F = np.array([[1, dt],
                     [0,  1]])    # state transition matrix
    kf.H = np.array([[1, 0]])     # Measurement function
    kf.R *= R                   # measurement uncertainty
    if np.isscalar(P):
        kf.P *= P                 # covariance matrix 
    else:
        kf.P[:] = P
    if np.isscalar(Q):
        kf.Q = Q_discrete_white_noise(dim=2, dt=dt, var=Q)
    else:
        kf.Q = Q
    return kf



def run(x0=(200.,0.), P=500, R=0, Q=0, dt=1.0, data=None,
        count=0, do_plot=True, **kwargs):
    """
    `data` is a 2D numpy array; the first column contains
    the actual position, the second contains the measurements
    """

    # create the Kalman filter
    kf = pos_vel_filter(x0, R=R, P=P, Q=Q, dt=dt)  

    # run the kalman filter and store the results
    xs, cov = [], []
    for n in range(data.shape[0]):
        row = data.iloc[n]
        z = row['Close']
        #z=np.array([z])
        R = (float(row['High'])-float(row['Low']))*2
        kf.predict( )
        xs.append(kf.x)
        cov.append(kf.P)
        
        kf.update(z, R =R)
        #print(z)
        
        
        
    xs, cov = np.array(xs), np.array(cov)
    
    return xs, cov
