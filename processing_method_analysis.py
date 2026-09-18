# ============================================================
# COFFEE ESTATE ANALYTICS
# FILE : processing_method_analysis.py
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import os

print("=" * 60)
print("LOADING DATASET")
print("=" * 60)

df = pd.read_excel(
    r"C:\Users\Admin\OneDrive\Desktop\Sujay Project\Karnataka_Coffee_Cleaned.xlsx"
)

os.makedirs("Results", exist_ok=True)

print("Dataset Shape :", df.shape)

# ============================================================
# PROCESSING METHOD SUMMARY
# ============================================================

print("\n")
print("=" * 60)
print("PROCESSING METHOD SUMMARY")
print("=" * 60)

summary = df.groupby("Processing_Method").agg({
    "Yield_kg_ha": "mean",
    "Bean_Quality_Score": "mean",
    "Market_Price_INR_kg": "mean",
    "Sustainability_Score": "mean",
    "Carbon_Footprint_tCO2e": "mean",
    "Pest_Severity_0_10": "mean",
    "Disease_Severity_0_10": "mean",
    "Soil_Moisture_%": "mean"
}).round(2)

print(summary)

summary.to_csv("Results/processing_method_summary.csv")

print("Summary Saved.")

# ============================================================
# RANKINGS
# ============================================================

print("\n")
print("=" * 60)
print("PROCESSING METHOD RANKINGS")
print("=" * 60)

ranking = pd.DataFrame({

    "Higher Yield": summary["Yield_kg_ha"],
    "Better Quality": summary["Bean_Quality_Score"],
    "Higher Price": summary["Market_Price_INR_kg"],
    "Better Sustainability": summary["Sustainability_Score"],
    "Lower Carbon": -summary["Carbon_Footprint_tCO2e"],
    "Lower Pest": -summary["Pest_Severity_0_10"],
    "Lower Disease": -summary["Disease_Severity_0_10"]

})

print(ranking)

ranking.to_csv("Results/processing_method_rankings.csv")

print("Ranking Saved.")

# ============================================================
# YIELD
# ============================================================

summary["Yield_kg_ha"].plot(kind="bar", figsize=(8,5))
plt.title("Yield by Processing Method")
plt.ylabel("Yield (kg/ha)")
plt.tight_layout()
plt.savefig("Results/processing_yield.png", dpi=300)
plt.close()

print("Yield Chart Saved.")

# ============================================================
# QUALITY
# ============================================================

summary["Bean_Quality_Score"].plot(kind="bar", figsize=(8,5))
plt.title("Bean Quality")
plt.tight_layout()
plt.savefig("Results/processing_quality.png", dpi=300)
plt.close()

print("Quality Chart Saved.")

# ============================================================
# MARKET PRICE
# ============================================================

summary["Market_Price_INR_kg"].plot(kind="bar", figsize=(8,5))
plt.title("Market Price")
plt.tight_layout()
plt.savefig("Results/processing_market_price.png", dpi=300)
plt.close()

print("Market Price Chart Saved.")

# ============================================================
# SUSTAINABILITY
# ============================================================

summary["Sustainability_Score"].plot(kind="bar", figsize=(8,5))
plt.title("Sustainability Score")
plt.tight_layout()
plt.savefig("Results/processing_sustainability.png", dpi=300)
plt.close()

print("Sustainability Chart Saved.")

# ============================================================
# CARBON FOOTPRINT
# ============================================================

summary["Carbon_Footprint_tCO2e"].plot(kind="bar", figsize=(8,5))
plt.title("Carbon Footprint")
plt.tight_layout()
plt.savefig("Results/processing_carbon.png", dpi=300)
plt.close()

print("Carbon Chart Saved.")

# ============================================================
# PEST
# ============================================================

summary["Pest_Severity_0_10"].plot(kind="bar", figsize=(8,5))
plt.title("Pest Severity")
plt.tight_layout()
plt.savefig("Results/processing_pest.png", dpi=300)
plt.close()

# ============================================================
# DISEASE
# ============================================================

summary["Disease_Severity_0_10"].plot(kind="bar", figsize=(8,5))
plt.title("Disease Severity")
plt.tight_layout()
plt.savefig("Results/processing_disease.png", dpi=300)
plt.close()

print("Pest & Disease Charts Saved.")

# ============================================================
# SOIL MOISTURE
# ============================================================

summary["Soil_Moisture_%"].plot(kind="bar", figsize=(8,5))
plt.title("Soil Moisture")
plt.tight_layout()
plt.savefig("Results/processing_soil_moisture.png", dpi=300)
plt.close()

print("Soil Moisture Chart Saved.")

# ============================================================
# PROCESSING METHOD DISTRIBUTION
# ============================================================

processing = df["Processing_Method"].value_counts()

processing.plot(
    kind="pie",
    autopct="%1.1f%%",
    figsize=(6,6)
)

plt.ylabel("")
plt.title("Processing Method Distribution")
plt.tight_layout()
plt.savefig("Results/processing_method_pie.png", dpi=300)
plt.close()

print("Pie Chart Saved.")

# ============================================================
# KPI
# ============================================================

print("\n")
print("=" * 60)
print("PROCESSING METHOD KPI")
print("=" * 60)

print("Washed Estates :", len(df[df["Processing_Method"] == "Washed"]))
print("Natural Estates :", len(df[df["Processing_Method"] == "Natural"]))
print("Honey Estates :", len(df[df["Processing_Method"] == "Honey"]))

print()
print(summary)

# ============================================================
# BEST PROCESSING METHOD
# ============================================================

score = {}

for method in summary.index:
    score[method] = 0

metrics = [

    ("Yield_kg_ha", True),
    ("Bean_Quality_Score", True),
    ("Market_Price_INR_kg", True),
    ("Sustainability_Score", True),
    ("Carbon_Footprint_tCO2e", False),
    ("Pest_Severity_0_10", False),
    ("Disease_Severity_0_10", False)

]

for metric, higher in metrics:

    if higher:
        winner = summary[metric].idxmax()
    else:
        winner = summary[metric].idxmin()

    score[winner] += 1

overall = max(score, key=score.get)

print("\n")
print("=" * 60)
print("BEST PROCESSING METHOD")
print("=" * 60)

print("Overall Best :", overall)

print("\nScores")
print(score)

# ============================================================
# FILES GENERATED
# ============================================================

print("\n")
print("=" * 60)
print("FILES GENERATED")
print("=" * 60)

print("CSV FILES")
print("--------------------------------")
print("Results/processing_method_summary.csv")
print("Results/processing_method_rankings.csv")

print("\nCHARTS")
print("--------------------------------")
print("processing_yield.png")
print("processing_quality.png")
print("processing_market_price.png")
print("processing_sustainability.png")
print("processing_carbon.png")
print("processing_pest.png")
print("processing_disease.png")
print("processing_soil_moisture.png")
print("processing_method_pie.png")

print("\n")
print("=" * 60)
print("PROCESSING METHOD ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 60)