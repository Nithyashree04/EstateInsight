# ============================================================
# COFFEE ESTATE ANALYTICS
# FILE : ai_recommendation_engine.py
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import os

print("=" * 60)
print("LOADING DATASET")
print("=" * 60)

df = pd.read_excel(
    r"C:\Users\Admin\OneDrive\Desktop\Sujay Project\Finaldataset1.xlsx"
)

os.makedirs("Results", exist_ok=True)

print("Dataset Shape :", df.shape)

print("\n")
print("=" * 60)
print("GENERATING AI RECOMMENDATIONS")
print("=" * 60)

# ------------------------------------------------------------
# AI Recommendation Function
# ------------------------------------------------------------

def generate_recommendation(row):

    recommendations = []

    # Soil Moisture
    if row["Soil_Moisture_%"] < 30:
        recommendations.append(
            "Increase irrigation frequency"
        )

    # Pest Severity
    if row["Pest_Severity_0_10"] >= 7:
        recommendations.append(
            "Immediate pest control required"
        )

    # Disease Severity
    if row["Disease_Severity_0_10"] >= 7:
        recommendations.append(
            "Apply disease management practices"
        )

    # Bean Quality
    if row["Bean_Quality_Score"] < 75:
        recommendations.append(
            "Improve harvesting and post-harvest processing"
        )

    # Sustainability
    if row["Sustainability_Score"] < 65:
        recommendations.append(
            "Adopt sustainable farming practices"
        )

    # Carbon Footprint
    if row["Carbon_Footprint_tCO2e"] > 2.8:
        recommendations.append(
            "Reduce carbon emissions"
        )

    # Yield
    if row["Yield_kg_ha"] < 1100:
        recommendations.append(
            "Improve crop management for higher yield"
        )

    # Zinc
    if row["Zn_ppm"] < 1.2:
        recommendations.append(
            "Apply Zinc micronutrient fertilizer"
        )

    # Iron
    if row["Fe_ppm"] < 10:
        recommendations.append(
            "Increase Iron supplementation"
        )

    # Magnesium
    if row["Mg_ppm"] < 35:
        recommendations.append(
            "Apply Magnesium fertilizer"
        )

    # Sulphur
    if row["S_ppm"] < 15:
        recommendations.append(
            "Apply Sulphur fertilizer"
        )

    # Export Quality
    if row["Export_Quality"] == "No":
        recommendations.append(
            "Improve bean quality for export standards"
        )

    # If no recommendation
    if len(recommendations) == 0:
        recommendations.append(
            "Estate performing well. Continue current practices."
        )

    return " | ".join(recommendations)


# ------------------------------------------------------------
# Generate Recommendations
# ------------------------------------------------------------

df["AI_Recommendation"] = df.apply(
    generate_recommendation,
    axis=1
)

print("AI Recommendations Generated Successfully.")

print("\n")
print("=" * 60)
print("SAMPLE RECOMMENDATIONS")
print("=" * 60)

print(
    df[
        [
            "District",
            "Coffee_Type",
            "Yield_kg_ha",
            "AI_Recommendation"
        ]
    ].head(10)
)

# Save CSV

df.to_csv(
    "Results/ai_recommendations.csv",
    index=False
)

print("\nAI Recommendation CSV Saved.")
# ============================================================
# RECOMMENDATION ANALYTICS
# ============================================================

print("\n")
print("=" * 60)
print("AI RECOMMENDATION ANALYTICS")
print("=" * 60)

# ------------------------------------------------------------
# Count Individual Recommendations
# ------------------------------------------------------------

recommendation_count = {}

for rec in df["AI_Recommendation"]:

    items = rec.split(" | ")

    for item in items:

        recommendation_count[item] = recommendation_count.get(item, 0) + 1

recommendation_summary = pd.DataFrame(

    recommendation_count.items(),
    columns=["Recommendation", "Count"]

)

recommendation_summary = recommendation_summary.sort_values(
    by="Count",
    ascending=False
)

print(recommendation_summary)

recommendation_summary.to_csv(
    "Results/recommendation_summary.csv",
    index=False
)

print("\nRecommendation Summary Saved.")

