import streamlit as st
import pandas as pd

# Load mock data (in a real scenario, this would come from an API or database)
@st.cache_data
def load_drug_data():
    return pd.read_csv("drug_data.csv")

@st.cache_data
def load_interaction_data():
    return pd.read_csv("interaction_data.csv")

drug_data = load_drug_data()
interaction_data = load_interaction_data()

def main():
    st.title("Clinical Decision Support System")

    # Patient Information
    st.header("Patient Information")
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
    weight = st.number_input("Weight (lbs)", min_value=0.0, max_value=300.0, value=70.0)
    
    # Medication Selection
    st.header("Medication Selection")
    selected_drugs = st.multiselect("Select medications", drug_data['drug_name'].tolist())

    if st.button("Check Interactions and Dosage"):
        check_interactions(selected_drugs)
        recommend_dosage(selected_drugs, age, weight)

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
        elif weight < 50:
            adjusted_dosage = base_dosage * 0.9
        else:
            adjusted_dosage = base_dosage
        
        st.info(f"{drug}: Recommended dosage is {adjusted_dosage:.2f} mg")

if __name__ == "__main__":
    main()
