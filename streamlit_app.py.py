import streamlit as st
import pandas as pd
import os

# File ka naam (ensure karein ke CSV file isi folder mein ho)
FILE_NAME = "ACAG Portal Data.csv"

st.set_page_config(page_title="ACAG Portal", layout="centered")

st.title("?? ACAG CNIC Search Portal")

# Data Load Karne ka Function
@st.cache_data # Isse website fast load hogi
def load_data():
    if os.path.exists(FILE_NAME):
        # Column names ko CSV ke mutabiq handle karna
        df = pd.read_csv(FILE_NAME, dtype=str)
        return df
    else:
        return pd.DataFrame(columns=["ApplicantCNIC", "ApplicantName", "Batch No."])

df = load_data()

menu = st.sidebar.selectbox("Menu", ["Search Record", "Add New Record"])

# ---------------- SEARCH SECTION -----------------
if menu == "Search Record":
    st.header("?? Record Search")
    st.info("CNIC enter karein (Bina dashes ke)")

    search_cnic = st.text_input("CNIC Number Likhein")

    if search_cnic:
        # Data mein search karna (Scientific notation handle karne ke liye)
        result = df[df["ApplicantCNIC"].str.contains(search_cnic, na=False)]
        
        if not result.empty:
            for index, row in result.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div style="background-color:#f0f2f6; padding:15px; border-radius:10px; border-left:5px solid #ff4b4b; margin-bottom:10px;">
                        <h3 style="margin:0;">?? {row['ApplicantName']}</h3>
                        <p style="margin:5px 0;"><b>CNIC:</b> {row['ApplicantCNIC']}</p>
                        <p style="margin:0;"><b>Batch:</b> <span style="color:green;">{row['Batch No.']}</span></p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.error("Afsos! Is CNIC ka koi record nahi mila.")

# ---------------- ADD RECORD SECTION -----------------
if menu == "Add New Record":
    st.header("? New Data Add Karein")
    with st.form("addform", clear_on_submit=True):
        cnic = st.text_input("CNIC")
        name = st.text_input("Name")
        batch = st.text_input("Batch No.")
        submit = st.form_submit_button("Save Record")

        if submit:
            new_data = pd.DataFrame([[cnic, name, batch]], columns=["ApplicantCNIC", "ApplicantName", "Batch No."])
            new_data.to_csv(FILE_NAME, mode='a', header=not os.path.exists(FILE_NAME), index=False)
            st.success("Data kamyabi se save ho gaya!")
            st.cache_data.clear() # Data refresh karne ke liye