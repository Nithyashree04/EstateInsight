# ==========================================================
# AI Coffee Estate Analytics Project
# File Name : 01_data_loading.py
# Purpose   : Load the dataset and perform basic inspection
# Author    : Nithya Shree V B
# ==========================================================

# ----------------------------------------------------------
# Import Required Library
# ----------------------------------------------------------

import pandas as pd


# ============================================================
# LOAD NEW DATASET
# ============================================================

DATASET_PATH = r"C:\Users\Admin\OneDrive\Desktop\Sujay Project\Finaldataset1.xlsx"

@st.cache_data
def load_new_dataset(file_path):
    data = pd.read_excel(file_path)
    data.columns = data.columns.astype(str).str.strip()
    return data

try:
    df = load_new_dataset(DATASET_PATH)

except FileNotFoundError:
    st.error("Dataset not found. Please check the Excel file path.")
    st.stop()

except Exception as e:
    st.error("Unable to load the new dataset.")
    st.exception(e)
    st.stop()

# ============================================================
# VALIDATE DATA
# ============================================================

if df is None or df.empty:
    st.error("The dataset is empty.")
    st.stop()

st.sidebar.success(
    f"Loaded {len(df):,} records successfully"
)

# ----------------------------------------------------------
# Display First Five Rows
# ----------------------------------------------------------

print("\n" + "=" * 60)
print("FIRST FIVE ROWS")
print("=" * 60)

print(df.head())

# ----------------------------------------------------------
# Display Last Five Rows
# ----------------------------------------------------------

print("\n" + "=" * 60)
print("LAST FIVE ROWS")
print("=" * 60)

print(df.tail())

# ----------------------------------------------------------
# Display Dataset Shape
# ----------------------------------------------------------

print("\n" + "=" * 60)
print("DATASET SHAPE")
print("=" * 60)

print(f"Number of Rows    : {df.shape[0]}")
print(f"Number of Columns : {df.shape[1]}")

# ----------------------------------------------------------
# Display Column Names
# ----------------------------------------------------------

print("\n" + "=" * 60)
print("COLUMN NAMES")
print("=" * 60)

for column in df.columns:
    print(column)

# ----------------------------------------------------------
# Display Dataset Information
# ----------------------------------------------------------

print("\n" + "=" * 60)
print("DATASET INFORMATION")
print("=" * 60)

df.info()

# Check missing values

print("\n" + "="*60)
print("MISSING VALUES")
print("="*60)

print(df.isnull().sum())
print("\nTotal Missing Values :", df.isnull().sum().sum())
# ----------------------------------------------------------
# Display Statistical Summary
# ----------------------------------------------------------

print("\n" + "=" * 60)
print("STATISTICAL SUMMARY")
print("=" * 60)

print(df.describe())

# ----------------------------------------------------------
# Identify Numerical Features
# ----------------------------------------------------------

numerical_columns = df.select_dtypes(include=["int64", "float64"]).columns

print("\n" + "=" * 60)
print("NUMERICAL FEATURES")
print("=" * 60)

for column in numerical_columns:
    print(column)

# ----------------------------------------------------------
# Identify Categorical Features
# ----------------------------------------------------------

categorical_columns = df.select_dtypes(include=["object", "string", "str"]).columns

print("\n" + "=" * 60)
print("CATEGORICAL FEATURES")
print("=" * 60)

for column in categorical_columns:
    print(column)

# ----------------------------------------------------------
# Count Numerical and Categorical Features
# ----------------------------------------------------------

print("\n" + "=" * 60)
print("FEATURE COUNT")
print("=" * 60)

print(f"Number of Numerical Features   : {len(numerical_columns)}")
print(f"Number of Categorical Features : {len(categorical_columns)}")

# ----------------------------------------------------------
# End of Data Loading
# ----------------------------------------------------------

print("\n" + "=" * 60)
print("DATA LOADING COMPLETED SUCCESSFULLY")
print("=" * 60)