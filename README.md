# Wflow-ML-Flood-Forecasting

## Overview
A physics-informed hydrological forecasting system for the Upper Niger Basin, integrating **Wflow SBM** (physically-based hydrology) with **Machine Learning** for flood prediction. This project is the workflow from data acquisition to discharge modeling.

## Project Architecture
The repository is structured to separate data processing, physical modeling, and analysis:

```
Wflow-ML-Flood-Forecasting/
├── data/
│   ├── raw/                 # ERA5 NetCDF files (not tracked)
│   └── processed/           # Wflow-ready forcing and ML features
├── notebooks/
│   ├── 01_data_acquisition.ipynb    # ERA5-Land retrieval & processing 
│   ├── 02_wflow_build.ipynb         # HydroMT model construction
│   └── 03_ml_forecast.ipynb         # Hybrid forecasting model
├── src/                     # Core python modules
├── models/                  # Wflow configuration & ML checkpoints
└── environment.yml          # Reproducible environment definition
```

## Core Components

### 1. Data Acquisition (ERA5-Land)
- **Source:** Copernicus Climate Data Store (CDS)
- **Method:** Optimized parallel retrieval using `cdsapi` with unarchived NetCDF handling.
- **Processing:** physical unit conversion (SI to Hydrological), temporal aggregation (Hourly to Daily), and water balance validation (Precipitation, PET, Soil Moisture).

### 2. Hydrological Modeling (Wflow SBM)
*(In Progress)*
- **Engine:** Wflow.jl (Kinematic wave, distributed)
- **Setup:** HydroMT for automated mesh generation and parameterization.

### 3. Machine Learning Forecast
*(In Progress)*
- **Goal:** Predict flood thresholds using rainfall features and antecedent moisture.

## Usage
1. **Environment Setup:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Data Acquisition:**
   Run `notebooks/01_data_acquisition.ipynb` to download and process the forcing data.

