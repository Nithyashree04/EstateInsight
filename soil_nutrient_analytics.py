# ============================================================
# COFFEE ESTATE ANALYTICS
# FILE : soil_nutrient_analytics.py
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
# SOIL NUTRIENT SUMMARY
# ============================================================

print("\n" + "="*60)
print("SOIL NUTRIENT SUMMARY")
print("="*60)

print(f"Average Zn (ppm)          : {df['Zn_ppm'].mean():.2f}")
print(f"Average Fe (ppm)          : {df['Fe_ppm'].mean():.2f}")
print(f"Average Mg (ppm)          : {df['Mg_ppm'].mean():.2f}")
print(f"Average S (ppm)           : {df['S_ppm'].mean():.2f}")
print(f"Average Soil Moisture (%) : {df['Soil_Moisture_%'].mean():.2f}")

print()

print(f"Maximum Zn : {df['Zn_ppm'].max():.2f}")
print(f"Maximum Fe : {df['Fe_ppm'].max():.2f}")
print(f"Maximum Mg : {df['Mg_ppm'].max():.2f}")
print(f"Maximum S  : {df['S_ppm'].max():.2f}")

print()

print(f"Minimum Zn : {df['Zn_ppm'].min():.2f}")
print(f"Minimum Fe : {df['Fe_ppm'].min():.2f}")
print(f"Minimum Mg : {df['Mg_ppm'].min():.2f}")
print(f"Minimum S  : {df['S_ppm'].min():.2f}")
# ============================================================
# NUTRIENT COMPARISON
# ============================================================

nutrient_summary = pd.DataFrame({

    "Nutrient":[
        "Zn",
        "Fe",
        "Mg",
        "S",
        "Soil Moisture"
    ],

    "Average":[

        df["Zn_ppm"].mean(),

        df["Fe_ppm"].mean(),

        df["Mg_ppm"].mean(),

        df["S_ppm"].mean(),

        df["Soil_Moisture_%"].mean()

    ]

})

print("\n")
print("="*60)
print("AVERAGE NUTRIENTS")
print("="*60)

print(nutrient_summary)

nutrient_summary.to_csv(

    "Results/soil_summary.csv",

    index=False

)

plt.figure(figsize=(9,5))

plt.bar(

    nutrient_summary["Nutrient"],

    nutrient_summary["Average"]

)

plt.title("Average Soil Nutrient Levels")

plt.ylabel("Average Value")

plt.tight_layout()

plt.savefig(

    "Results/soil_comparison.png",

    dpi=300

)

plt.close()

print("Soil Comparison Chart Saved.")
# ============================================================
# DISTRICT NUTRIENT ANALYSIS
# ============================================================

district_nutrients = df.groupby("District")[

    [
        "Zn_ppm",
        "Fe_ppm",
        "Mg_ppm",
        "S_ppm",
        "Soil_Moisture_%"
    ]

].mean().round(2)

print("\n" + "="*60)
print("DISTRICT NUTRIENT ANALYSIS")
print("="*60)

print(district_nutrients)

district_nutrients.to_csv(
    "Results/district_nutrients.csv"
)

# ---------------- District Nutrient Chart ----------------

district_nutrients.plot(
    kind="bar",
    figsize=(12,6)
)

plt.title("District-wise Average Nutrient Levels")
plt.ylabel("Average Value")

plt.tight_layout()

plt.savefig(
    "Results/district_nutrients.png",
    dpi=300
)

plt.close()

print("District Nutrient Chart Saved.")
# ============================================================
# NUTRIENT DEFICIENCY DETECTION
# ============================================================

print("\nCalculating Nutrient Status...")

def nutrient_status(row):

    deficiencies = 0

    if row["Zn_ppm"] < 2:
        deficiencies += 1

    if row["Fe_ppm"] < 10:
        deficiencies += 1

    if row["Mg_ppm"] < 40:
        deficiencies += 1

    if row["S_ppm"] < 8:
        deficiencies += 1

    if row["Soil_Moisture_%"] < 35:
        deficiencies += 1

    if deficiencies >= 2:
        return "Deficient"

    return "Healthy"

