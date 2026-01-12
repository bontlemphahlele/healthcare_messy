# Patient Health Analytics Dashboard



This project involves the cleaning and analysis of messy healthcare data. The process includes data wrangling, exploratory data analysis (EDA), and the creation of an interactive web dashboard using Streamlit to visualize patient health metrics.

## Project Overview

The primary goal is to transform a raw, inconsistent healthcare dataset into a clean, structured format suitable for analysis. Subsequently, an interactive dashboard is built to explore relationships between patient demographics (age, gender) and key health indicators such as blood pressure, cholesterol levels, existing health conditions, and hospital visit patterns.

### Key Components

*   `clean.ipynb`: A Jupyter Notebook detailing the entire data cleaning and exploratory data analysis (EDA) process.
*   `app.py`: A Streamlit application that creates and runs the interactive patient health analytics dashboard.
*   `healthcare_messy_data.csv`: The initial, raw dataset with various inconsistencies, missing values, and formatting errors.
*   `healthcare_clean_data.csv`: The cleaned and processed dataset, used as the source for the Streamlit dashboard.

## Data Cleaning and Preparation

The `clean.ipynb` notebook documents the comprehensive steps taken to clean `healthcare_messy_data.csv`:

*   **Handling Missing Data**: Missing values in columns like `age` and `cholesterol` were imputed using the median.
*   **Data Type Correction**: Corrected inconsistent data types, such as converting string ages (e.g., 'forty') to numeric and ensuring columns like `age` and `cholesterol` are integers.
*   **Column Transformation**:
    *   The `blood_pressure` column was split into separate `systolic` and `diastolic` numeric columns.
    *   Personal Identifiable Information (PII) like `Patient Name`, `Email`, and `Phone Number` were dropped to ensure privacy, and a `patient_id` was generated.
*   **Date Standardization**: The `visit_date` column, which had multiple formats (`%m/%d/%Y`, `%B %d, %Y`, etc.), was standardized to a consistent `YYYY-MM-DD` format.
*   **Feature Engineering**: New categorical features were created to facilitate analysis:
    *   `age_group`: Categorized ages into 'Child', 'Young', 'Adult', and 'Senior'.
    *   `bp_level`: Classified blood pressure as 'Normal', 'Elevated', or 'High'.
    *   `cholesterol_level`: Classified cholesterol as 'Normal', 'Borderline High', or 'High'.
*   **Data Validation**: Corrected illogical entries, such as mapping the correct `medication` to its corresponding `condition`.

## Interactive Dashboard

The `app.py` script launches a web-based dashboard using Streamlit, Plotly, and Pandas. The dashboard provides an interactive interface to explore the cleaned patient data.

### Features

*   **Dynamic Filtering**: Users can filter the data by `Age Group` and `Gender` using the sidebar controls.
*   **Key Performance Indicators (KPIs)**: A top-level summary displays key metrics like Total Patients, Average Age, and counts of patients with high blood pressure or high cholesterol.
*   **Patient Demographics**: Pie charts visualize the distribution of patients across different age groups and genders.
*   **Health Risk Analysis**:
    *   Box plots compare systolic blood pressure and cholesterol levels across age groups and genders.
    *   A bar chart identifies the number of high-risk patients (high BP or cholesterol) by demographic segments.
*   **Visit Pattern Analysis**: Bar charts show the total number of patient visits aggregated by month and year.
*   **Data Preview**: A table displays the filtered, cleaned dataset for direct inspection.

## How to Run

To run the interactive dashboard locally, follow these steps:

1.  **Prerequisites**:
    *   Python 3.7+
    *   pip

2.  **Clone the repository**:
    ```bash
    git clone https://github.com/bontlemphahlele/healthcare_messy.git
    cd healthcare_messy
    ```

3.  **Install the required libraries**:
    ```bash
    pip install streamlit pandas plotly-express
    ```

4.  **Run the Streamlit application**:
    ```bash
    streamlit run app.py
    ```

    This will open the Patient Health Analytics Dashboard in your default web browser.