# ------------------------------------------------------------
# District-wise Recommendation Count
# ------------------------------------------------------------

district_summary = (

    df.groupby("District")["AI_Recommendation"]
    .count()
    .reset_index()

)

district_summary.columns = [

    "District",
    "Total_Recommendations"

]

print("\n")
print("=" * 60)
print("DISTRICT RECOMMENDATION SUMMARY")
print("=" * 60)

print(district_summary)

district_summary.to_csv(
    "Results/district_recommendations.csv",
    index=False
)

print("District Recommendation CSV Saved.")

# ------------------------------------------------------------
# Coffee Type Recommendation Count
# ------------------------------------------------------------

coffee_summary = (

    df.groupby("Coffee_Type")["AI_Recommendation"]
    .count()
    .reset_index()

)

coffee_summary.columns = [

    "Coffee_Type",
    "Total_Recommendations"

]

print("\n")
print("=" * 60)
print("COFFEE TYPE RECOMMENDATIONS")
print("=" * 60)

print(coffee_summary)

coffee_summary.to_csv(
    "Results/coffee_type_recommendations.csv",
    index=False
)

print("Coffee Type Recommendation CSV Saved.")

# ------------------------------------------------------------
# Processing Method Recommendation Count
# ------------------------------------------------------------

processing_summary = (

    df.groupby("Processing_Method")["AI_Recommendation"]
    .count()
    .reset_index()

)

processing_summary.columns = [

    "Processing_Method",
    "Total_Recommendations"

]

print("\n")
print("=" * 60)
print("PROCESSING METHOD RECOMMENDATIONS")
print("=" * 60)

print(processing_summary)

processing_summary.to_csv(
    "Results/processing_method_recommendations.csv",
    index=False
)

print("Processing Method Recommendation CSV Saved.")

# ------------------------------------------------------------
# Export Quality Recommendation Count
# ------------------------------------------------------------

export_summary = (

    df.groupby("Export_Quality")["AI_Recommendation"]
    .count()
    .reset_index()

)

export_summary.columns = [

    "Export_Quality",
    "Total_Recommendations"

]

print("\n")
print("=" * 60)
print("EXPORT QUALITY RECOMMENDATIONS")
print("=" * 60)

print(export_summary)

export_summary.to_csv(
    "Results/export_quality_recommendations.csv",
    index=False
)

print("Export Recommendation CSV Saved.")

# ------------------------------------------------------------
# Top 10 Estates With Most Recommendations
# ------------------------------------------------------------

df["Recommendation_Count"] = df["AI_Recommendation"].apply(

    lambda x: len(x.split(" | "))

)

top10 = df.sort_values(

    by="Recommendation_Count",
    ascending=False

).head(10)

print("\n")
print("=" * 60)
print("TOP 10 ESTATES NEEDING ATTENTION")
print("=" * 60)

print(

    top10[
        [

            "District",
            "Coffee_Type",
            "Recommendation_Count",
            "AI_Recommendation"

        ]
    ]

)

top10.to_csv(

    "Results/top10_estates_requiring_attention.csv",
    index=False

)

print("Top 10 Estates CSV Saved.")
# ============================================================
# AI RECOMMENDATION VISUALIZATIONS
# ============================================================

print("\n")
print("=" * 60)
print("GENERATING AI VISUALIZATIONS")
print("=" * 60)

# ------------------------------------------------------------
# Recommendation Bar Chart
# ------------------------------------------------------------

recommendation_summary.plot(
    x="Recommendation",
    y="Count",
    kind="bar",
    figsize=(12,6),
    legend=False
)

plt.title("AI Recommendation Distribution")
plt.xlabel("Recommendation")
plt.ylabel("Number of Estates")
plt.xticks(rotation=45, ha="right")

plt.tight_layout()

plt.savefig(
    "Results/recommendation_bar.png",
    dpi=300
)

plt.close()

print("Recommendation Bar Chart Saved.")

# ------------------------------------------------------------
# Recommendation Pie Chart
# ------------------------------------------------------------

recommendation_summary.set_index("Recommendation")["Count"].plot(

    kind="pie",
    autopct="%1.1f%%",
    figsize=(8,8)

)

plt.ylabel("")
plt.title("Recommendation Distribution")