df["Nutrient_Status"] = df.apply(
    nutrient_status,
    axis=1
)

print("Nutrient Status Calculated.")

status_counts = df["Nutrient_Status"].value_counts()

print("\n")
print("="*60)
print("NUTRIENT STATUS")
print("="*60)

print(status_counts)

df.to_csv(
    "Results/nutrient_status.csv",
    index=False
)

print("Nutrient Status CSV Saved.")
# ============================================================
# HEALTHY vs DEFICIENT CHARTS
# ============================================================

# ---------------- Pie Chart ----------------

plt.figure(figsize=(7,7))

plt.pie(
    status_counts,
    labels=status_counts.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Nutrient Status Distribution")

plt.savefig(
    "Results/nutrient_status_pie.png",
    dpi=300
)

plt.close()

print("Pie Chart Saved.")

# ---------------- Bar Chart ----------------

plt.figure(figsize=(7,5))

status_counts.plot(kind="bar")

plt.title("Healthy vs Deficient Estates")
plt.ylabel("Number of Estates")

plt.tight_layout()

plt.savefig(
    "Results/nutrient_status_bar.png",
    dpi=300
)

plt.close()

print("Bar Chart Saved.")
# ============================================================
# NUTRIENT HEATMAP
# ============================================================

print("\nGenerating Correlation Heatmap...")

corr = df[

    [

        "Yield_kg_ha",

        "Zn_ppm",

        "Fe_ppm",

        "Mg_ppm",

        "S_ppm",

        "Soil_Moisture_%"

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

plt.title("Nutrient Correlation Heatmap")

plt.tight_layout()

plt.savefig(
    "Results/nutrient_heatmap.png",
    dpi=300
)

plt.close()

print("Heatmap Saved.")
# ============================================================
# YIELD vs NUTRIENTS
# ============================================================

print("\nGenerating Scatter Plots...")

# ---------------- Zn ----------------

plt.figure(figsize=(7,5))

plt.scatter(
    df["Zn_ppm"],
    df["Yield_kg_ha"],
    alpha=0.5
)

plt.xlabel("Zn (ppm)")
plt.ylabel("Yield (kg/ha)")
plt.title("Yield vs Zn")

plt.tight_layout()

plt.savefig(
    "Results/yield_vs_zn.png",
    dpi=300
)

plt.close()

print("Yield vs Zn Saved.")

# ---------------- Fe ----------------

plt.figure(figsize=(7,5))

plt.scatter(
    df["Fe_ppm"],
    df["Yield_kg_ha"],
    alpha=0.5
)

plt.xlabel("Fe (ppm)")
plt.ylabel("Yield (kg/ha)")
plt.title("Yield vs Fe")

plt.tight_layout()

plt.savefig(
    "Results/yield_vs_fe.png",
    dpi=300
)

plt.close()

print("Yield vs Fe Saved.")

# ---------------- Mg ----------------

plt.figure(figsize=(7,5))

plt.scatter(
    df["Mg_ppm"],
    df["Yield_kg_ha"],
    alpha=0.5
)

plt.xlabel("Mg (ppm)")
plt.ylabel("Yield (kg/ha)")
plt.title("Yield vs Mg")

plt.tight_layout()

plt.savefig(
    "Results/yield_vs_mg.png",
    dpi=300
)

plt.close()

print("Yield vs Mg Saved.")

# ---------------- Soil Moisture ----------------

plt.figure(figsize=(7,5))

plt.scatter(
    df["Soil_Moisture_%"],
    df["Yield_kg_ha"],
    alpha=0.5
)

plt.xlabel("Soil Moisture (%)")
plt.ylabel("Yield (kg/ha)")
plt.title("Yield vs Soil Moisture")

plt.tight_layout()

plt.savefig(
    "Results/yield_vs_soil_moisture.png",
    dpi=300
)

plt.close()

print("Yield vs Soil Moisture Saved.")
# ============================================================
# TOP 10 NUTRIENT RICH ESTATES
# ============================================================

print("\n" + "="*60)
print("TOP 10 NUTRIENT RICH ESTATES")
print("="*60)

df["Nutrient_Score"] = (

    df["Zn_ppm"] +

    df["Fe_ppm"] +

    df["Mg_ppm"] +

    df["S_ppm"] +

    df["Soil_Moisture_%"]

)

top10 = df.sort_values(

    by="Nutrient_Score",

    ascending=False

).head(10)

print(

    top10[

        [

            "District",

            "Coffee_Type",

            "Zn_ppm",

            "Fe_ppm",

            "Mg_ppm",

            "S_ppm",

            "Soil_Moisture_%",

            "Nutrient_Score"

        ]

    ]

)

top10.to_csv(

    "Results/top10_nutrient_estates.csv",

    index=False

)

print("Top 10 CSV Saved.")
# ============================================================
# DISTRICT NUTRIENT RANKING
# ============================================================

district_rank = df.groupby("District")[

    "Nutrient_Score"

].mean().sort_values(

    ascending=False

)

print("\n" + "="*60)
print("DISTRICT NUTRIENT RANKING")
print("="*60)

print(district_rank)

district_rank.to_csv(

    "Results/district_nutrient_ranking.csv"

)

plt.figure(figsize=(8,5))

district_rank.plot(kind="bar")

plt.title("District Nutrient Ranking")
plt.ylabel("Average Nutrient Score")

plt.tight_layout()

plt.savefig(

    "Results/district_nutrient_ranking.png",

    dpi=300

)

plt.close()

print("District Ranking Saved.")
# ============================================================
# NUTRIENT KPI DASHBOARD
# ============================================================

print("\n" + "="*60)
print("NUTRIENT KPI DASHBOARD")
print("="*60)

healthy_count = (df["Nutrient_Status"] == "Healthy").sum()
deficient_count = (df["Nutrient_Status"] == "Deficient").sum()

print(f"Total Estates              : {len(df)}")

print(f"Average Zn (ppm)           : {df['Zn_ppm'].mean():.2f}")
print(f"Average Fe (ppm)           : {df['Fe_ppm'].mean():.2f}")
print(f"Average Mg (ppm)           : {df['Mg_ppm'].mean():.2f}")
print(f"Average S (ppm)            : {df['S_ppm'].mean():.2f}")
print(f"Average Soil Moisture (%)  : {df['Soil_Moisture_%'].mean():.2f}")

print()

print(f"Healthy Estates            : {healthy_count}")
print(f"Deficient Estates          : {deficient_count}")

print()

print(f"Highest Nutrient Score     : {df['Nutrient_Score'].max():.2f}")
print(f"Average Nutrient Score     : {df['Nutrient_Score'].mean():.2f}")
print(f"Lowest Nutrient Score      : {df['Nutrient_Score'].min():.2f}")
# ============================================================
# FILES GENERATED
# ============================================================

print("\n")
print("="*60)
print("FILES GENERATED")
print("="*60)

print("CSV FILES")
print("--------------------------------------------")

print("Results/soil_summary.csv")
print("Results/district_nutrients.csv")
print("Results/nutrient_status.csv")
print("Results/top10_nutrient_estates.csv")
print("Results/district_nutrient_ranking.csv")

print()

print("CHARTS")
print("--------------------------------------------")

print("soil_comparison.png")
print("district_nutrients.png")
print("nutrient_status_bar.png")
print("nutrient_status_pie.png")
print("nutrient_heatmap.png")
print("yield_vs_zn.png")
print("yield_vs_fe.png")
print("yield_vs_mg.png")
print("yield_vs_soil_moisture.png")
print("district_nutrient_ranking.png")

print("\n")
print("="*60)
print("SOIL NUTRIENT ANALYTICS COMPLETED SUCCESSFULLY")
print("="*60)