# ============================================================
# AI Coffee Estate Analytics
# 03_eda.py
# Exploratory Data Analysis (EDA)
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import os

# ------------------------------------------------------------
# Create folder to store plots
# ------------------------------------------------------------

os.makedirs("EDA_Plots", exist_ok=True)

# ------------------------------------------------------------
# Load Dataset
# ------------------------------------------------------------

df = pd.read_csv(r"C:\Users\Admin\Downloads\Karnataka_Coffee_Master_V3_15000.csv")

# ------------------------------------------------------------
# Dataset Shape
# ------------------------------------------------------------

print("=" * 60)
print("DATASET SHAPE")
print("=" * 60)

print("Rows    :", df.shape[0])
print("Columns :", df.shape[1])

# ------------------------------------------------------------
# Duplicate Records
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("DUPLICATE RECORDS")
print("=" * 60)

duplicates = df.duplicated().sum()

print("Duplicate Rows :", duplicates)

# ------------------------------------------------------------
# Missing Values
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

print(df.isnull().sum())

print("\nTotal Missing Values :", df.isnull().sum().sum())

# ------------------------------------------------------------
# Unique Values
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("UNIQUE VALUES")
print("=" * 60)

print(df.nunique())

# ------------------------------------------------------------
# Numerical and Categorical Features
# ------------------------------------------------------------

numerical_columns = df.select_dtypes(include=["int64", "float64"]).columns

categorical_columns = df.select_dtypes(include=["object", "string"]).columns

print("\n" + "=" * 60)
print("NUMERICAL FEATURES")
print("=" * 60)

for column in numerical_columns:
    print(column)

print("\n" + "=" * 60)
print("CATEGORICAL FEATURES")
print("=" * 60)

for column in categorical_columns:
    print(column)

# ------------------------------------------------------------
# Value Counts of Categorical Columns
# ------------------------------------------------------------

for column in categorical_columns:

    # Estate_ID is only an identifier
    if column == "Estate_ID":
        continue

    print("\n" + "=" * 60)
    print(f"VALUE COUNTS : {column}")
    print("=" * 60)

    print(df[column].value_counts())

# ------------------------------------------------------------
# Statistical Summary
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("STATISTICAL SUMMARY")
print("=" * 60)

print(df.describe())

# ------------------------------------------------------------
# Histograms
# ------------------------------------------------------------

print("\nGenerating Histograms...")

for column in numerical_columns:

    plt.figure(figsize=(7,4))

    plt.hist(df[column], bins=20)

    plt.title(column)

    plt.xlabel(column)

    plt.ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(f"EDA_Plots/{column}_Histogram.png")

    plt.close()

print("Histograms Saved.")

# ------------------------------------------------------------
# Boxplots
# ------------------------------------------------------------

print("\nGenerating Boxplots...")

for column in numerical_columns:

    plt.figure(figsize=(8,2))

    plt.boxplot(df[column], orientation="horizontal")

    plt.title(column)

    plt.tight_layout()

    plt.savefig(f"EDA_Plots/{column}_Boxplot.png")

    plt.close()

print("Boxplots Saved.")

# ------------------------------------------------------------
# Count Plots
# ------------------------------------------------------------

print("\nGenerating Count Plots...")

for column in categorical_columns:

    if column == "Estate_ID":
        continue

    plt.figure(figsize=(7,4))

    df[column].value_counts().plot(kind="bar")

    plt.title(column)

    plt.xlabel(column)

    plt.ylabel("Count")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(f"EDA_Plots/{column}_CountPlot.png")

    plt.close()

print("Count Plots Saved.")

# ------------------------------------------------------------
# Correlation Matrix
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("CORRELATION MATRIX")
print("=" * 60)

correlation = df[numerical_columns].corr()

print(correlation)

# ------------------------------------------------------------
# Correlation Heatmap
# ------------------------------------------------------------

plt.figure(figsize=(18,15))

plt.imshow(correlation, cmap="coolwarm")

plt.colorbar()

plt.xticks(
    range(len(correlation.columns)),
    correlation.columns,
    rotation=90,
    fontsize=8
)

plt.yticks(
    range(len(correlation.columns)),
    correlation.columns,
    fontsize=8
)

plt.title("Correlation Heatmap")

plt.tight_layout()

plt.savefig("EDA_Plots/Correlation_Heatmap.png")

plt.close()

print("Correlation Heatmap Saved.")

# ------------------------------------------------------------
# Top Correlations with Yield
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("TOP CORRELATIONS WITH Yield_kg_ha")
print("=" * 60)

yield_corr = correlation["Yield_kg_ha"].sort_values(ascending=False)

print(yield_corr)

# ------------------------------------------------------------
# Scatter Plot
# ------------------------------------------------------------

plt.figure(figsize=(7,5))

plt.scatter(
    df["Farm_Size_Acres"],
    df["Yield_kg_ha"],
    alpha=0.5
)

plt.xlabel("Farm Size (Acres)")

plt.ylabel("Yield (kg/ha)")

plt.title("Farm Size vs Yield")

plt.tight_layout()

plt.savefig("EDA_Plots/FarmSize_vs_Yield.png")

plt.close()

print("Scatter Plot Saved.")

# ------------------------------------------------------------
# Dataset Insights
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("EDA SUMMARY")
print("=" * 60)

print(f"Total Records              : {df.shape[0]}")
print(f"Total Features             : {df.shape[1]}")
print(f"Numerical Features         : {len(numerical_columns)}")
print(f"Categorical Features       : {len(categorical_columns)}")
print(f"Duplicate Records          : {duplicates}")
print(f"Missing Values             : {df.isnull().sum().sum()}")

print("\nDistrict Distribution")
print(df["District"].value_counts())

print("\nCoffee Type Distribution")
print(df["Coffee_Type"].value_counts())

print("\nYield Category Distribution")
print(df["Yield_Category"].value_counts())

print("\nEDA Completed Successfully.")
print("All graphs are saved in the 'EDA_Plots' folder.")

print("\n" + "=" * 60)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 60)