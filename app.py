from flask import Flask, render_template, request
import pickle
import numpy as np
import joblib
app = Flask(__name__)


# Load the trained model (adjust the path if necessary)
try:
    model = joblib.load("model.pkl")
    print("Model load successfully")
except Exception as e:
    print(f"Error loading models: {e}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    Diesel=0
    Petrol=0
    CNG=0
    LPG=0
    First_Owner = 0
    Second_Owner = 0
    Third_Owner = 0
    Fourth_and_Above_Owner = 0
    Test_Drive_Car = 0
    if request.method == "POST":
        try:
            # Collect input data from the form
            name = request.form["name"]
            year = int(request.form["year"])
            km_driven = int(request.form["km_driven"])
            fuel = request.form["fuel"]
            if fuel=="Diesel":
                Diesel=1
            elif fuel=="Petrol":
                Petrol=1
            elif fuel=="CNG":
                CNG=1
            else:
                LPG=1
            seller_type = request.form["seller_type"]
            if seller_type=="Individual":
                seller=1
            else:
                seller=0
            transmission = request.form["transmission"]
            if transmission=="Individual":
                transmission=1
            else:
                transmission=0
            owner = request.form["owner"]
            if owner == "First Owner":
                First_Owner = 1
            elif owner == "Second Owner":
                Second_Owner = 1
            elif owner == "Third Owner":
                Third_Owner = 1
            elif owner == "Fourth & Above Owner":
                Fourth_and_Above_Owner = 1
            elif owner == "Test Drive Car":
                Test_Drive_Car = 1
            seats = int(request.form["seats"])
            torque = float(request.form["torque"])
            max_power = float(request.form["max_power"])
            engine_cc = float(request.form["engine_cc"])
            mileage = float(request.form["mileage"])

            # Create input array for prediction
            input_data = np.array([[year, km_driven,seller,transmission, seats, torque, max_power, engine_cc, mileage,First_Owner, Fourth_and_Above_Owner,Second_Owner,Test_Drive_Car,Third_Owner,CNG,Diesel,LPG,Petrol]])

            # Use the model to predict
            prediction = model.predict(input_data)
            return render_template(
                "result.html",
                name=name,
                prediction=round(prediction[0], 2),
            )
        except Exception as e:
            return f"Error in prediction: {e}"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
