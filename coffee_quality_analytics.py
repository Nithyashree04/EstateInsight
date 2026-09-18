# ============================================================
# COFFEE ESTATE ANALYTICS
# FILE : coffee_quality_analytics.py
# ============================================================

import os
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
# QUALITY DATA SUMMARY
# ============================================================

print("\n")
print("=" * 60)
print("COFFEE QUALITY DATA SUMMARY")
print("=" * 60)

print("Average Bean Quality :", round(df["Bean_Quality_Score"].mean(),2))
print("Maximum Quality      :", round(df["Bean_Quality_Score"].max(),2))
print("Minimum Quality      :", round(df["Bean_Quality_Score"].min(),2))
# ============================================================
# COFFEE TYPE ANALYSIS
# ============================================================

coffee_type = df["Coffee_Type"].value_counts()

print("\n")
print("=" * 60)
print("COFFEE TYPE DISTRIBUTION")
print("=" * 60)

print(coffee_type)

coffee_type.to_csv(
    "Results/coffee_type_distribution.csv"
)
# ============================================================
# EXPORT QUALITY
# ============================================================

export_quality = df["Export_Quality"].value_counts()

print("\n")
print("=" * 60)
print("EXPORT QUALITY")
print("=" * 60)

print(export_quality)

export_quality.to_csv(
    "Results/export_quality_distribution.csv"
)
# ============================================================
# PROCESSING METHOD
# ============================================================

processing = df["Processing_Method"].value_counts()

print("\n")
print("=" * 60)
print("PROCESSING METHOD")
print("=" * 60)

print(processing)

processing.to_csv(
    "Results/processing_method_distribution.csv"
)
# ============================================================
# QUALITY BY COFFEE TYPE
# ============================================================

quality_type = (
    df.groupby("Coffee_Type")["Bean_Quality_Score"]
      .mean()
      .round(2)
)

print("\n")
print("=" * 60)
print("AVERAGE QUALITY BY COFFEE TYPE")
print("=" * 60)

print(quality_type)

quality_type.to_csv(
    "Results/quality_by_type.csv"
)
# ============================================================
# QUALITY BY DISTRICT
# ============================================================

quality_district = (
    df.groupby("District")["Bean_Quality_Score"]
      .mean()
      .round(2)
)

print("\n")
print("=" * 60)
print("AVERAGE QUALITY BY DISTRICT")
print("=" * 60)

print(quality_district)

quality_district.to_csv(
    "Results/quality_by_district.csv"
)
# ============================================================
# BEAN QUALITY HISTOGRAM
# ============================================================

plt.figure(figsize=(10,6))

plt.hist(
    df["Bean_Quality_Score"],
    bins=20,
    edgecolor="black"
)

plt.title("Bean Quality Score Distribution")
plt.xlabel("Bean Quality Score")
plt.ylabel("Number of Estates")

plt.tight_layout()

plt.savefig(
    "Results/bean_quality_histogram.png",
    dpi=300
)

plt.close()

print("Bean Quality Histogram Saved.")
# ============================================================
# COFFEE TYPE PIE CHART
# ============================================================

plt.figure(figsize=(7,7))

plt.pie(
    coffee_type,
    labels=coffee_type.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Coffee Type Distribution")

plt.savefig(
    "Results/coffee_type_pie.png",
    dpi=300
)

plt.close()

print("Coffee Type Pie Chart Saved.")
# ============================================================
# EXPORT QUALITY DONUT CHART
# ============================================================

plt.figure(figsize=(7,7))

plt.pie(
    export_quality,
    labels=export_quality.index,
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops=dict(width=0.45)
)

plt.title("Export Quality Distribution")

plt.savefig(
    "Results/export_quality_donut.png",
    dpi=300
)

plt.close()

print("Export Quality Donut Chart Saved.")
# ============================================================
# PROCESSING METHOD BAR CHART
# ============================================================

plt.figure(figsize=(8,5))

processing.plot(kind="bar")

plt.title("Processing Method Distribution")
plt.xlabel("Processing Method")
plt.ylabel("Number of Estates")

plt.tight_layout()

plt.savefig(
    "Results/processing_method_bar.png",
    dpi=300
)

plt.close()

print("Processing Method Bar Chart Saved.")
# ============================================================
# BEAN QUALITY BOXPLOT
# ============================================================

plt.figure(figsize=(6,6))

plt.boxplot(df["Bean_Quality_Score"])

plt.title("Bean Quality Score Distribution")
plt.ylabel("Bean Quality Score")

plt.tight_layout()

plt.savefig(
    "Results/bean_quality_boxplot.png",
    dpi=300
)

plt.close()

print("Bean Quality Box Plot Saved.")
# ============================================================
# TOP 10 QUALITY ESTATES
# ============================================================

top_quality = df.sort_values(
    by="Bean_Quality_Score",
    ascending=False
).head(10)

print("\n" + "=" * 60)
print("TOP 10 HIGHEST QUALITY ESTATES")
print("=" * 60)

print(
    top_quality[
        [
            "District",
            "Coffee_Type",
            "Bean_Quality_Score",
            "Export_Quality",
            "Processing_Method"
        ]
    ]
)

top_quality.to_csv(
    "Results/top10_quality_estates.csv",
    index=False
)
# ============================================================
# QUALITY KPI
# ============================================================

print("\n" + "=" * 60)
print("QUALITY KPI")
print("=" * 60)

print(f"Total Estates          : {len(df)}")
print(f"Average Quality Score  : {df['Bean_Quality_Score'].mean():.2f}")
print(f"Highest Quality Score  : {df['Bean_Quality_Score'].max():.2f}")
print(f"Lowest Quality Score   : {df['Bean_Quality_Score'].min():.2f}")

print(f"\nArabica Estates : {(df['Coffee_Type']=='Arabica').sum()}")
print(f"Robusta Estates : {(df['Coffee_Type']=='Robusta').sum()}")

print(f"\nExport Quality Estates : {(df['Export_Quality']=='Yes').sum()}")
print(f"Non Export Estates     : {(df['Export_Quality']=='No').sum()}")
# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("FILES GENERATED")
print("=" * 60)

print("Results/coffee_type_distribution.csv")
print("Results/export_quality_distribution.csv")
print("Results/processing_method_distribution.csv")
print("Results/quality_by_type.csv")
print("Results/quality_by_district.csv")
print("Results/top10_quality_estates.csv")

print("\nCharts Generated")

print("bean_quality_histogram.png")
print("coffee_type_pie.png")
print("export_quality_donut.png")
print("processing_method_bar.png")
print("bean_quality_boxplot.png")

print("\n" + "=" * 60)
print("COFFEE QUALITY ANALYTICS COMPLETED SUCCESSFULLY")
print("=" * 60)