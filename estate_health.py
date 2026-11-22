
# ============================================================
# COFFEE ESTATE ANALYTICS
# FILE : 06_estate_health.py
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# LOAD DATASET
# ============================================================

print("=" * 60)
print("LOADING DATASET")
print("=" * 60)

DATASET_PATH = (
    r"C:\Users\Admin\OneDrive\Desktop\Sujay Project\Finaldataset1.xlsx"
)

df = pd.read_excel(DATASET_PATH)

print("Dataset Shape:", df.shape)

# ============================================================
# CREATE RESULTS FOLDER
# ============================================================

os.makedirs("Results", exist_ok=True)

# ============================================================
# VALIDATE REQUIRED COLUMNS
# ============================================================

required_columns = [
    "Soil_Moisture_%",
    "Bean_Quality_Score",
    "Sustainability_Score",
    "Pest_Severity_0_10",
    "Disease_Severity_0_10",
    "District",
    "Coffee_Type",
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required dataset columns: {missing_columns}"
    )

# ============================================================
# NORMALIZE FEATURES (0 - 100 SCALE)
# ============================================================

print("\nNormalizing Features...")


def normalize(series):
    """Normalize numeric values to a 0–100 scale safely."""
    values = pd.to_numeric(series, errors="coerce")
    min_value = values.min()
    max_value = values.max()

    if pd.isna(min_value) or pd.isna(max_value):
        return pd.Series(50.0, index=series.index)

    if max_value == min_value:
        return pd.Series(50.0, index=series.index)

    return (
        (values - min_value) /
        (max_value - min_value)
    ) * 100


soil = normalize(df["Soil_Moisture_%"])
bean = normalize(df["Bean_Quality_Score"])
sustainability = normalize(df["Sustainability_Score"])

# Lower pest and disease severity means better health.
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
    if pd.isna(score):
        return "Unknown"
    elif score >= 75:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Moderate"
    else:
        return "Poor"


df["Health_Category"] = df["Estate_Health_Score"].apply(
    health_category
)

# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("ESTATE HEALTH SUMMARY")
print("=" * 60)

print(df["Estate_Health_Score"].describe())
print("\nHealth Category Counts\n")
print(df["Health_Category"].value_counts())

print(
    "\nAverage Health Score:",
    round(df["Estate_Health_Score"].mean(), 2)
)

print(
    "Highest Health Score:",
    round(df["Estate_Health_Score"].max(), 2)
)

print(
    "Lowest Health Score:",
    round(df["Estate_Health_Score"].min(), 2)
)

# ============================================================
# SAVE RESULTS
# ============================================================

df.to_csv("Results/estate_health.csv", index=False)
print("\nEstate Health CSV Saved.")

# ============================================================
# HEALTH DISTRIBUTION BAR CHART
# ============================================================

category_order = ["Excellent", "Good", "Moderate", "Poor"]

health_counts = (
    df["Health_Category"]
    .value_counts()
    .reindex(category_order, fill_value=0)
)

plt.figure(figsize=(8, 5))
health_counts.plot(
    kind="bar",
    color=["green", "steelblue", "orange", "red"]
)

plt.title("Estate Health Distribution")
plt.xlabel("Health Category")
plt.ylabel("Number of Records")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("Results/health_distribution.png", dpi=300)
plt.close()

print("Bar Chart Saved.")

# ============================================================
# HEALTH PIE CHART
# ============================================================

pie_counts = health_counts[health_counts > 0]

if not pie_counts.empty:
    plt.figure(figsize=(7, 7))
    pie_counts.plot(
        kind="pie",
        autopct="%1.1f%%",
        startangle=90
    )
    plt.ylabel("")
    plt.title("Estate Health Percentage")
    plt.tight_layout()
    plt.savefig("Results/health_pie_chart.png", dpi=300)
    plt.close()

print("Pie Chart Saved.")

# ============================================================
# HEALTH SCORE HISTOGRAM
# ============================================================

health_scores = df["Estate_Health_Score"].dropna()

plt.figure(figsize=(8, 5))
plt.hist(
    health_scores,
    bins=20,
    edgecolor="black"
)

plt.xlabel("Estate Health Score")
plt.ylabel("Number of Records")
plt.title("Estate Health Score Distribution")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("Results/health_histogram.png", dpi=300)
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

plt.figure(figsize=(8, 5))
district_health.plot(kind="bar", color="teal")

plt.title("Average Estate Health by District")
plt.xlabel("District")
plt.ylabel("Average Health Score")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("Results/district_health.png", dpi=300)
plt.close()

print("District Comparison Saved.")

# ============================================================
# TOP 10 HEALTHIEST RECORDS
# ============================================================

print("\n" + "=" * 60)
print("TOP 10 HEALTHIEST ESTATES")
print("=" * 60)

top10 = df.nlargest(
    10, "Estate_Health_Score"
)[[
    "District",
    "Coffee_Type",
    "Estate_Health_Score",
    "Health_Category"
]]

print(top10)
top10.to_csv("Results/top10_healthiest_estates.csv", index=False)

# ============================================================
# BOTTOM 10 RECORDS
# ============================================================

print("\n" + "=" * 60)
print("BOTTOM 10 ESTATES")
print("=" * 60)

bottom10 = df.nsmallest(
    10, "Estate_Health_Score"
)[[
    "District",
    "Coffee_Type",
    "Estate_Health_Score",
    "Health_Category"
]]

print(bottom10)
bottom10.to_csv("Results/bottom10_estates.csv", index=False)

# ============================================================
# DISTRICT HEALTH RANKING
# ============================================================

print("\n" + "=" * 60)
print("DISTRICT HEALTH RANKING")
print("=" * 60)

print(district_health)

district_health.to_csv(
    "Results/district_health_ranking.csv",
    header=["Average_Health_Score"]
)

# ============================================================
# ESTATE HEALTH KPI SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("ESTATE HEALTH KPI")
print("=" * 60)

print(f"Total Records         : {len(df)}")
print(
    f"Average Health Score  : "
    f"{df['Estate_Health_Score'].mean():.2f}"
)
print(
    f"Excellent Records     : "
    f"{(df['Health_Category'] == 'Excellent').sum()}"
)
print(
    f"Good Records          : "
    f"{(df['Health_Category'] == 'Good').sum()}"
)
print(
    f"Moderate Records      : "
    f"{(df['Health_Category'] == 'Moderate').sum()}"
)
print(
    f"Poor Records          : "
    f"{(df['Health_Category'] == 'Poor').sum()}"
)

# ============================================================
# COMPLETED
# ============================================================

print("\n" + "=" * 60)
print("ESTATE HEALTH ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 60)

print("Results Saved       : Results/estate_health.csv")
print("Top 10 Estates      : Results/top10_healthiest_estates.csv")
print("Bottom 10 Estates   : Results/bottom10_estates.csv")
print("Health Distribution : Results/health_distribution.png")
print("Health Pie Chart    : Results/health_pie_chart.png")
print("Health Histogram    : Results/health_histogram.png")
print("District Comparison : Results/district_health.png")
print("=" * 60)