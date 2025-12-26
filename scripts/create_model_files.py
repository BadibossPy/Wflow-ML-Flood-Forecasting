"""
Create Wflow model files for Niger Basin
Resamples static maps to match ERA5 grid for consistency
"""
from pathlib import Path
import numpy as np
import xarray as xr
from scipy.interpolate import RegularGridInterpolator

# Paths
MODEL_DIR = Path('models/wflow_sbm/wflow_niger')
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Load ERA5 (smaller grid - use this as reference)
forcing_path = Path('data/processed/era5_niger_daily_wflow_fixed.nc')
ds_era5 = xr.open_dataset(forcing_path)

lat = ds_era5.latitude.values
lon = ds_era5.longitude.values
time = ds_era5.time.values

print(f'ERA5 grid: {len(lat)}x{len(lon)}')
print(f'Time: {time[0]} to {time[-1]}')

# Load static maps
static_path = Path('data/static/staticmaps_niger.nc')
ds_static = xr.open_dataset(static_path)

y_old = ds_static.y.values
x_old = ds_static.x.values

def resample_to_era5(data, y_old, x_old, lat_new, lon_new, fill_value=np.nan):
    data_float = data.astype('float64')
    interp = RegularGridInterpolator((y_old, x_old), data_float, method='nearest', bounds_error=False, fill_value=fill_value)
    lon_grid, lat_grid = np.meshgrid(lon_new, lat_new)
    points = np.column_stack([lat_grid.ravel(), lon_grid.ravel()])
    return interp(points).reshape(len(lat_new), len(lon_new))

print('Resampling static maps...')

dem_rs = resample_to_era5(ds_static['wflow_dem'].values, y_old, x_old, lat, lon, fill_value=500.0)
ldd_rs = resample_to_era5(ds_static['wflow_ldd'].values, y_old, x_old, lat, lon, fill_value=5.0)
river_rs = resample_to_era5(ds_static['wflow_river'].values, y_old, x_old, lat, lon, fill_value=0.0)
slope_rs = resample_to_era5(ds_static['Slope'].values, y_old, x_old, lat, lon, fill_value=0.01)
uparea_rs = resample_to_era5(ds_static['wflow_uparea'].values, y_old, x_old, lat, lon, fill_value=1.0)

# Fill NaN
dem_rs = np.nan_to_num(dem_rs, nan=500.0).astype('float32')
ldd_rs = np.nan_to_num(ldd_rs, nan=5).astype('uint8')
river_rs = np.nan_to_num(river_rs, nan=0).astype('uint8')
slope_rs = np.nan_to_num(slope_rs, nan=0.01).astype('float32')
uparea_rs = np.nan_to_num(uparea_rs, nan=1.0).astype('float32')

# Subcatchment
subcatch = np.ones((len(lat), len(lon)), dtype='int32')

# Create staticmaps.nc
print('Creating staticmaps.nc...')
ds_out = xr.Dataset({
    'wflow_dem': (['y', 'x'], dem_rs),
    'wflow_ldd': (['y', 'x'], ldd_rs),
    'wflow_river': (['y', 'x'], river_rs),
    'wflow_subcatch': (['y', 'x'], subcatch),
    'wflow_uparea': (['y', 'x'], uparea_rs),
    'Slope': (['y', 'x'], slope_rs),
    'N': (['y', 'x'], np.full_like(dem_rs, 0.072)),
    'SoilThickness': (['y', 'x'], np.full_like(dem_rs, 2000.0)),
    'KsatVer': (['y', 'x'], np.full_like(dem_rs, 5.0)),
    'thetaS': (['y', 'x'], np.full_like(dem_rs, 0.45)),
    'thetaR': (['y', 'x'], np.full_like(dem_rs, 0.05)),
}, coords={'y': lat, 'x': lon})
ds_out.to_netcdf(MODEL_DIR / 'staticmaps.nc')
print(f'Saved: staticmaps.nc')

# Create inmaps.nc
print('Creating inmaps.nc...')
ds_forcing = xr.Dataset({
    'precip': (['time', 'y', 'x'], ds_era5['precip'].values),
    'temp': (['time', 'y', 'x'], ds_era5['temp'].values),
    'pet': (['time', 'y', 'x'], ds_era5['pet'].values),
}, coords={'time': time, 'y': lat, 'x': lon})
ds_forcing.to_netcdf(MODEL_DIR / 'inmaps.nc')
print(f'Saved: inmaps.nc')

# Create LAI cyclic
print('Creating LAI...')
lai_path = Path('data/static/lai_niger.nc')
ds_lai = xr.open_dataset(lai_path)
lai_rs = np.zeros((12, len(lat), len(lon)), dtype='float32')
for i in range(12):
    lai_rs[i] = resample_to_era5(ds_lai['LAI'].values[i], ds_lai.y.values, ds_lai.x.values, lat, lon)
lai_rs = np.nan_to_num(lai_rs, nan=1.5)

ds_lai_out = xr.Dataset({
    'LAI': (['time', 'y', 'x'], lai_rs)
}, coords={'time': np.arange(1, 13), 'y': lat, 'x': lon})
ds_lai_out.to_netcdf(MODEL_DIR / 'cyclic_lai.nc')
print(f'Saved: cyclic_lai.nc')

print('\nModel files ready!')

