import xarray as xr
import numpy as np
import pandas as pd
import joblib

model = joblib.load("cyclone_wind_model.pkl")


def extract_features(nc_file):

    ds = xr.open_dataset(nc_file)
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


def predict_wind(nc_file):

    features = extract_features(nc_file)

    print("Features Shape:", features.shape)

    print("Columns:", features.columns.tolist())

    prediction = model.predict(features)

    return prediction[0]