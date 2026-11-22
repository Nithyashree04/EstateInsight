# ============================================================
# COFFEE ESTATE ANALYTICS
# FILE : disease_pest_analytics.py
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# CREATE RESULTS FOLDER
# ============================================================

os.makedirs("Results", exist_ok=True)
# ============================================================
# LOAD DATASET
# ============================================================

print("="*60)
print("LOADING DATASET")
print("="*60)

df = pd.read_excel(
    r"C:\Users\Admin\OneDrive\Desktop\Sujay Project\Finaldataset1.xlsx"
)

print("Dataset Shape :", df.shape)
# ============================================================
# DATA SUMMARY
# ============================================================

print("\n" + "="*60)
print("PEST & DISEASE SUMMARY")
print("="*60)

print("Average Pest Severity    :", round(df["Pest_Severity_0_10"].mean(),2))
print("Average Disease Severity :", round(df["Disease_Severity_0_10"].mean(),2))

print()

print("Maximum Pest Severity    :", df["Pest_Severity_0_10"].max())
print("Maximum Disease Severity :", df["Disease_Severity_0_10"].max())

print()

print("Minimum Pest Severity    :", df["Pest_Severity_0_10"].min())
print("Minimum Disease Severity :", df["Disease_Severity_0_10"].min())
# ============================================================
# PEST BY DISTRICT
# ============================================================

pest_district = (
    df.groupby("District")["Pest_Severity_0_10"]
      .mean()
      .round(2)
)

print("\n" + "="*60)
print("PEST SEVERITY BY DISTRICT")
print("="*60)

print(pest_district)

pest_district.to_csv(
    "Results/pest_by_district.csv"
)

plt.figure(figsize=(8,5))

pest_district.plot(kind="bar")

plt.title("Average Pest Severity by District")
plt.xlabel("District")
plt.ylabel("Average Severity")

plt.tight_layout()

plt.savefig(
    "Results/pest_by_district.png",
    dpi=300
)

plt.close()

print("Pest Severity Chart Saved.")
# ============================================================
# DISEASE BY DISTRICT
# ============================================================

disease_district = (
    df.groupby("District")["Disease_Severity_0_10"]
      .mean()
      .round(2)
)

print("\n" + "="*60)
print("DISEASE SEVERITY BY DISTRICT")
print("="*60)

print(disease_district)

disease_district.to_csv(
    "Results/disease_by_district.csv"
)

plt.figure(figsize=(8,5))

disease_district.plot(kind="bar")

plt.title("Average Disease Severity by District")
plt.xlabel("District")
plt.ylabel("Average Severity")

plt.tight_layout()

plt.savefig(
    "Results/disease_by_district.png",
    dpi=300
)

plt.close()

print("Disease Severity Chart Saved.")
# ============================================================
# RISK SCORE
# ============================================================

print("\nCalculating Risk Score...")

df["Risk_Score"] = (

    0.5 * df["Pest_Severity_0_10"]

    +

    0.5 * df["Disease_Severity_0_10"]

)

def classify_risk(score):

    if score < 2:
        return "Low"

    elif score < 5:
        return "Moderate"

    elif score < 7.5:
        return "High"

    else:
        return "Critical"

df["Risk_Category"] = df["Risk_Score"].apply(classify_risk)

print("Risk Score Calculated.")

df.to_csv(
    "Results/high_risk_estates.csv",
    index=False
)

print("High Risk CSV Saved.")
# ============================================================
# RISK CATEGORY DISTRIBUTION
# ============================================================

risk_counts = df["Risk_Category"].value_counts()

print("\n" + "="*60)
print("RISK CATEGORY DISTRIBUTION")
print("="*60)

print(risk_counts)

# Save CSV
risk_counts.to_csv(
    "Results/risk_category_distribution.csv"
)

# -------------------- Bar Chart --------------------

plt.figure(figsize=(8,5))

risk_counts.plot(kind="bar")

plt.title("Risk Category Distribution")
plt.xlabel("Risk Category")
plt.ylabel("Number of Estates")

plt.tight_layout()

plt.savefig(
    "Results/risk_bar.png",
    dpi=300
)

plt.close()

print("Risk Bar Chart Saved.")

# -------------------- Pie Chart --------------------

plt.figure(figsize=(7,7))

