# ============================================================
# COFFEE ESTATE ANALYTICS
# FILE : sustainability_dashboard.py
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

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
    r"C:\Users\Admin\OneDrive\Desktop\Sujay Project\Karnataka_Coffee_Cleaned.xlsx"
)
print("Dataset Shape :", df.shape)

# ============================================================
# SUSTAINABILITY SUMMARY
# ============================================================

print("\n" + "="*60)
print("SUSTAINABILITY SUMMARY")
print("="*60)

print(f"Average Sustainability Score : {df['Sustainability_Score'].mean():.2f}")
print(f"Maximum Sustainability Score : {df['Sustainability_Score'].max():.2f}")
print(f"Minimum Sustainability Score : {df['Sustainability_Score'].min():.2f}")

print()

print(f"Average Carbon Footprint : {df['Carbon_Footprint_tCO2e'].mean():.2f}")
print(f"Maximum Carbon Footprint : {df['Carbon_Footprint_tCO2e'].max():.2f}")
print(f"Minimum Carbon Footprint : {df['Carbon_Footprint_tCO2e'].min():.2f}")

# ============================================================
# DISTRICT SUSTAINABILITY
# ============================================================

district = df.groupby("District")[[
    "Sustainability_Score",
    "Carbon_Footprint_tCO2e"
]].mean().round(2)

print("\n" + "="*60)
print("DISTRICT SUSTAINABILITY")
print("="*60)

print(district)

district.to_csv(
    "Results/district_sustainability.csv"
)

print("District Sustainability CSV Saved.")

# ============================================================
# DISTRICT BAR CHART
# ============================================================

district["Sustainability_Score"].plot(
    kind="bar",
    figsize=(8,5)
)

plt.ylabel("Average Sustainability Score")
plt.title("District Sustainability Score")

plt.tight_layout()

plt.savefig(
    "Results/district_sustainability.png",
    dpi=300
)

plt.close()

print("District Sustainability Chart Saved.")

# ============================================================
# CARBON FOOTPRINT BY DISTRICT
# ============================================================

district["Carbon_Footprint_tCO2e"].plot(
    kind="bar",
    figsize=(8,5)
)

plt.ylabel("Carbon Footprint (tCO2e)")
plt.title("Average Carbon Footprint by District")

plt.tight_layout()

plt.savefig(
    "Results/district_carbon.png",
    dpi=300
)

plt.close()

print("District Carbon Chart Saved.")
# ============================================================
# SUSTAINABILITY CATEGORY
# ============================================================

print("\nCalculating Sustainability Category...")

def classify(score):

    if score >= 85:
        return "Excellent"

    elif score >= 70:
        return "Good"

    elif score >= 50:
        return "Moderate"

    else:
        return "Poor"

df["Sustainability_Category"] = df[
    "Sustainability_Score"
].apply(classify)

category = df["Sustainability_Category"].value_counts()

print("\n" + "="*60)
print("SUSTAINABILITY CATEGORY")
print("="*60)

print(category)

category.to_csv(
    "Results/sustainability_category.csv"
)

print("Category CSV Saved.")
# ============================================================
# SUSTAINABILITY DISTRIBUTION
# ============================================================

plt.figure(figsize=(7,7))

