# ============================================================
# COFFEE ESTATE ANALYTICS
# FILE : 06_estate_health.py
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# LOAD DATASET
# ============================================================

print("=" * 60)
print("LOADING DATASET")
print("=" * 60)

df = pd.read_excel(
    r"C:\Users\Admin\OneDrive\Desktop\Sujay Project\Karnataka_Coffee_Cleaned.xlsx"
)

print("Dataset Shape :", df.shape)

# ============================================================
# CREATE RESULTS FOLDER
# ============================================================

os.makedirs("Results", exist_ok=True)

# ============================================================
# NORMALIZE FEATURES (0 - 100 SCALE)
# ============================================================

print("\nNormalizing Features...")

def normalize(series):
    return (
        (series - series.min()) /
        (series.max() - series.min())
    ) * 100

soil = normalize(df["Soil_Moisture_%"])

bean = normalize(df["Bean_Quality_Score"])

sustainability = normalize(df["Sustainability_Score"])

# Lower pest & disease = better health
pest = 100 - normalize(df["Pest_Severity_0_10"])

disease = 100 - normalize(df["Disease_Severity_0_10"])

print("Normalization Completed.")

# ============================================================
# CALCULATE ESTATE HEALTH SCORE
# ============================================================

print("\nCalculating Estate Health Score...")

df["Estate_Health_Score"] = (

      soil * 0.25
    + bean * 0.20
    + sustainability * 0.20
    + pest * 0.20
    + disease * 0.15

)

print("Estate Health Score Calculated.")

# ============================================================
# HEALTH CATEGORY
# ============================================================

def health_category(score):

    if score >= 80:
        return "Excellent"

    elif score >= 60:
        return "Good"

    elif score >= 40:
        return "Moderate"

    else:
        return "Poor"

def health_category(score):

    if score >= 75:
      return "Excellent"
    elif score >= 60:
      return "Good"
    elif score >= 40:
      return "Moderate"
    else:
      return "Poor"
df["Health_Category"] = df["Estate_Health_Score"].apply(health_category)

# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("ESTATE HEALTH SUMMARY")
print("=" * 60)

print(df["Estate_Health_Score"].describe())

print("\nHealth Category Counts\n")

print(df["Health_Category"].value_counts())

print("\nAverage Health Score :",
      round(df["Estate_Health_Score"].mean(), 2))

print("Highest Health Score :",
      round(df["Estate_Health_Score"].max(), 2))

print("Lowest Health Score :",
      round(df["Estate_Health_Score"].min(), 2))

# ============================================================
# SAVE RESULTS
# ============================================================

df.to_csv(
    "Results/estate_health.csv",
    index=False
)

print("\nEstate Health CSV Saved.")

# ============================================================
# BAR CHART
# ============================================================

health_counts = df["Health_Category"].value_counts()

plt.figure(figsize=(8,5))

health_counts.plot(
    kind="bar",
    color=[
        "green",
        "steelblue",
        "orange",
        "red"
    ]
)

plt.title("Estate Health Distribution")

plt.xlabel("Health Category")

plt.ylabel("Number of Estates")

plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    "Results/health_distribution.png",
    dpi=300
)

plt.close()

print("Bar Chart Saved.")

# ============================================================
# PIE CHART
# ============================================================

plt.figure(figsize=(7,7))

health_counts.plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90
)

plt.ylabel("")

plt.title("Estate Health Percentage")

plt.tight_layout()

plt.savefig(
    "Results/health_pie_chart.png",
    dpi=300
)

plt.close()

print("Pie Chart Saved.")

# ============================================================
# HISTOGRAM
# ============================================================

plt.figure(figsize=(8,5))

plt.hist(
    df["Estate_Health_Score"],
    bins=20,
    edgecolor="black"
)

plt.xlabel("Estate Health Score")

plt.ylabel("Number of Estates")

plt.title("Estate Health Score Distribution")

plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    "Results/health_histogram.png",
    dpi=300
)

plt.close()

print("Histogram Saved.")

# ============================================================
# DISTRICT HEALTH COMPARISON
# ============================================================

district_health = (
    df.groupby("District")["Estate_Health_Score"]
      .mean()
      .sort_values(ascending=False)
)

plt.figure(figsize=(8,5))

district_health.plot(
    kind="bar",
    color="teal"
)

plt.title("Average Estate Health by District")

plt.xlabel("District")

plt.ylabel("Average Health Score")

plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    "Results/district_health.png",
    dpi=300
)

plt.close()

print("District Comparison Saved.")

# ============================================================
# TOP 10 HEALTHIEST ESTATES
# ============================================================

print("\n" + "=" * 60)
print("TOP 10 HEALTHIEST ESTATES")
print("=" * 60)

top10 = df.nlargest(
    10,
    "Estate_Health_Score"
)[[
    "District",
    "Coffee_Type",
    "Estate_Health_Score",
    "Health_Category"
]]

print(top10)

top10.to_csv(
    "Results/top10_healthiest_estates.csv",
    index=False
)

# ============================================================
# WORST 10 ESTATES
# ============================================================

print("\n" + "=" * 60)
print("BOTTOM 10 ESTATES")
print("=" * 60)

bottom10 = df.nsmallest(
    10,
    "Estate_Health_Score"
)[[
    "District",
    "Coffee_Type",
    "Estate_Health_Score",
    "Health_Category"
]]

print(bottom10)

bottom10.to_csv(
    "Results/bottom10_estates.csv",
    index=False
)

# ============================================================
# COMPLETED
# ============================================================

print("\n")
print("=" * 60)
print("ESTATE HEALTH ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 60)

print("Results Saved : Results/estate_health.csv")

print("Top 10 Estates : Results/top10_healthiest_estates.csv")

print("Bottom 10 Estates : Results/bottom10_estates.csv")

print("Charts Saved :")

print(" • health_distribution.png")

print(" • health_pie_chart.png")

print(" • health_histogram.png")

print(" • district_health.png")

print("=" * 60)
# ============================================================
# DISTRICT HEALTH RANKING
# ============================================================

district_health = (
    df.groupby("District")["Estate_Health_Score"]
      .mean()
      .sort_values(ascending=False)
)

print("\n" + "=" * 60)
print("DISTRICT HEALTH RANKING")
print("=" * 60)
print(district_health)

district_health.to_csv(
    "Results/district_health_ranking.csv"
)
# ============================================================
# KPI SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("ESTATE HEALTH KPI")
print("=" * 60)

print(f"Total Estates        : {len(df)}")
print(f"Average Health Score : {df['Estate_Health_Score'].mean():.2f}")
print(f"Excellent Estates    : {(df['Health_Category']=='Excellent').sum()}")
print(f"Good Estates         : {(df['Health_Category']=='Good').sum()}")
print(f"Moderate Estates     : {(df['Health_Category']=='Moderate').sum()}")
print(f"Poor Estates         : {(df['Health_Category']=='Poor').sum()}")