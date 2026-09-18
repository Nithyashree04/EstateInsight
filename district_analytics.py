import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("Results", exist_ok=True)

print("="*60)
print("LOADING DATASET")
print("="*60)

df = pd.read_excel(
    r"C:\Users\Admin\OneDrive\Desktop\Sujay Project\Karnataka_Coffee_Cleaned.xlsx"
)

print("Dataset Shape :", df.shape)
print("\n")
print("="*60)
print("DISTRICT SUMMARY")
print("="*60)

temp_cols = [c for c in df.columns if "Temp_" in c]
rain_cols = [c for c in df.columns if "Rain_" in c]

df["Average_Temperature"] = df[temp_cols].mean(axis=1)
df["Average_Rainfall"] = df[rain_cols].mean(axis=1)

district_summary = df.groupby("District").agg({

    "Yield_kg_ha":"mean",
    "Bean_Quality_Score":"mean",
    "Average_Rainfall":"mean",
    "Average_Temperature":"mean",
    "Sustainability_Score":"mean",
    "Carbon_Footprint_tCO2e":"mean",
    "Pest_Severity_0_10":"mean",
    "Disease_Severity_0_10":"mean",
    "Soil_Moisture_%":"mean",
    "Market_Price_INR_kg":"mean"

}).round(2)

print(district_summary)

district_summary.to_csv(
    "Results/district_summary.csv"
)

print("District Summary Saved.")
print("\n")
print("="*60)
print("DISTRICT RANKINGS")
print("="*60)

ranking = pd.DataFrame({

    "Highest Yield":
        district_summary["Yield_kg_ha"],

    "Best Bean Quality":
        district_summary["Bean_Quality_Score"],

    "Best Sustainability":
        district_summary["Sustainability_Score"],

    "Lowest Carbon":
        -district_summary["Carbon_Footprint_tCO2e"]

})

print(ranking)

ranking.to_csv(
    "Results/district_rankings.csv"
)

print("Ranking CSV Saved.")
district_summary["Yield_kg_ha"].plot(
    kind="bar",
    figsize=(8,5)
)

plt.title("Average Yield by District")
plt.ylabel("Yield (kg/ha)")
plt.tight_layout()

plt.savefig(
    "Results/district_yield.png",
    dpi=300
)

plt.close()

print("Yield Chart Saved.")
district_summary["Bean_Quality_Score"].plot(
    kind="bar",
    figsize=(8,5)
)

plt.title("Bean Quality by District")
plt.tight_layout()

plt.savefig(
    "Results/district_quality.png",
    dpi=300
)

plt.close()

print("Quality Chart Saved.")
district_summary["Sustainability_Score"].plot(
    kind="bar",
    figsize=(8,5)
)

plt.title("Sustainability by District")

plt.tight_layout()

plt.savefig(
    "Results/district_sustainability.png",
    dpi=300
)

plt.close()

print("Sustainability Chart Saved.")
district_summary["Average_Rainfall"].plot(
    kind="bar",
    figsize=(8,5)
)

plt.title("Average Rainfall by District")

plt.tight_layout()

plt.savefig(
    "Results/district_rainfall.png",
    dpi=300
)

plt.close()

print("Rainfall Chart Saved.")
district_summary["Average_Temperature"].plot(
    kind="bar",
    figsize=(8,5)
)

plt.title("Average Temperature by District")

plt.tight_layout()

plt.savefig(
    "Results/district_temperature.png",
    dpi=300
)

plt.close()

print("Temperature Chart Saved.")
district_summary["Pest_Severity_0_10"].plot(
    kind="bar",
    figsize=(8,5)
)

plt.title("Pest Severity by District")

plt.tight_layout()

plt.savefig(
    "Results/district_pest.png",
    dpi=300
)

plt.close()

print("Pest Chart Saved.")
district_summary["Disease_Severity_0_10"].plot(
    kind="bar",
    figsize=(8,5)
)

plt.title("Disease Severity by District")

plt.tight_layout()

plt.savefig(
    "Results/district_disease.png",
    dpi=300
)

plt.close()

print("Disease Chart Saved.")
district_summary["Carbon_Footprint_tCO2e"].plot(
    kind="bar",
    figsize=(8,5)
)

plt.title("Carbon Footprint by District")

plt.tight_layout()

plt.savefig(
    "Results/district_carbon.png",
    dpi=300
)

plt.close()

print("Carbon Chart Saved.")
print("\n")
print("="*60)
print("DISTRICT KPI DASHBOARD")
print("="*60)

print("Total Districts :", len(district_summary))

print(
    "Highest Yield District :",
    district_summary["Yield_kg_ha"].idxmax()
)

print(
    "Highest Quality District :",
    district_summary["Bean_Quality_Score"].idxmax()
)

print(
    "Highest Sustainability :",
    district_summary["Sustainability_Score"].idxmax()
)

print(
    "Lowest Carbon District :",
    district_summary["Carbon_Footprint_tCO2e"].idxmin()
)

print(
    "Highest Rainfall District :",
    district_summary["Average_Rainfall"].idxmax()
)
district_summary["Overall_Score"] = (

      district_summary["Yield_kg_ha"].rank()

    + district_summary["Bean_Quality_Score"].rank()

    + district_summary["Sustainability_Score"].rank()

    + district_summary["Average_Rainfall"].rank()

)

best = district_summary["Overall_Score"].idxmax()

print("\n")
print("="*60)
print("BEST OVERALL DISTRICT")
print("="*60)

print("Best District :", best)

district_summary.to_csv(
    "Results/district_summary.csv"
)
print("\n")
print("="*60)
print("FILES GENERATED")
print("="*60)

print("CSV FILES")
print("-------------------------------------")
print("Results/district_summary.csv")
print("Results/district_rankings.csv")

print("\nCHARTS")
print("-------------------------------------")
print("district_yield.png")
print("district_quality.png")
print("district_sustainability.png")
print("district_rainfall.png")
print("district_temperature.png")
print("district_pest.png")
print("district_disease.png")
print("district_carbon.png")

print("\n")
print("="*60)
print("DISTRICT ANALYTICS COMPLETED SUCCESSFULLY")
print("="*60)