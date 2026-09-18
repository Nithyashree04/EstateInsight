# ============================================================
# COFFEE ESTATE ANALYTICS
# FILE : climate_analytics.py
# ============================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# CREATE RESULTS FOLDER
# ============================================================

os.makedirs("Results", exist_ok=True)
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
# CLIMATE COLUMNS
# ============================================================

months = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

temperature_columns = [
    "Temp_Jan_C",
    "Temp_Feb_C",
    "Temp_Mar_C",
    "Temp_Apr_C",
    "Temp_May_C",
    "Temp_Jun_C",
    "Temp_Jul_C",
    "Temp_Aug_C",
    "Temp_Sep_C",
    "Temp_Oct_C",
    "Temp_Nov_C",
    "Temp_Dec_C"
]

rainfall_columns = [
    "Rain_Jan_mm",
    "Rain_Feb_mm",
    "Rain_Mar_mm",
    "Rain_Apr_mm",
    "Rain_May_mm",
    "Rain_Jun_mm",
    "Rain_Jul_mm",
    "Rain_Aug_mm",
    "Rain_Sep_mm",
    "Rain_Oct_mm",
    "Rain_Nov_mm",
    "Rain_Dec_mm"
]
# ============================================================
# MONTHLY CLIMATE ANALYSIS
# ============================================================

print("\nCalculating Climate Statistics...")

avg_temperature = df[temperature_columns].mean()
avg_rainfall = df[rainfall_columns].mean()

annual_temperature = avg_temperature.mean()
annual_rainfall = avg_rainfall.sum()

hottest_month = avg_temperature.idxmax()
coolest_month = avg_temperature.idxmin()

wettest_month = avg_rainfall.idxmax()
driest_month = avg_rainfall.idxmin()

print("Climate Statistics Calculated.")
# ============================================================
# YEARLY CLIMATE SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("YEARLY CLIMATE SUMMARY")
print("=" * 60)

print(f"Average Annual Temperature : {annual_temperature:.2f} °C")
print(f"Average Annual Rainfall    : {annual_rainfall:.2f} mm")

print()

print("Hottest Month :", hottest_month.replace("Temp_", "").replace("_C", ""))
print("Coolest Month :", coolest_month.replace("Temp_", "").replace("_C", ""))

print()

print("Wettest Month :", wettest_month.replace("Rain_", "").replace("_mm", ""))
print("Driest Month  :", driest_month.replace("Rain_", "").replace("_mm", ""))
# ============================================================
# SAVE SUMMARY
# ============================================================

summary = pd.DataFrame({

    "Metric": [

        "Average Annual Temperature",

        "Average Annual Rainfall",

        "Hottest Month",

        "Coolest Month",

        "Wettest Month",

        "Driest Month"

    ],

    "Value": [

        round(annual_temperature, 2),

        round(annual_rainfall, 2),

        hottest_month,

        coolest_month,

        wettest_month,

        driest_month

    ]

})

summary.to_csv(

    "Results/climate_summary.csv",

    index=False

)

print("\nClimate Summary Saved.")
# ============================================================
# DISTRICT CLIMATE ANALYSIS
# ============================================================

print("\nCalculating District Climate Statistics...")

district_temperature = (
    df.groupby("District")[temperature_columns]
      .mean()
      .mean(axis=1)
)

district_rainfall = (
    df.groupby("District")[rainfall_columns]
      .mean()
      .sum(axis=1)
)

district_climate = pd.DataFrame({
    "Average_Temperature_C": district_temperature,
    "Average_Rainfall_mm": district_rainfall
})

district_climate = district_climate.round(2)

print("\n" + "=" * 60)
print("DISTRICT CLIMATE")
print("=" * 60)

print(district_climate)

district_climate.to_csv(
    "Results/district_climate.csv"
)

print("\nDistrict Climate CSV Saved.")
# ============================================================
# MONTHLY TEMPERATURE LINE CHART
# ============================================================

plt.figure(figsize=(12,6))

plt.plot(
    months,
    avg_temperature.values,
    marker="o",
    linewidth=3
)

