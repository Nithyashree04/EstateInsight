# ============================================================
# COFFEE ESTATE ANALYTICS
# FILE : export_quality_analysis.py
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import os

print("="*60)
print("LOADING DATASET")
print("="*60)

df = pd.read_excel(
    r"C:\Users\Admin\OneDrive\Desktop\Sujay Project\Karnataka_Coffee_Cleaned.xlsx"
)

os.makedirs("Results", exist_ok=True)

print("Dataset Shape :", df.shape)
print("\n")
print("="*60)
print("EXPORT QUALITY SUMMARY")
print("="*60)

summary = df.groupby("Export_Quality").agg({

    "Yield_kg_ha":"mean",
    "Bean_Quality_Score":"mean",
    "Market_Price_INR_kg":"mean",
    "Sustainability_Score":"mean",
    "Carbon_Footprint_tCO2e":"mean",
    "Pest_Severity_0_10":"mean",
    "Disease_Severity_0_10":"mean",
    "Soil_Moisture_%":"mean"

}).round(2)

print(summary)

summary.to_csv(
    "Results/export_quality_summary.csv"
)

print("Summary Saved.")
print("\n")
print("="*60)
print("EXPORT QUALITY RANKINGS")
print("="*60)

ranking = pd.DataFrame({

    "Higher Yield":
        summary["Yield_kg_ha"],

    "Better Quality":
        summary["Bean_Quality_Score"],

    "Higher Price":
        summary["Market_Price_INR_kg"],

    "Better Sustainability":
        summary["Sustainability_Score"],

    "Lower Carbon":
        -summary["Carbon_Footprint_tCO2e"],

    "Lower Pest":
        -summary["Pest_Severity_0_10"],

    "Lower Disease":
        -summary["Disease_Severity_0_10"]

})

print(ranking)

ranking.to_csv(
    "Results/export_quality_rankings.csv"
)

print("Ranking Saved.")
summary["Yield_kg_ha"].plot(kind="bar",figsize=(7,5))

plt.title("Yield by Export Quality")
plt.ylabel("Yield (kg/ha)")
plt.tight_layout()

plt.savefig(
    "Results/export_yield.png",
    dpi=300
)

plt.close()

print("Yield Chart Saved.")
summary["Bean_Quality_Score"].plot(kind="bar",figsize=(7,5))

plt.title("Bean Quality")

plt.tight_layout()

plt.savefig(
    "Results/export_quality_score.png",
    dpi=300
)

plt.close()

print("Quality Chart Saved.")
summary["Market_Price_INR_kg"].plot(kind="bar",figsize=(7,5))

plt.title("Market Price")

plt.tight_layout()

plt.savefig(
    "Results/export_market_price.png",
    dpi=300
)

plt.close()

print("Market Price Chart Saved.")
summary["Sustainability_Score"].plot(kind="bar",figsize=(7,5))

plt.title("Sustainability")

plt.tight_layout()

plt.savefig(
    "Results/export_sustainability.png",
    dpi=300
)

plt.close()

print("Sustainability Chart Saved.")
summary["Carbon_Footprint_tCO2e"].plot(kind="bar",figsize=(7,5))

plt.title("Carbon Footprint")

plt.tight_layout()

plt.savefig(
    "Results/export_carbon.png",
    dpi=300
)

plt.close()

print("Carbon Chart Saved.")
summary["Pest_Severity_0_10"].plot(kind="bar",figsize=(7,5))

plt.title("Pest Severity")

plt.tight_layout()

plt.savefig(
    "Results/export_pest.png",
    dpi=300
)

plt.close()

summary["Disease_Severity_0_10"].plot(kind="bar",figsize=(7,5))

plt.title("Disease Severity")

plt.tight_layout()

plt.savefig(
    "Results/export_disease.png",
    dpi=300
)

plt.close()

print("Pest & Disease Charts Saved.")
summary["Soil_Moisture_%"].plot(kind="bar",figsize=(7,5))

plt.title("Soil Moisture")

plt.tight_layout()

plt.savefig(
    "Results/export_soil_moisture.png",
    dpi=300
)

plt.close()

print("Soil Moisture Chart Saved.")
export = df["Export_Quality"].value_counts()

export.plot(
    kind="pie",
    autopct="%1.1f%%",
    figsize=(6,6)
)

plt.ylabel("")
plt.title("Export Quality Distribution")

plt.tight_layout()

plt.savefig(
    "Results/export_quality_pie.png",
    dpi=300
)

plt.close()

print("Pie Chart Saved.")
print("\n")
print("="*60)
print("EXPORT QUALITY KPI")
print("="*60)

print("Export Estates :", len(df[df["Export_Quality"]=="Yes"]))

print("Non Export Estates :", len(df[df["Export_Quality"]=="No"]))

print()

print(summary)
score = {

    "Yes":0,
    "No":0

}

metrics=[

("Yield_kg_ha",True),
("Bean_Quality_Score",True),
("Market_Price_INR_kg",True),
("Sustainability_Score",True),
("Carbon_Footprint_tCO2e",False),
("Pest_Severity_0_10",False),
("Disease_Severity_0_10",False)

]

for metric,higher in metrics:

    if higher:

        winner = summary[metric].idxmax()

    else:

        winner = summary[metric].idxmin()

    score[winner]+=1

overall=max(score,key=score.get)

print("\n")
print("="*60)
print("OVERALL BEST EXPORT CATEGORY")
print("="*60)

print(overall)

print(score)
print("\n")
print("="*60)
print("FILES GENERATED")
print("="*60)

print("CSV FILES")
print("--------------------------------")

print("Results/export_quality_summary.csv")
print("Results/export_quality_rankings.csv")

print()

print("CHARTS")
print("--------------------------------")

print("export_yield.png")
print("export_quality_score.png")
print("export_market_price.png")
print("export_sustainability.png")
print("export_carbon.png")
print("export_pest.png")
print("export_disease.png")
print("export_soil_moisture.png")
print("export_quality_pie.png")

print("\n")
print("="*60)
print("EXPORT QUALITY ANALYSIS COMPLETED SUCCESSFULLY")
print("="*60)