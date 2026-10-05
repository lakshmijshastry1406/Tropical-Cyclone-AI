import xarray as xr
import numpy as np
import pandas as pd
import joblib
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

model = joblib.load("cyclone_wind_model.pkl")


def extract_features(nc_file):

    ds = xr.open_dataset(nc_file)
    print("Dataset Dimensions:")
    print(ds.dims)
    print("Variables inside file:")
    print(list(ds.data_vars))

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
def generate_satellite_image(nc_file):

    ds = xr.open_dataset(nc_file)

    print("Available Variables:")
    print(list(ds.data_vars))
    variable = "ssmis_91h"

    data = ds[variable].values

    print("Shape:", data.shape)

    print("Dimensions:", data.ndim) 

    plt.figure(figsize=(6,6))
    plt.imshow(data, aspect='auto')
    plt.colorbar()
    plt.title(variable)

    image_path = "static/images/latest_satellite.png"

    plt.savefig(image_path)

    plt.close()

    ds.close()

    return image_path


def predict_wind(nc_file):

    features = extract_features(nc_file)

    print("Features Shape:", features.shape)

    print("Columns:", features.columns.tolist())

    prediction = model.predict(features)

    return prediction[0]