plt.title("Average Monthly Temperature")
plt.xlabel("Month")
plt.ylabel("Temperature (°C)")
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "Results/monthly_temperature.png",
    dpi=300
)

plt.close()

print("Temperature Line Chart Saved.")
# ============================================================
# MONTHLY RAINFALL LINE CHART
# ============================================================

plt.figure(figsize=(12,6))

plt.plot(
    months,
    avg_rainfall.values,
    marker="o",
    linewidth=3
)

plt.title("Average Monthly Rainfall")
plt.xlabel("Month")
plt.ylabel("Rainfall (mm)")
plt.grid(True)

plt.tight_layout()

plt.savefig(
    "Results/monthly_rainfall.png",
    dpi=300
)

plt.close()

print("Rainfall Line Chart Saved.")
# ============================================================
# TEMPERATURE BOXPLOT
# ============================================================

plt.figure(figsize=(12,6))

plt.boxplot(
    [df[col] for col in temperature_columns],
    tick_labels=months
)

plt.title("Monthly Temperature Distribution")
plt.xlabel("Month")
plt.ylabel("Temperature (°C)")

plt.tight_layout()

plt.savefig(
    "Results/temperature_boxplot.png",
    dpi=300
)

plt.close()

print("Temperature Box Plot Saved.")
# ============================================================
# RAINFALL BOXPLOT
# ============================================================

plt.figure(figsize=(12,6))

plt.boxplot(
    [df[col] for col in rainfall_columns],
    tick_labels=months
)

plt.title("Monthly Rainfall Distribution")
plt.xlabel("Month")
plt.ylabel("Rainfall (mm)")

plt.tight_layout()

plt.savefig(
    "Results/rainfall_boxplot.png",
    dpi=300
)

plt.close()

print("Rainfall Box Plot Saved.")
# ============================================================
# DISTRICT TEMPERATURE
# ============================================================

plt.figure(figsize=(8,5))

district_temperature.sort_values().plot(
    kind="bar"
)

plt.title("Average Temperature by District")
plt.xlabel("District")
plt.ylabel("Temperature (°C)")

plt.tight_layout()

plt.savefig(
    "Results/district_temperature.png",
    dpi=300
)

plt.close()

print("District Temperature Chart Saved.")
# ============================================================
# DISTRICT RAINFALL
# ============================================================

plt.figure(figsize=(8,5))

district_rainfall.sort_values().plot(
    kind="bar"
)

plt.title("Average Rainfall by District")
plt.xlabel("District")
plt.ylabel("Rainfall (mm)")

plt.tight_layout()

plt.savefig(
    "Results/district_rainfall.png",
    dpi=300
)

plt.close()

print("District Rainfall Chart Saved.")
# ============================================================
# CLIMATE CORRELATION HEATMAP
# ============================================================

climate_data = df[
    temperature_columns +
    rainfall_columns
]

correlation = climate_data.corr()

plt.figure(figsize=(14,10))

plt.imshow(
    correlation,
    aspect="auto"
)

plt.colorbar()

plt.xticks(
    range(len(correlation.columns)),
    correlation.columns,
    rotation=90,
    fontsize=7
)

plt.yticks(
    range(len(correlation.columns)),
    correlation.columns,
    fontsize=7
)

plt.title("Climate Correlation Heatmap")

plt.tight_layout()

plt.savefig(
    "Results/climate_heatmap.png",
    dpi=300
)

plt.close()

print("Climate Heatmap Saved.")
# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("FILES GENERATED")
print("=" * 60)

print("Results/climate_summary.csv")
print("Results/district_climate.csv")
print("Results/monthly_temperature.png")
print("Results/monthly_rainfall.png")
print("Results/temperature_boxplot.png")
print("Results/rainfall_boxplot.png")
print("Results/district_temperature.png")
print("Results/district_rainfall.png")
print("Results/climate_heatmap.png")

print("\n" + "=" * 60)
print("CLIMATE ANALYTICS COMPLETED SUCCESSFULLY")
print("=" * 60)