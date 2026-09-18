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

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------

# If the dataset is in the same folder as this script,
# simply specify the file name.

file_path = r"C:\Users\Admin\Downloads\Karnataka_Coffee_Master_V3_15000.xlsx"

df = pd.read_excel(file_path)

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