plt.pie(
    risk_counts,
    labels=risk_counts.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Risk Category Distribution")

plt.savefig(
    "Results/risk_distribution.png",
    dpi=300
)

plt.close()

print("Risk Pie Chart Saved.")
# ============================================================
# CORRELATION HEATMAP
# ============================================================

print("\nGenerating Correlation Heatmap...")

corr = df[
    [
        "Yield_kg_ha",
        "Pest_Severity_0_10",
        "Disease_Severity_0_10",
        "Soil_Moisture_%",
        "Bean_Quality_Score"
    ]
].corr()

plt.figure(figsize=(7,6))

plt.imshow(corr, cmap="coolwarm")

plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
plt.yticks(range(len(corr.columns)), corr.columns)

plt.colorbar()

plt.title("Correlation Heatmap")

plt.tight_layout()

plt.savefig(
    "Results/correlation_heatmap.png",
    dpi=300
)

plt.close()

print("Correlation Heatmap Saved.")
# ============================================================
# SCATTER PLOTS
# ============================================================

# Pest vs Yield

plt.figure(figsize=(7,6))

plt.scatter(
    df["Pest_Severity_0_10"],
    df["Yield_kg_ha"],
    alpha=0.4
)

plt.xlabel("Pest Severity")
plt.ylabel("Yield")

plt.title("Pest Severity vs Yield")

plt.tight_layout()

plt.savefig(
    "Results/pest_vs_yield.png",
    dpi=300
)

plt.close()

print("Pest vs Yield Saved.")

# Disease vs Yield

plt.figure(figsize=(7,6))

plt.scatter(
    df["Disease_Severity_0_10"],
    df["Yield_kg_ha"],
    alpha=0.4
)

plt.xlabel("Disease Severity")
plt.ylabel("Yield")

plt.title("Disease Severity vs Yield")

plt.tight_layout()

plt.savefig(
    "Results/disease_vs_yield.png",
    dpi=300
)

plt.close()

print("Disease vs Yield Saved.")
# ============================================================
# TOP 10 HIGH RISK ESTATES
# ============================================================

top_risk = df.sort_values(
    by="Risk_Score",
    ascending=False
).head(10)

print("\n" + "="*60)
print("TOP 10 HIGH RISK ESTATES")
print("="*60)

print(
    top_risk[
        [
            "District",
            "Coffee_Type",
            "Pest_Severity_0_10",
            "Disease_Severity_0_10",
            "Risk_Score",
            "Risk_Category"
        ]
    ]
)

top_risk.to_csv(
    "Results/top10_high_risk.csv",
    index=False
)
# ============================================================
# DISTRICT RISK
# ============================================================

district_risk = (
    df.groupby("District")["Risk_Score"]
      .mean()
      .round(2)
      .sort_values(ascending=False)
)

print("\n" + "="*60)
print("DISTRICT RISK RANKING")
print("="*60)

print(district_risk)

district_risk.to_csv(
    "Results/district_risk.csv"
)
# ============================================================
# KPI SUMMARY
# ============================================================

print("\n" + "="*60)
print("DISEASE & PEST KPI")
print("="*60)

print(f"Total Estates            : {len(df)}")
print(f"Average Pest Severity    : {df['Pest_Severity_0_10'].mean():.2f}")
print(f"Average Disease Severity : {df['Disease_Severity_0_10'].mean():.2f}")

print(f"Critical Estates : {(df['Risk_Category']=='Critical').sum()}")
print(f"High Estates     : {(df['Risk_Category']=='High').sum()}")
print(f"Moderate Estates : {(df['Risk_Category']=='Moderate').sum()}")
print(f"Low Estates      : {(df['Risk_Category']=='Low').sum()}")
# ============================================================
# FINAL REPORT
# ============================================================

print("\n" + "="*60)
print("FILES GENERATED")
print("="*60)

print("Results/pest_by_district.csv")
print("Results/disease_by_district.csv")
print("Results/high_risk_estates.csv")
print("Results/top10_high_risk.csv")
print("Results/district_risk.csv")
print("Results/risk_category_distribution.csv")

print("\nCharts Generated")

print("pest_by_district.png")
print("disease_by_district.png")
print("risk_distribution.png")
print("risk_bar.png")
print("pest_vs_yield.png")
print("disease_vs_yield.png")
print("correlation_heatmap.png")

print("\n" + "="*60)
print("DISEASE & PEST ANALYTICS COMPLETED SUCCESSFULLY")
print("="*60)