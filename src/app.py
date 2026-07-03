import streamlit as st
import joblib
import pandas as pd

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Credit Risk Assessment Engine",
    page_icon="🏦",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.big-title {
    text-align: center;
    font-size: 48px;
    font-weight: 800;
    color: #4CAF50;
}

.sub-title {
    text-align: center;
    color: #B0B0B0;
    font-size: 18px;
    margin-bottom: 30px;
}

.stButton > button {
    width: 100%;
    height: 60px;
    font-size: 20px;
    font-weight: bold;
    border-radius: 12px;
    background-color: #4CAF50;
}

.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD MODEL
# ==================================================
try:
    model = joblib.load("models/loan_approval_model.pkl")
except Exception as e:
    st.error(f"Error loading model:{e}")
    st.stop()

# ==================================================
# HEADER
# ==================================================

st.markdown("""
<div class="big-title">
🏦 Credit Risk Assessment Engine
</div>

<div class="sub-title">
AI-Powered Loan Approval & Credit Risk Prediction
</div>
""", unsafe_allow_html=True)

# ==================================================
# DASHBOARD METRICS
# ==================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
📊 Dataset Size

# 614
""")

with col2:
    st.success("""
⚙️ Features

# 11
""")

with col3:
    st.warning("""
🎯 Best Accuracy

# 78.86%
""")


st.divider()

# ==================================================
# FORM
# ==================================================

st.subheader("📋 Applicant Information")

col1, col2 = st.columns(2)

with col1:

    gender = st.selectbox(
        "Gender",
        ["Male", "Female"]
    )

    married = st.selectbox(
        "Married",
        ["No", "Yes"]
    )

    education = st.selectbox(
        "Education",
        ["Graduate", "Not Graduate"]
    )

    self_employed = st.selectbox(
        "Self Employed",
        ["No", "Yes"]
    )

    credit_history = st.selectbox(
        "Credit History",
        ["Bad Credit History", "Good Credit History"]
    )

with col2:

    dependents = st.selectbox(
        "Dependents",
        [0, 1, 2, 3]
    )

    property_area = st.selectbox(
        "Property Area",
        ["Rural", "Semiurban", "Urban"]
    )

    applicant_income = st.number_input(
        "Applicant Income",
        min_value=0,
        value=5000
    )

    coapplicant_income = st.number_input(
        "Coapplicant Income",
        min_value=0,
        value=0
    )

    loan_amount = st.number_input(
        "Loan Amount",
        min_value=0,
        value=120
    )

loan_term = st.slider(
    "Loan Amount Term (Months)",
    min_value=12,
    max_value=480,
    value=360
)

# ==================================================
# ENCODING
# ==================================================

gender = 1 if gender == "Male" else 0

married = 1 if married == "Yes" else 0

education = 0 if education == "Graduate" else 1

self_employed = 1 if self_employed == "Yes" else 0

credit_history = 1 if credit_history == "Good Credit History" else 0

property_area_map = {
    "Rural": 0,
    "Semiurban": 1,
    "Urban": 2
}

property_area = property_area_map[property_area]

# ==================================================
# PREDICT BUTTON
# ==================================================

if st.button("🔍 Predict Loan Approval"):

    sample = pd.DataFrame({
        "Gender": [gender],
        "Married": [married],
        "Dependents": [dependents],
        "Education": [education],
        "Self_Employed": [self_employed],
        "ApplicantIncome": [applicant_income],
        "CoapplicantIncome": [coapplicant_income],
        "LoanAmount": [loan_amount],
        "Loan_Amount_Term": [loan_term],
        "Credit_History": [credit_history],
        "Property_Area": [property_area]
    })
    
    try:
        prediction = model.predict(sample)
    except Exception as e:
        st.error(f"Prediction Error: {e}")  
        st.stop()  

    try:
        probability = model.predict_proba(sample)[0][1]
        approval_score = round(probability * 100, 2)
    except Exception as e:
        st.error(e)
        approval_score = 0

    st.divider()

    st.subheader("📈 Risk Assessment")

    st.progress(int(approval_score))

    st.metric(
        label="Approval Score",
        value=f"{approval_score}%"
    )

    if prediction[0] == 1:

        st.success("🎉 Congratulations! Loan Approved")

        st.markdown("""
### ✅ Decision Summary

- Credit profile acceptable
- Income profile satisfactory
- Risk level is LOW
- Application meets approval criteria
        """)

        st.balloons()

    else:

        st.error("⚠️ Loan Not Approved")

        st.markdown("""
### ❌ Decision Summary

- Risk level is HIGH
- Credit profile needs improvement
- Application does not satisfy approval criteria
- Reassessment recommended
        """)

# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "Built using Python • Scikit-Learn • Logistic Regression • Streamlit"
)