plt.tight_layout()

plt.savefig(
    "Results/recommendation_pie.png",
    dpi=300
)

plt.close()

print("Recommendation Pie Chart Saved.")

# ------------------------------------------------------------
# District Recommendation Chart
# ------------------------------------------------------------

district_summary.plot(

    x="District",
    y="Total_Recommendations",
    kind="bar",
    figsize=(7,5),
    legend=False

)

plt.title("Recommendations by District")
plt.ylabel("Number of Estates")

plt.tight_layout()

plt.savefig(
    "Results/district_recommendations.png",
    dpi=300
)

plt.close()

print("District Recommendation Chart Saved.")

# ------------------------------------------------------------
# Coffee Type Recommendation Chart
# ------------------------------------------------------------

coffee_summary.plot(

    x="Coffee_Type",
    y="Total_Recommendations",
    kind="bar",
    figsize=(6,5),
    legend=False

)

plt.title("Recommendations by Coffee Type")
plt.ylabel("Number of Estates")

plt.tight_layout()

plt.savefig(
    "Results/coffee_type_recommendations.png",
    dpi=300
)

plt.close()

print("Coffee Type Recommendation Chart Saved.")

# ------------------------------------------------------------
# Processing Method Recommendation Chart
# ------------------------------------------------------------

processing_summary.plot(

    x="Processing_Method",
    y="Total_Recommendations",
    kind="bar",
    figsize=(7,5),
    legend=False

)

plt.title("Recommendations by Processing Method")
plt.ylabel("Number of Estates")

plt.tight_layout()

plt.savefig(
    "Results/processing_method_recommendations.png",
    dpi=300
)

plt.close()

print("Processing Method Recommendation Chart Saved.")

# ------------------------------------------------------------
# Export Quality Recommendation Chart
# ------------------------------------------------------------

export_summary.plot(

    x="Export_Quality",
    y="Total_Recommendations",
    kind="bar",
    figsize=(6,5),
    legend=False

)

plt.title("Recommendations by Export Quality")
plt.ylabel("Number of Estates")

plt.tight_layout()

plt.savefig(
    "Results/export_quality_recommendations.png",
    dpi=300
)

plt.close()

print("Export Recommendation Chart Saved.")

print("\n")
print("=" * 60)
print("ALL AI VISUALIZATIONS GENERATED SUCCESSFULLY")
print("=" * 60)
# ============================================================
# AI RECOMMENDATION KPI DASHBOARD
# ============================================================

print("\n")
print("=" * 60)
print("AI RECOMMENDATION KPI DASHBOARD")
print("=" * 60)

total_estates = len(df)

total_recommendations = df["Recommendation_Count"].sum()

average_recommendations = round(
    df["Recommendation_Count"].mean(), 2
)

maximum_recommendations = df["Recommendation_Count"].max()

minimum_recommendations = df["Recommendation_Count"].min()

print(f"Total Estates                 : {total_estates}")
print(f"Total Recommendations         : {total_recommendations}")
print(f"Average Recommendations       : {average_recommendations}")
print(f"Maximum Recommendations       : {maximum_recommendations}")
print(f"Minimum Recommendations       : {minimum_recommendations}")

print("\n")

# ------------------------------------------------------------
# Most Frequent Recommendation
# ------------------------------------------------------------

most_common = recommendation_summary.iloc[0]

print("=" * 60)
print("MOST COMMON AI RECOMMENDATION")
print("=" * 60)

print("Recommendation :",
      most_common["Recommendation"])

print("Occurrences    :",
      int(most_common["Count"]))

print("\n")

# ------------------------------------------------------------
# Recommendation Percentage
# ------------------------------------------------------------

recommendation_summary["Percentage"] = (

    recommendation_summary["Count"]
    / recommendation_summary["Count"].sum()

) * 100

recommendation_summary["Percentage"] = (
    recommendation_summary["Percentage"].round(2)
)

recommendation_summary.to_csv(

    "Results/recommendation_percentages.csv",

    index=False

)

print("=" * 60)
print("TOP 10 RECOMMENDATIONS")
print("=" * 60)

print(recommendation_summary.head(10))

print("\n")

