# ==========================================================
# AI Coffee Estate Analytics Project
# Step 2 : Data Cleaning
# ==========================================================

# Import Pandas
import pandas as pd

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------

df = pd.read_excel(r"C:\Users\Admin\OneDrive\Desktop\Sujay Project\Finaldataset1.xlsx")

print("="*60)
print("DATA CLEANING")
print("="*60)

# ----------------------------------------------------------
# Check Missing Values
# ----------------------------------------------------------

print("\nMissing Values")
print(df.isnull().sum())

# ----------------------------------------------------------
# Check Duplicate Rows
# ----------------------------------------------------------

duplicates = df.duplicated().sum()

print("\nDuplicate Rows :", duplicates)

# Remove duplicate rows if any exist

if duplicates > 0:
    df = df.drop_duplicates()
    print("Duplicate rows removed.")
else:
    print("No duplicate rows found.")

# ----------------------------------------------------------
# Check Data Types
# ----------------------------------------------------------

print("\nData Types")
print(df.dtypes)

# ----------------------------------------------------------
# Remove Unnecessary Columns
# ----------------------------------------------------------

# Estate_ID is only an identifier.
# It is usually not useful for Machine Learning.

if "Estate_ID" in df.columns:
    df = df.drop(columns=["Estate_ID"])
    print("\nEstate_ID column removed.")

# ----------------------------------------------------------
# Check for Invalid Numerical Values
# ----------------------------------------------------------

print("\nChecking Negative Values...")

numerical_columns = df.select_dtypes(include=['int64', 'float64']).columns

for column in numerical_columns:

    negative_values = (df[column] < 0).sum()

    if negative_values > 0:
        print(f"{column} : {negative_values} negative values found")

print("Negative value check completed.")

# ----------------------------------------------------------
# Remove Impossible Values (Example)
# ----------------------------------------------------------

# Soil moisture should never exceed 100%

if "Soil_Moisture_%" in df.columns:
    df = df[df["Soil_Moisture_%"] <= 100]

# Temperature should not be below -10°C or above 60°C

temperature_columns = [col for col in df.columns if "Temp_" in col]

for column in temperature_columns:

    df = df[(df[column] >= -10) & (df[column] <= 60)]

# Rainfall should never be negative

rain_columns = [col for col in df.columns if "Rain_" in col]

for column in rain_columns:

    df = df[df[column] >= 0]

print("\nInvalid value check completed.")

# ----------------------------------------------------------
# Final Dataset Shape
# ----------------------------------------------------------

print("\nFinal Dataset Shape")

print(df.shape)

# ----------------------------------------------------------
# Save Clean Dataset
# ----------------------------------------------------------

df.to_excel("Karnataka_Coffee_Cleaned.xlsx", index=False)

print("\nCleaned dataset saved successfully.")

print("\nFile Name : Karnataka_Coffee_Cleaned.xlsx")
