import streamlit as st
import sqlite3
import datetime

# Database setup
conn = sqlite3.connect('safety_pro.db', check_same_thread=False)
c = conn.cursor()
c.execute('CREATE TABLE IF NOT EXISTS assessments (site TEXT, hazard TEXT, risk TEXT, date TEXT)')
c.execute('CREATE TABLE IF NOT EXISTS scenarios (title TEXT, description TEXT, answer TEXT)')
conn.commit()

st.set_page_config(page_title="Safety AI Pro")
st.title("🛡️ Safety AI Operating System")

menu = ["Site Assessment", "Safety Oracle", "Incident Training"]
choice = st.sidebar.radio("Navigation", menu)

if choice == "Site Assessment":
    st.subheader("🏗️ Real-Time Site Log")
    with st.form("site_form"):
        site = st.text_input("Location/Project")
        hazard = st.text_area("Observation")
        risk = st.select_slider("Priority", ["Low", "Medium", "High", "Critical"])
        if st.form_submit_button("Save & Analyze"):
            c.execute("INSERT INTO assessments VALUES (?,?,?,?)", (site, hazard, risk, datetime.datetime.now()))
            conn.commit()
            st.success("Logged to Memory!")

elif choice == "Safety Oracle":
    st.subheader("🔍 Search OHS Knowledge")
    st.text_input("Ask a question...")
    st.info("Searching your uploads folder...")

elif choice == "Incident Training":
    st.subheader("🚨 Investigation Simulation")
    st.markdown("**Scenario: The Fall Clearance**")
    st.write("Worker fell 4m in a harness but hit the ground. Lanyard was 2m, Shock absorber 1.5m.")
    if st.button("See Expert Analysis"):
        st.write("Analysis: The fall clearance was insufficient for the equipment used.")
