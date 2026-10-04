from flask import Flask, render_template, request, jsonify
from predict import predict_wind
import os

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

    try:
        wind_speed = predict_wind(filepath)
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

    return jsonify({
        "predicted_wind": round(float(wind_speed), 2),
        "category": category
    })

if __name__ == "__main__":
    app.run(debug=True)