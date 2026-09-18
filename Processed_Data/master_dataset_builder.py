# ============================================================
# COFFEE ESTATE ANALYTICS
# FILE : master_dataset_builder.py
# ============================================================

import os
import pandas as pd

print("=" * 60)
print("MASTER DATASET BUILDER")
print("=" * 60)

# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs("Processed_Data", exist_ok=True)

# ============================================================
# LOAD ORIGINAL DATASET
# ============================================================

dataset_path = r"C:\Users\Admin\OneDrive\Desktop\Sujay Project\Karnataka_Coffee_Cleaned.xlsx"

df = pd.read_excel(dataset_path)

print("\nOriginal Dataset Loaded Successfully")
print("Shape :", df.shape)
print("Columns :", len(df.columns))
# ============================================================
# HELPER FUNCTION
# ============================================================

def merge_columns(csv_path, columns):

    if not os.path.exists(csv_path):
        print(f"Skipped : {csv_path} not found.")
        return

    temp = pd.read_csv(csv_path)

    for col in columns:

        if col in temp.columns:

            df[col] = temp[col]

            print(f"Merged : {col}")

        else:

            print(f"Column Missing : {col}")
# ============================================================
# ESTATE HEALTH
# ============================================================

merge_columns(

    "Results/estate_health.csv",

    [

        "Estate_Health_Score",
        "Health_Category"

    ]

)
# ============================================================
# DISEASE & PEST
# ============================================================

merge_columns(

    "Results/high_risk_estates.csv",

    [

        "Risk_Score",
        "Risk_Category"

    ]

)
# ============================================================
# SOIL NUTRIENTS
# ============================================================

merge_columns(

    "Results/nutrient_status.csv",

    [

        "Nutrient_Score",
        "Nutrient_Status"

    ]

)
# ============================================================
# SUSTAINABILITY
# ============================================================

merge_columns(

    "Results/sustainability_category.csv",

    [

        "Sustainability_Category"

    ]

)
# ============================================================
# AI RECOMMENDATION
# ============================================================

merge_columns(

    "Results/ai_recommendations.csv",

    [

        "AI_Recommendation",
        "Priority"

    ]

)
# ============================================================
# FORECAST
# ============================================================

merge_columns(

    "Results/yield_forecast.csv",

    [

        "Predicted_Yield",
        "Expected_Profit",
        "Forecast_Status"

    ]

)
# ============================================================
# CLIMATE
# ============================================================

merge_columns(

    "Results/climate_summary.csv",

    [

        "Climate_Index"

    ]

)
# ============================================================
# OVERALL RATING
# ============================================================

if "Estate_Health_Score" in df.columns and \
   "Sustainability_Score" in df.columns and \
   "Bean_Quality_Score" in df.columns:

    df["Overall_Rating"] = (

        df["Estate_Health_Score"] * 0.40 +

        df["Bean_Quality_Score"] * 0.30 +

        df["Sustainability_Score"] * 0.30

    ).round(2)

    print("Overall Rating Calculated.")

# ============================================================
# SAVE MASTER DATASET
# ============================================================

output_path = "Processed_Data/Coffee_Estate_Master.xlsx"

df.to_excel(

    output_path,

    index=False

)

print("\nMaster Dataset Saved Successfully")
print("Location :", output_path)

print("\nFinal Shape :", df.shape)
print("Total Columns :", len(df.columns))
# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("MASTER DATASET BUILD COMPLETED")
print("=" * 60)

print("Input File")
print("--------------------------------")
print(dataset_path)

print("\nOutput File")
print("--------------------------------")
print(output_path)

print("\nDataset Information")
print("--------------------------------")
print("Rows :", len(df))
print("Columns :", len(df.columns))

print("\nNew Columns Added")
print("--------------------------------")

new_columns = [

    "Estate_Health_Score",
    "Health_Category",
    "Risk_Score",
    "Risk_Category",
    "Nutrient_Score",
    "Nutrient_Status",
    "Sustainability_Category",
    "AI_Recommendation",
    "Priority",
    "Predicted_Yield",
    "Expected_Profit",
    "Forecast_Status",
    "Climate_Index",
    "Overall_Rating"

]

for col in new_columns:

    if col in df.columns:

       print("[OK]", col)

print("\n" + "=" * 60)
print("READY FOR STREAMLIT DASHBOARD")
print("=" * 60)
