# Wflow-ML-Flood-Forecasting

## Overview
A physics-informed hydrological forecasting system for the Upper Niger Basin, integrating **Wflow SBM** (physically-based hydrology) with **Machine Learning** for flood prediction.

## Project Structure

```
Wflow-ML-Flood-Forecasting/
├── data/
│   ├── raw/                          # ERA5 NetCDF files (gitignored)
│   └── processed/                    # Wflow-ready daily forcing
├── notebooks/
│   ├── 01_data_acquisition.ipynb     # ERA5-Land retrieval & processing
│   ├── 02_wflow_model_build.ipynb    # HydroMT model construction
│   └── 03_ml_forecast.ipynb          # ML flood forecasting (TBD)
├── models/
│   └── wflow_sbm/
│       ├── wflow_build.yml           # HydroMT build configuration
│       ├── hydromt_data.yml          # Data catalog (ERA5 forcing)
│       └── run_wflow.jl              # Julia simulation runner
├── src/                              # Python modules (TBD)
└── requirements.txt
```

## Notebooks

| Notebook | Description | Status |
|----------|-------------|--------|
| `01_data_acquisition` | ERA5-Land download, unit conversion, daily aggregation | ✅ Complete |
| `02_wflow_model_build` | HydroMT model setup, static maps, forcing preparation | ✅ Complete |
| `03_ml_forecast` | ML-based flood threshold prediction | 🔄 In Progress |

## Dependencies

**Python:**
```bash
pip install -r requirements.txt
```

**Julia (for Wflow simulation):**
```julia
using Pkg
Pkg.add("Wflow")
```

## Usage

1. **Data Acquisition:** Run `01_data_acquisition.ipynb` to download ERA5-Land forcing
2. **Model Build:** Run `02_wflow_model_build.ipynb` to construct the Wflow model
3. **Simulation:** Execute Julia script:
   ```bash
   julia models/wflow_sbm/run_wflow.jl models/wflow_sbm/wflow_niger/wflow_sbm.toml
   ```

## Study Area
Upper Niger Basin (Guinea/Mali) — a monsoon-driven tropical catchment with strong seasonal rainfall variability.