# ------------------------------------------------------------
# District Ranking
# ------------------------------------------------------------

district_rank = (

    df.groupby("District")["Recommendation_Count"]

    .mean()

    .sort_values(ascending=False)

)

print("=" * 60)
print("DISTRICT ATTENTION RANKING")
print("=" * 60)

print(district_rank)

district_rank.to_csv(

    "Results/district_attention_ranking.csv"

)

print("\n")

# ------------------------------------------------------------
# Coffee Type Ranking
# ------------------------------------------------------------

coffee_rank = (

    df.groupby("Coffee_Type")["Recommendation_Count"]

    .mean()

    .sort_values(ascending=False)

)

print("=" * 60)
print("COFFEE TYPE ATTENTION RANKING")
print("=" * 60)

print(coffee_rank)

coffee_rank.to_csv(

    "Results/coffee_type_attention_ranking.csv"

)

print("\n")

# ------------------------------------------------------------
# Processing Method Ranking
# ------------------------------------------------------------

processing_rank = (

    df.groupby("Processing_Method")["Recommendation_Count"]

    .mean()

    .sort_values(ascending=False)

)

print("=" * 60)
print("PROCESSING METHOD ATTENTION RANKING")
print("=" * 60)

print(processing_rank)

processing_rank.to_csv(

    "Results/processing_attention_ranking.csv"

)

print("\n")

# ------------------------------------------------------------
# AI Recommendation Score
# ------------------------------------------------------------

df["AI_Score"] = (

    100

    - df["Recommendation_Count"] * 8

)

df["AI_Score"] = df["AI_Score"].clip(

    lower=0

)

print("=" * 60)
print("AI SCORE SUMMARY")
print("=" * 60)

print(df["AI_Score"].describe().round(2))

df.to_csv(

    "Results/ai_recommendation_scores.csv",

    index=False

)

print("\n")

# ------------------------------------------------------------
# Top Performing Estates
# ------------------------------------------------------------

top10 = df.sort_values(

    "AI_Score",

    ascending=False

).head(10)

print("=" * 60)
print("TOP 10 BEST ESTATES")
print("=" * 60)

print(

    top10[

        [

            "District",

            "Coffee_Type",

            "AI_Score",

            "Recommendation_Count"

        ]

    ]

)

top10.to_csv(

    "Results/top10_ai_estates.csv",

    index=False

)

print("\n")

# ------------------------------------------------------------
# Estates Needing Attention
# ------------------------------------------------------------

bottom10 = df.sort_values(

    "AI_Score"

).head(10)

print("=" * 60)
print("TOP 10 ESTATES NEEDING ATTENTION")
print("=" * 60)

print(

    bottom10[

        [

            "District",

            "Coffee_Type",

            "AI_Score",

            "Recommendation_Count"

        ]

    ]

)

bottom10.to_csv(

    "Results/bottom10_ai_estates.csv",

    index=False

)

print("\n")

# ------------------------------------------------------------
# Files Generated
# ------------------------------------------------------------

print("=" * 60)
print("FILES GENERATED")
print("=" * 60)

print("CSV FILES")
print("--------------------------------------")

print("Results/ai_recommendations.csv")
print("Results/recommendation_summary.csv")
print("Results/recommendation_percentages.csv")
print("Results/district_recommendations.csv")
print("Results/coffee_type_recommendations.csv")
print("Results/processing_method_recommendations.csv")
print("Results/export_quality_recommendations.csv")
print("Results/top10_estates_requiring_attention.csv")
print("Results/district_attention_ranking.csv")
print("Results/coffee_type_attention_ranking.csv")
print("Results/processing_attention_ranking.csv")
print("Results/ai_recommendation_scores.csv")
print("Results/top10_ai_estates.csv")
print("Results/bottom10_ai_estates.csv")

print("\n")

print("CHARTS")
print("--------------------------------------")

print("recommendation_bar.png")
print("recommendation_pie.png")
print("district_recommendations.png")
print("coffee_type_recommendations.png")
print("processing_method_recommendations.png")
print("export_quality_recommendations.png")

print("\n")

print("=" * 60)
print("AI RECOMMENDATION ENGINE COMPLETED SUCCESSFULLY")
print("=" * 60)
