

#
# Assuming a dataset has been prepared
# i.e. the CRIMAC preprocessing pipeline has been run (raw->zarr)
# Here we use a test data set (two files) from the annual NVG herring spawning survey
# The data includes clear herring schools midwater on the shelf outside Vesterålen

import xarray as xr
import numpy as np
import pandas as pd
import os
import json
import sys
import glob
import numpy as np
import xarray as xr
import scipy.io
import matplotlib.pyplot as plt

local = 1 # Running tests on local machine, 0->on IMR server

# Example dataset with herring schools, two (crimac-scratch/test_data/dBDiff)
# No preprocessing in Korona (ie averaging)
if local==1:
    f = '/mnt/z/test_data/dBDiff/ACOUSTIC/GRIDDED/out/S2024204001_sv.zarr'
elif local==0:
    f = '/data/crimac-scratch/test_data/dBDiff/ACOUSTIC/GRIDDED/out/S2024204001_sv.zarr'

freqs=[38000, 200000]
print(f)
data=xr.open_dataset(f,engine="zarr")

# Select a subset for testing
dataSel=data.sv.sel(frequency=freqs,ping_time=slice("2024-02-21 05:00:00","2024-02-21 05:30:00"))

# What's the best way to resample / coarsen prior to dB differencing and other operations in xarray????
#dataSelResamp=dataSel.resample(ping_time="1min").mean(dim=["ping_time"]).coarsen(range=1, boundary="trim").mean()

# That didn't work...

# Calculate the difference between the frequencies 38 and 200
dB_diff = 10*np.log10(dataSel.sel(frequency=freqs[1])) - 10*np.log10(dataSel.sel(frequency=freqs[0]))

# Set min and max for visualization of Sv
vmin=-82
vmax=-30

# Select 38 kHz data and plot
dB_38000=10*np.log10(dataSel.sel(frequency=38000))

fig, ax = plt.subplots(figsize=(10, 6))
dB_38000.plot.pcolormesh(x='ping_time', y='range', ax=ax, cmap='viridis', vmin=vmin, vmax=vmax)
ax.set_title('Sv at 38000 Hz')
ax.set_xlabel('Time')
ax.set_ylabel('Range (m)')
ax.set_ylim(0,250)
ax.invert_yaxis()
plt.show()

# Plot dB diff
fig, ax = plt.subplots(figsize=(10, 6))
dB_diff.plot.pcolormesh(x='ping_time', y='range', ax=ax, cmap='viridis')
ax.set_title('dB difference / 38-200')
ax.set_xlabel('Time')
ax.set_ylabel('Range (m)')
ax.set_ylim(0,250)
ax.invert_yaxis()
plt.show()

# Plot with min/max dBdiff values
vmin=0
vmax=10

fig, ax = plt.subplots(figsize=(10, 6))
dB_diff.plot.pcolormesh(x='ping_time', y='range', ax=ax, cmap='viridis',vmin=vmin, vmax=vmax)
ax.set_title('dB difference / 38-200')
ax.set_xlabel('Time')
ax.set_ylabel('Range (m)')
ax.set_ylim(0,250)
ax.invert_yaxis()
plt.show()

# Cut bellow a set threshold
vmax=10

fig, ax = plt.subplots(figsize=(10, 6))
dB_diff.where(dB_diff<=vmax).plot.pcolormesh(x='ping_time', y='range', ax=ax, cmap='viridis')
ax.set_title('dB difference / 38-200')
ax.set_xlabel('Time')
ax.set_ylabel('Range (m)')
ax.set_ylim(0,250)
ax.invert_yaxis()
plt.show()  