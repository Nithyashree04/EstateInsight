# ============================================================
# COFFEE ESTATE ANALYTICS
# FILE : coffee_type_comparison.py
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import os

print("="*60)
print("LOADING DATASET")
print("="*60)

df = pd.read_excel(
    r"C:\Users\Admin\OneDrive\Desktop\Sujay Project\Finaldataset1.xlsx"
)

os.makedirs("Results", exist_ok=True)

print("Dataset Shape :", df.shape)
print("\n")
print("="*60)
print("COFFEE TYPE SUMMARY")
print("="*60)

summary = df.groupby("Coffee_Type").agg({

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
    "Results/coffee_type_summary.csv"
)

print("Coffee Type Summary Saved.")
print("\n")
print("="*60)
print("COFFEE TYPE RANKINGS")
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
    "Results/coffee_type_rankings.csv"
)

print("Ranking CSV Saved.")
summary["Yield_kg_ha"].plot(

    kind="bar",
    figsize=(7,5)

)

plt.title("Average Yield by Coffee Type")
plt.ylabel("Yield (kg/ha)")
plt.tight_layout()

plt.savefig(
    "Results/yield_comparison.png",
    dpi=300
)

plt.close()

print("Yield Comparison Saved.")
summary["Bean_Quality_Score"].plot(

    kind="bar",
    figsize=(7,5)

)

plt.title("Bean Quality Comparison")
plt.ylabel("Quality Score")

plt.tight_layout()

plt.savefig(
    "Results/quality_comparison.png",
    dpi=300
)

plt.close()

print("Quality Comparison Saved.")
summary["Market_Price_INR_kg"].plot(

    kind="bar",
    figsize=(7,5)

)

plt.title("Market Price Comparison")
plt.ylabel("Price (INR/kg)")

plt.tight_layout()

plt.savefig(
    "Results/market_price_comparison.png",
    dpi=300
)

plt.close()

print("Market Price Comparison Saved.")
summary["Sustainability_Score"].plot(

    kind="bar",
    figsize=(7,5)

)

plt.title("Sustainability Comparison")
plt.ylabel("Score")

plt.tight_layout()

plt.savefig(
    "Results/sustainability_comparison.png",
    dpi=300
)

plt.close()

print("Sustainability Comparison Saved.")
summary["Carbon_Footprint_tCO2e"].plot(

    kind="bar",
    figsize=(7,5)

)

plt.title("Carbon Footprint Comparison")
plt.ylabel("tCO2e")

plt.tight_layout()

plt.savefig(
    "Results/carbon_comparison.png",
    dpi=300
)

plt.close()

print("Carbon Comparison Saved.")
summary["Pest_Severity_0_10"].plot(kind="bar",figsize=(7,5))

plt.title("Pest Severity Comparison")

plt.tight_layout()

plt.savefig(
    "Results/pest_comparison.png",
    dpi=300
)

plt.close()

summary["Disease_Severity_0_10"].plot(kind="bar",figsize=(7,5))

plt.title("Disease Severity Comparison")

plt.tight_layout()

plt.savefig(
    "Results/disease_comparison.png",
    dpi=300
)

plt.close()

print("Pest & Disease Charts Saved.")
summary["Pest_Severity_0_10"].plot(kind="bar",figsize=(7,5))

plt.title("Pest Severity Comparison")

plt.tight_layout()

plt.savefig(
    "Results/pest_comparison.png",
    dpi=300
)

plt.close()

summary["Disease_Severity_0_10"].plot(kind="bar",figsize=(7,5))

plt.title("Disease Severity Comparison")

plt.tight_layout()

plt.savefig(
    "Results/disease_comparison.png",
    dpi=300
)

plt.close()

print("Pest & Disease Charts Saved.")
summary["Soil_Moisture_%"].plot(

    kind="bar",
    figsize=(7,5)

)

plt.title("Soil Moisture Comparison")

plt.tight_layout()

plt.savefig(
    "Results/soil_moisture_comparison.png",
    dpi=300
)

plt.close()

print("Soil Moisture Chart Saved.")
coffee = df["Coffee_Type"].value_counts()

coffee.plot(

    kind="pie",
    autopct="%1.1f%%",
    figsize=(6,6)

)

plt.ylabel("")

plt.title("Coffee Type Distribution")

plt.tight_layout()

plt.savefig(
    "Results/coffee_type_pie.png",
    dpi=300
)

plt.close()

print("Pie Chart Saved.")
print("\n")
print("="*60)
print("COFFEE TYPE KPI")
print("="*60)

print("Arabica Estates :", len(df[df["Coffee_Type"]=="Arabica"]))

print("Robusta Estates :", len(df[df["Coffee_Type"]=="Robusta"]))

print()

print(summary)
score = {

    "Arabica":0,
    "Robusta":0

}

metrics = [

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

overall = max(score,key=score.get)

print("\n")
print("="*60)
print("OVERALL BEST COFFEE TYPE")
print("="*60)

print(overall)

print()

print("Score")

print(score)
print("\n")
print("="*60)
print("FILES GENERATED")
print("="*60)

print("CSV FILES")
print("-----------------------------------")

print("Results/coffee_type_summary.csv")
print("Results/coffee_type_rankings.csv")

print()

print("CHARTS")
print("-----------------------------------")

print("yield_comparison.png")
print("quality_comparison.png")
print("market_price_comparison.png")
print("sustainability_comparison.png")
print("carbon_comparison.png")
print("pest_comparison.png")
print("disease_comparison.png")
print("soil_moisture_comparison.png")
print("coffee_type_pie.png")

print("\n")
print("="*60)
print("COFFEE TYPE COMPARISON COMPLETED SUCCESSFULLY")
print("="*60)