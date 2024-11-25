import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

def generate_dietary_plan(medical_condition):
    """
    Generate a dietary plan based on the patient's medical needs.
    """
    dietary_plan = []

    if medical_condition == "Diabetes" or medical_condition == "Both":
        dietary_plan.append({
            "category": "Diabetes Management",
            "recommendations": [
                "Low Glycemic Index foods (e.g., whole grains, lentils)",
                "Avoid refined sugars and sugary drinks",
                "Include high-fiber vegetables (e.g., broccoli, spinach)",
                "Lean proteins (e.g., chicken, tofu, fish)"
            ]
        })
    if medical_condition == "Cardiovascular Disease" or medical_condition == "Both":
        dietary_plan.append({
            "category": "Heart Health",
            "recommendations": [
                "Low saturated fats (e.g., olive oil, nuts)",
                "Increase omega-3 fatty acids (e.g., salmon, chia seeds)",
                "Limit sodium intake",
                "Include whole grains and legumes"
            ]
        })

    if not dietary_plan:
        dietary_plan.append({
            "category": "General Health",
            "recommendations": [
                "Balanced diet with fruits, vegetables, whole grains",
                "Lean proteins",
                "Plenty of water"
            ]
        })

    return dietary_plan

def calculate_bmi(weight, height):
    """Calculate BMI"""
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 1)

def get_bmi_category(bmi):
    """Determine BMI category"""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

st.set_page_config(
    page_title="Personalized Nutrition Dashboard", 
    page_icon="🥗", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .reportview-container {
        background-color: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🥗 Personalized Nutrition Dashboard")
    
    with st.sidebar:
        st.header("Patient Details")
        patient_name = st.text_input("Patient Name", placeholder="Enter patient name")
        age = st.number_input("Age", min_value=0, max_value=120, value=30, step=1)
        weight = st.number_input("Weight (kg)", min_value=0.0, value=70.0, step=0.1)
        height = st.number_input("Height (cm)", min_value=0.0, value=170.0, step=0.1)
        
        medical_condition = st.radio(
            "Medical Condition",
            ("Diabetes", "Cardiovascular Disease", "Both", "None"),
            key="medical_condition"
        )
        
        generate_button = st.button("Generate Personalized Plan", type="primary")

    if generate_button:
        bmi = calculate_bmi(weight, height)
        bmi_category = get_bmi_category(bmi)

        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Patient Name", patient_name)
        
        with col2:
            st.metric("BMI", f"{bmi} ({bmi_category})")
        
        with col3:
            st.metric("Medical Condition", medical_condition)

        st.header("Personalized Dietary Recommendations")
        
        dietary_plan = generate_dietary_plan(medical_condition)
        
        for plan in dietary_plan:
            with st.expander(f"{plan['category']} Recommendations"):
                for recommendation in plan['recommendations']:
                    st.write(f"- {recommendation}")

        st.header("Nutritional Insights")
        
        focus_data = pd.DataFrame({
            "Aspect": ["Carbohydrate Control", "Protein Intake", "Healthy Fats", "Fiber"],
            "Importance": [30, 25, 25, 20]
        })
        
        fig = px.pie(
            focus_data, 
            values='Importance', 
            names='Aspect', 
            title='Dietary Focus Distribution'
        )
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()