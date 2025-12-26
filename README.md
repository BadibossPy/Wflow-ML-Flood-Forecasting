# Wflow-ML-Flood-Forecasting

## Overview
A physics-informed hydrological forecasting system for the **Upper Niger Basin**, integrating Wflow SBM with Machine Learning for flood prediction.

## Project Structure
```
Wflow-ML-Flood-Forecasting/
├── data/
│   ├── static/              # DEM, flow direction, slope (from SRTM)
│   └── processed/           # ERA5 daily forcing
├── notebooks/
│   ├── 00_static_data_acquisition.ipynb  # Download SRTM, derive LDD
│   ├── 01_data_acquisition.ipynb         # ERA5-Land forcing
│   └── 02_wflow_model_build.ipynb        # Model inspection
├── models/wflow_sbm/wflow_niger/
│   ├── staticmaps.nc        # Static model parameters
│   ├── inmaps.nc            # ERA5 forcing (precip, temp, PET)
│   ├── cyclic_lai.nc        # Monthly LAI climatology
│   └── wflow_sbm.toml       # Wflow configuration
├── scripts/
│   ├── create_model_files.py
│   └── verify_model.py
└── requirements.txt
```

## Model Domain
- **Region:** Upper Niger Basin (Guinea/Mali)
- **Bbox:** [-10.5°, 9.5°, -6.5°, 13.0°]
- **Resolution:** 0.1° (~10 km)
- **Period:** 2019-01-01 to 2020-02-29

## Data Sources
| Dataset | Source | Resolution |
|---------|--------|------------|
| DEM | CGIAR SRTM 90m | 90m |
| Flow Direction | Derived (pyflwdir) | 0.1° |
| Forcing | ERA5-Land | 0.1° daily |
| LAI | Synthetic climatology | Monthly |

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Download Static Data
Run `notebooks/00_static_data_acquisition.ipynb` or:
```bash
python scripts/create_model_files.py
```

### 3. Run Wflow Simulation
Requires Julia + Wflow.jl:
```bash
cd models/wflow_sbm/wflow_niger
julia -e "using Wflow; Wflow.run(\"wflow_sbm.toml\")"
```

## Notebooks
| # | Notebook | Description |
|---|----------|-------------|
| 00 | `00_static_data_acquisition` | Download SRTM, derive flow direction |
| 01 | `01_data_acquisition` | ERA5-Land forcing download |
| 02 | `02_wflow_model_build` | Model inspection and visualization |

## Model Configuration
- **Type:** Wflow SBM (Soil-Bucket Model)
- **Routing:** Kinematic wave
- **Timestep:** Daily (86400 s)
- **Snow:** Disabled (tropical region)

## Output Variables
- `q_river`: River discharge (m³/s)
- `satwaterdepth`: Saturated zone depth
- `ustorelayerdepth`: Unsaturated storage
