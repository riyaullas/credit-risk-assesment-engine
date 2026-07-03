import joblib
import pandas as pd

model = joblib.load("models/loan_approval_model.pkl")

sample = pd.DataFrame({
    "Gender":[1],
    "Married":[1],
    "Dependents":[0],
    "Education":[0],
    "Self_Employed":[0],
    "ApplicantIncome":[5000],
    "CoapplicantIncome":[0],
    "LoanAmount":[120],
    "Loan_Amount_Term":[360],
    "Credit_History":[1],
    "Property_Area":[2]
})

prediction = model.predict(sample)

print(prediction)