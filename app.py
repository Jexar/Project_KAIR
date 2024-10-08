import streamlit as st
import pandas as pd
import datetime
from welcome_page import show_welcome_page

st.set_page_config(page_title="Clinical Decision Support System", layout="wide", initial_sidebar_state="collapsed")

@st.cache_data
def load_drug_data():
   return pd.read_csv("drug_data.csv")

@st.cache_data
def load_patient_data():
   return pd.read_csv('patient_info.csv')

@st.cache_data
def load_interaction_data():
   return pd.read_csv("interaction_data.csv")

@st.cache_data
def load_household_interaction_data():
   return pd.read_csv("household_interaction_data.csv")

df = load_patient_data()
drug_data = load_drug_data()
interaction_data = load_interaction_data()
household_interaction_data = load_household_interaction_data()

def doctor_app():
    st.title("Clinical Decision Support System")

    # Patient Information
    st.header("Patient Information")
    name = st.text_input("Enter your patient's name:")
    
    current_medications = []  # Initialize as an empty list

    if name:
        person = df[df['Name'].str.lower() == name.lower()]
        if not person.empty:
            person = person.iloc[0]  # Get the first (and should be only) matching row
            dob = pd.to_datetime(person['DateOfBirth'])
            weight = person['Weight']

            st.write(f"Date of Birth: {dob.strftime('%B %d, %Y')}")
            
            # Calculate and display age
            today = datetime.date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            st.write(f"Age: {age} years")
            
            # Display weight
            st.write(f"Weight: {weight} lbs")

            # Display current medications
            if 'CurrentMedications' in person:
                current_medications_str = person['CurrentMedications']
                st.write("Current Medications:")
                if pd.notna(current_medications_str) and current_medications_str != '':
                    current_medications = [med.strip() for med in current_medications_str.split(',')]
                    for med in current_medications:
                        st.write(f"- {med}")
                else:
                    st.write("No current medications recorded.")
            else:
                st.write("Current medications information not available.")

            # Allow updating weight
            new_weight = st.number_input("Update weight (lbs):", min_value=0.0, max_value=5000.0, step=0.1, value=float(weight))
            if new_weight != weight:
                st.write(f"Updated weight: {new_weight} lbs")
                # In a real application, you would update the database here
        else:
            st.write("Person not found in the database.")
    
    # Medication Selection
    st.header("Medication Selection")
    all_drugs = drug_data['drug_name'].tolist()
    
    # Pre-select current medications
    default_selected = [drug for drug in current_medications if drug in all_drugs]
    
    selected_drugs = st.multiselect("Select medications", all_drugs, default=default_selected)

    if st.button("Check Interactions and Dosage"):
        if name and not person.empty:
            check_interactions(selected_drugs)
            recommend_dosage(selected_drugs, age, new_weight)
        else:
            st.warning("Please enter valid patient information before checking interactions and dosage.")

def check_interactions(selected_drugs):
   st.subheader("Drug Interactions")
   interactions = []
   for i, drug1 in enumerate(selected_drugs):
       for drug2 in selected_drugs[i+1:]:
           interaction = interaction_data[(interaction_data['drug1'] == drug1) & (interaction_data['drug2'] == drug2)]
           if not interaction.empty:
               interactions.append(f"{drug1} - {drug2}: {interaction['interaction'].values[0]}")
  
   if interactions:
       for interaction in interactions:
           st.warning(interaction)
   else:
       st.success("No known interactions found.")

def recommend_dosage(selected_drugs, age, weight):
   st.subheader("Dosage Recommendations")
   for drug in selected_drugs:
       drug_info = drug_data[drug_data['drug_name'] == drug].iloc[0]
       base_dosage = drug_info['base_dosage']
      
       # Simple dosage adjustment based on age and weight
       if age > 65:
           adjusted_dosage = base_dosage * 0.8
       elif weight < 90:
           adjusted_dosage = base_dosage * 0.9
       else:
           adjusted_dosage = base_dosage
      
       st.info(f"{drug}: Recommended dosage is {adjusted_dosage:.2f} mg")

def patient_app():
    st.title("Clinical Decision Support System - Patient View")
    
    # Patient Information
    st.header("Your Information")
    name = st.text_input("Enter your name:")
    
    if name:
        person = df[df['Name'].str.lower() == name.lower()]
        if not person.empty:
            person = person.iloc[0]
            dob = pd.to_datetime(person['DateOfBirth'])
            weight = person['Weight']

            st.write(f"Date of Birth: {dob.strftime('%B %d, %Y')}")
            
            today = datetime.date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            st.write(f"Age: {age} years")
            
            st.write(f"Weight: {weight} lbs")

            if 'CurrentMedications' in person:
                current_medications_str = person['CurrentMedications']
                st.write("Your Current Medications:")
                if pd.notna(current_medications_str) and current_medications_str != '':
                    current_medications = [med.strip() for med in current_medications_str.split(',')]
                    for med in current_medications:
                        st.write(f"- {med}")
                else:
                    st.write("No current medications recorded.")
            else:
                st.write("Current medications information not available.")

            # Household Item Interactions
            st.header("Household Item Interactions")
            household_items = household_interaction_data['item'].unique().tolist()
            selected_items = st.multiselect("Select household items you commonly use:", household_items)

            if selected_items:
                st.subheader("Potential Interactions:")
                for med in current_medications:
                    for item in selected_items:
                        interaction = household_interaction_data[
                            (household_interaction_data['drug'] == med) & 
                            (household_interaction_data['item'] == item)
                        ]
                        if not interaction.empty:
                            st.warning(f"{med} - {item}: {interaction['interaction'].values[0]}")
            else:
                st.info("Select household items to check for potential interactions with your medications.")
        else:
            st.write("Person not found in the database.")

def main_app():
    if st.session_state.user_role == "doctor":
        doctor_app()
    elif st.session_state.user_role == "patient":
        patient_app()

def app():
    if 'page' not in st.session_state:
        st.session_state.page = "welcome"
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None

    if st.session_state.page == "welcome":
        show_welcome_page()
    elif st.session_state.page == "main":
        main_app()

if __name__ == "__main__":
   app()
