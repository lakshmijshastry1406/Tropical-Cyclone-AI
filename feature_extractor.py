import xarray as xr
import numpy as np
import pandas as pd


def extract_features(nc_file):

    ds = xr.open_dataset(nc_file)

    features = {}

    for variable in ds.data_vars:

        if variable.startswith("ssmis"):

            data = ds[variable].values

            features[variable + "_mean"] = np.mean(data)
            features[variable + "_std"] = np.std(data)
            features[variable + "_min"] = np.min(data)
            features[variable + "_max"] = np.max(data)

    ds.close()

    return pd.DataFrame([features])