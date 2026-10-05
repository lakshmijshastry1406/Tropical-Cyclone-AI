from flask import Flask, render_template, request, jsonify
from predict import predict_wind, generate_satellite_image
import os
import pandas as pd

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    file = request.files["file"]

    filepath = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )
    file.save(filepath)

    image_path = generate_satellite_image(filepath)

    try:
        wind_speed = predict_wind(filepath)

        confidence = round(
            min(
                95,
            max(
                70,
                100 - abs(wind_speed - 60) / 3
            )
        ),
        1
    )
    except Exception as e:
        print("ERROR:", e)
        raise

    if wind_speed < 34:
        category = "Tropical Depression"

    elif wind_speed < 48:
        category = "Deep Depression"

    elif wind_speed < 64:
        category = "Cyclonic Storm"

    elif wind_speed < 90:
        category = "Severe Cyclonic Storm"

    else:
        category = "Very Severe Cyclonic Storm"
        log = pd.DataFrame([{
    "file": file.filename,
    "wind_speed": float(wind_speed),
    "category": category
}])

        try:
            old = pd.read_csv("prediction_log.csv")
            log = pd.concat([old, log])
        except:
            pass

        log.to_csv(
            "prediction_log.csv",
            index=False
        )

    return jsonify({
    "predicted_wind": round(float(wind_speed), 2),
    "category": category,
    "confidence": confidence
})

if __name__ == "__main__":
    app.run(debug=True)