plt.pie(
    category,
    labels=category.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Sustainability Distribution")

plt.savefig(
    "Results/sustainability_pie.png",
    dpi=300
)

plt.close()

print("Pie Chart Saved.")

# ----------------------------

plt.figure(figsize=(8,5))

category.plot(kind="bar")

plt.ylabel("Number of Estates")
plt.title("Sustainability Categories")

plt.tight_layout()

plt.savefig(
    "Results/sustainability_bar.png",
    dpi=300
)

plt.close()

print("Bar Chart Saved.")
# ============================================================
# TOP 10 SUSTAINABLE ESTATES
# ============================================================

top10 = df.sort_values(
    by="Sustainability_Score",
    ascending=False
).head(10)

print("\n" + "="*60)
print("TOP 10 SUSTAINABLE ESTATES")
print("="*60)

print(

top10[

[
"District",
"Coffee_Type",
"Sustainability_Score",
"Carbon_Footprint_tCO2e",
"Yield_kg_ha"
]

]

)

top10.to_csv(
    "Results/top10_sustainable.csv",
    index=False
)

print("Top 10 CSV Saved.")
# ============================================================
# BOTTOM 10 SUSTAINABLE ESTATES
# ============================================================

bottom10 = df.sort_values(
    by="Sustainability_Score"
).head(10)

print("\n" + "="*60)
print("BOTTOM 10 SUSTAINABLE ESTATES")
print("="*60)

print(

bottom10[

[
"District",
"Coffee_Type",
"Sustainability_Score",
"Carbon_Footprint_tCO2e",
"Yield_kg_ha"
]

]

)

bottom10.to_csv(
    "Results/bottom10_sustainable.csv",
    index=False
)

print("Bottom 10 CSV Saved.")
# ============================================================
# SCATTER PLOTS
# ============================================================

print("\nGenerating Scatter Plots...")

# ---------------- Sustainability vs Yield ----------------

plt.figure(figsize=(8,5))

plt.scatter(
    df["Sustainability_Score"],
    df["Yield_kg_ha"],
    alpha=0.5
)

plt.xlabel("Sustainability Score")
plt.ylabel("Yield (kg/ha)")
plt.title("Yield vs Sustainability Score")

plt.tight_layout()

plt.savefig(
    "Results/yield_vs_sustainability.png",
    dpi=300
)

plt.close()

print("Yield vs Sustainability Saved.")

# ---------------- Carbon vs Yield ----------------

plt.figure(figsize=(8,5))

plt.scatter(
    df["Carbon_Footprint_tCO2e"],
    df["Yield_kg_ha"],
    alpha=0.5
)

plt.xlabel("Carbon Footprint (tCO2e)")
plt.ylabel("Yield (kg/ha)")
plt.title("Yield vs Carbon Footprint")

plt.tight_layout()

plt.savefig(
    "Results/yield_vs_carbon.png",
    dpi=300
)

plt.close()

print("Yield vs Carbon Saved.")
# ============================================================
# CORRELATION HEATMAP
# ============================================================

print("\nGenerating Correlation Heatmap...")

corr = df[
    [
        "Yield_kg_ha",
        "Sustainability_Score",
        "Carbon_Footprint_tCO2e",
        "Bean_Quality_Score",
        "Soil_Moisture_%",
        "Pest_Severity_0_10",
        "Disease_Severity_0_10"
    ]
].corr()

plt.figure(figsize=(8,6))

plt.imshow(
    corr,
    cmap="coolwarm"
)

plt.xticks(
    range(len(corr.columns)),
    corr.columns,
    rotation=45
)

plt.yticks(
    range(len(corr.columns)),
    corr.columns
)

plt.colorbar()

plt.title("Sustainability Correlation Heatmap")

plt.tight_layout()

plt.savefig(
    "Results/sustainability_heatmap.png",
    dpi=300
)

plt.close()

print("Heatmap Saved.")
# ============================================================
# DISTRICT RANKING
# ============================================================

district_rank = df.groupby("District")[
    "Sustainability_Score"
].mean().sort_values(
    ascending=False
)

print("\n" + "="*60)
print("DISTRICT SUSTAINABILITY RANKING")
print("="*60)

print(district_rank)

district_rank.to_csv(
    "Results/district_sustainability_ranking.csv"
)

plt.figure(figsize=(8,5))

district_rank.plot(
    kind="bar"
)

plt.ylabel("Average Sustainability Score")
plt.title("District Sustainability Ranking")

plt.tight_layout()

plt.savefig(
    "Results/district_sustainability_ranking.png",
    dpi=300
)

plt.close()

print("District Ranking Saved.")

# ---------------- Carbon Ranking ----------------

carbon_rank = df.groupby("District")[
    "Carbon_Footprint_tCO2e"
].mean().sort_values()

carbon_rank.to_csv(
    "Results/district_carbon_ranking.csv"
)

plt.figure(figsize=(8,5))

carbon_rank.plot(
    kind="bar"
)

plt.ylabel("Carbon Footprint (tCO2e)")
plt.title("District Carbon Footprint Ranking")

plt.tight_layout()

plt.savefig(
    "Results/district_carbon_ranking.png",
    dpi=300
)

plt.close()

print("Carbon Ranking Saved.")
# ============================================================
# SUSTAINABILITY KPI DASHBOARD
# ============================================================

print("\n" + "="*60)
print("SUSTAINABILITY KPI DASHBOARD")
print("="*60)

excellent = (df["Sustainability_Category"]=="Excellent").sum()
good = (df["Sustainability_Category"]=="Good").sum()
moderate = (df["Sustainability_Category"]=="Moderate").sum()
poor = (df["Sustainability_Category"]=="Poor").sum()

print(f"Total Estates                 : {len(df)}")

print(f"Average Sustainability Score  : {df['Sustainability_Score'].mean():.2f}")
print(f"Highest Sustainability Score  : {df['Sustainability_Score'].max():.2f}")
print(f"Lowest Sustainability Score   : {df['Sustainability_Score'].min():.2f}")

print()

print(f"Average Carbon Footprint      : {df['Carbon_Footprint_tCO2e'].mean():.2f}")
print(f"Highest Carbon Footprint      : {df['Carbon_Footprint_tCO2e'].max():.2f}")
print(f"Lowest Carbon Footprint       : {df['Carbon_Footprint_tCO2e'].min():.2f}")

print()

print(f"Excellent Estates             : {excellent}")
print(f"Good Estates                  : {good}")
print(f"Moderate Estates              : {moderate}")
print(f"Poor Estates                  : {poor}")
# ============================================================
# COFFEE TYPE SUSTAINABILITY
# ============================================================

coffee_type = df.groupby("Coffee_Type")[

    [
        "Sustainability_Score",
        "Carbon_Footprint_tCO2e"
    ]

].mean().round(2)

print("\n" + "="*60)
print("COFFEE TYPE SUSTAINABILITY")
print("="*60)

print(coffee_type)

coffee_type.to_csv(
    "Results/coffee_type_sustainability.csv"
)

coffee_type["Sustainability_Score"].plot(
    kind="bar",
    figsize=(7,5)
)

plt.ylabel("Average Sustainability Score")
plt.title("Coffee Type Sustainability")

plt.tight_layout()

plt.savefig(
    "Results/coffee_type_sustainability.png",
    dpi=300
)

plt.close()

print("Coffee Type Sustainability Chart Saved.")
# ============================================================
# EXPORT QUALITY SUSTAINABILITY
# ============================================================

export = df.groupby("Export_Quality")[

    [
        "Sustainability_Score",
        "Carbon_Footprint_tCO2e"
    ]

].mean().round(2)

print("\n" + "="*60)
print("EXPORT QUALITY SUSTAINABILITY")
print("="*60)

print(export)

export.to_csv(
    "Results/export_sustainability.csv"
)

export["Sustainability_Score"].plot(
    kind="bar",
    figsize=(7,5)
)

plt.ylabel("Average Sustainability Score")
plt.title("Export Quality Sustainability")

plt.tight_layout()

plt.savefig(
    "Results/export_sustainability.png",
    dpi=300
)

plt.close()

print("Export Sustainability Chart Saved.")
# ============================================================
# FILES GENERATED
# ============================================================

print("\n")
print("="*60)
print("FILES GENERATED")
print("="*60)

print("CSV FILES")
print("--------------------------------------------")

print("Results/district_sustainability.csv")
print("Results/sustainability_category.csv")
print("Results/top10_sustainable.csv")
print("Results/bottom10_sustainable.csv")
print("Results/district_sustainability_ranking.csv")
print("Results/district_carbon_ranking.csv")
print("Results/coffee_type_sustainability.csv")
print("Results/export_sustainability.csv")

print()

print("CHARTS")
print("--------------------------------------------")

print("district_sustainability.png")
print("district_carbon.png")
print("sustainability_pie.png")
print("sustainability_bar.png")
print("yield_vs_sustainability.png")
print("yield_vs_carbon.png")
print("sustainability_heatmap.png")
print("district_sustainability_ranking.png")
print("district_carbon_ranking.png")
print("coffee_type_sustainability.png")
print("export_sustainability.png")

print("\n")
print("="*60)
print("SUSTAINABILITY DASHBOARD COMPLETED SUCCESSFULLY")
print("="*60)