import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Patient Health Dashboard",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("healthcare_clean_data.csv")
df['visit_date'] = pd.to_datetime(df['visit_date'])

# -----------------------------
# TITLE & DESCRIPTION
# -----------------------------
st.title("Patient Health Analytics Dashboard")
st.markdown("""
**Purpose:**  
This dashboard explores whether **demographics (age & gender)** influence  
**blood pressure, cholesterol, health conditions, and hospital visits**.
""")

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("Filters")

age_groups = st.sidebar.multiselect(
    "Select Age Group",
    options=df['age_group'].unique(),
    default=df['age_group'].unique()
)

genders = st.sidebar.multiselect(
    "Select Gender",
    options=df['gender'].unique(),
    default=df['gender'].unique()
)

filtered_df = df[
    (df['age_group'].isin(age_groups)) &
    (df['gender'].isin(genders))
]

# -----------------------------
# KPI METRICS (TOP SUMMARY)
# -----------------------------
st.subheader("Key Summary Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Patients", len(filtered_df))
col2.metric("Average Age", round(filtered_df['age'].mean(), 1))
col3.metric("High BP Patients", (filtered_df['bp_level'] == 'High').sum())
col4.metric(
    "High Cholesterol Patients",
    (filtered_df['cholesterol_level'] == 'Borderline High').sum()
)

st.divider()

# ==========================================================
# 1. WHO ARE THE PATIENTS? (DEMOGRAPHICS)
# ==========================================================
st.header("1. Patient Demographics")

col1, col2 = st.columns(2)

with col1:
    fig_age = px.pie(
        filtered_df,
        names='age_group',
        title="Age Group Distribution"
    )
    st.plotly_chart(fig_age, use_container_width=True)

with col2:
    fig_gender = px.pie(
        filtered_df,
        names='gender',
        title="Gender Distribution"
    )
    st.plotly_chart(fig_gender, use_container_width=True)

# ==========================================================
# 2. DO BP & CHOLESTEROL DIFFER BY AGE & GENDER?
# ==========================================================
st.header("2. Blood Pressure & Cholesterol by Demographics")

col1, col2 = st.columns(2)

with col1:
    fig_bp = px.box(
        filtered_df,
        x='age_group',
        y='systolic',
        color='gender',
        title="Systolic Blood Pressure by Age Group & Gender"
    )
    st.plotly_chart(fig_bp, use_container_width=True)

with col2:
    fig_chol = px.box(
        filtered_df,
        x='age_group',
        y='cholesterol',
        color='gender',
        title="Cholesterol Levels by Age Group & Gender"
    )
    st.plotly_chart(fig_chol, use_container_width=True)

# ==========================================================
# 3. WHO IS AT HIGHER RISK?
# ==========================================================
st.header("3. High Risk Patients")

high_risk_df = filtered_df.copy()
high_risk_df['high_risk'] = (
    (high_risk_df['bp_level'] == 'High') |
    (high_risk_df['cholesterol_level'] == 'Borderline High')
)

risk_summary = (
    high_risk_df
    .groupby(['age_group', 'gender'])['high_risk']
    .sum()
    .reset_index()
)

fig_risk = px.bar(
    risk_summary,
    x='age_group',
    y='high_risk',
    color='gender',
    barmode='group',
    title="High Risk Patients by Age Group & Gender"
)
st.plotly_chart(fig_risk, use_container_width=True)

# ==========================================================
# 4. ARE CERTAIN CONDITIONS LINKED WITH BP OR CHOLESTEROL?
# ==========================================================
st.header("4. Health Conditions vs BP & Cholesterol")

col1, col2 = st.columns(2)

with col1:
    fig_cond_bp = px.box(
        filtered_df,
        x='condition',
        y='systolic',
        title="Blood Pressure by Condition"
    )
    st.plotly_chart(fig_cond_bp, use_container_width=True)

with col2:
    fig_cond_chol = px.box(
        filtered_df,
        x='condition',
        y='cholesterol',
        title="Cholesterol Levels by Condition"
    )
    st.plotly_chart(fig_cond_chol, use_container_width=True)

# ==========================================================
# 5. WHEN DO PATIENTS VISIT THE MOST?
# ==========================================================
st.header("5. Patient Visit Patterns")

filtered_df['visit_month'] = filtered_df['visit_date'].dt.month_name()
filtered_df['visit_year'] = filtered_df['visit_date'].dt.year

month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

month_visits = (
    filtered_df
    .groupby('visit_month')
    .size()
    .reindex(month_order, fill_value=0)
    .reset_index(name='visits')
)

year_visits = (
    filtered_df
    .groupby('visit_year')
    .size()
    .reset_index(name='visits')
)

col1, col2 = st.columns(2)

with col1:
    fig_month = px.bar(
        month_visits,
        x='visit_month',
        y='visits',
        title="Visits by Month"
    )
    st.plotly_chart(fig_month, use_container_width=True)

with col2:
    fig_year = px.bar(
        year_visits,
        x='visit_year',
        y='visits',
        title="Visits by Year"
    )
    st.plotly_chart(fig_year, use_container_width=True)

# ==========================================================
# DATASET PREVIEW
# ==========================================================
st.header("Dataset Preview")
st.write("Filtered view of the cleaned healthcare dataset:")
st.dataframe(filtered_df)
