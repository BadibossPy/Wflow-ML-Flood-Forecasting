"""Verify Wflow Niger model files"""
import xarray as xr
from pathlib import Path

model_dir = Path('models/wflow_sbm/wflow_niger')

print('=== WFLOW NIGER MODEL FILES ===')
print()

# Static maps
print('1. STATIC MAPS (staticmaps.nc):')
ds = xr.open_dataset(model_dir / 'staticmaps.nc')
print(f'   Grid: {ds.dims}')
print(f'   Variables: {list(ds.data_vars)}')
print(f'   DEM range: {float(ds.wflow_dem.min()):.0f} - {float(ds.wflow_dem.max()):.0f} m')
print()

# Forcing
print('2. FORCING DATA (inmaps.nc):')
ds_f = xr.open_dataset(model_dir / 'inmaps.nc')
print(f'   Time: {ds_f.time.values[0]} to {ds_f.time.values[-1]}')
print(f'   Timesteps: {len(ds_f.time)}')
print(f'   Variables: {list(ds_f.data_vars)}')
print()

# LAI
print('3. LAI CYCLIC (cyclic_lai.nc):')
ds_l = xr.open_dataset(model_dir / 'cyclic_lai.nc')
print(f'   Months: {len(ds_l.time)}')
print(f'   LAI range: {float(ds_l.LAI.min()):.1f} - {float(ds_l.LAI.max()):.1f}')
print()

# Config
print('4. CONFIGURATION (wflow_sbm.toml):')
with open(model_dir / 'wflow_sbm.toml') as f:
    for i, line in enumerate(f):
        if i < 10:
            print(f'   {line.rstrip()}')
print()

print('=== MODEL READY FOR SIMULATION ===')
print()
print('To run (requires Julia + Wflow.jl):')
print('  cd models/wflow_sbm/wflow_niger')
print('  julia -e "using Wflow; Wflow.run(\\"wflow_sbm.toml\\")"')

