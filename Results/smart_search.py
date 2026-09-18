# ============================================================
# COFFEE ESTATE ANALYTICS
# FILE : smart_search.py
# ============================================================

import pandas as pd
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
print("SMART SEARCH ENGINE")
print("="*60)


# ============================================================
# SMART SEARCH FUNCTION
# ============================================================

def smart_search(
        district=None,
        coffee_type=None,
        processing_method=None,
        export_quality=None,
        yield_category=None
):

    result = df.copy()

    if district:
        result = result[
            result["District"] == district
        ]

    if coffee_type:
        result = result[
            result["Coffee_Type"] == coffee_type
        ]

    if processing_method:
        result = result[
            result["Processing_Method"] == processing_method
        ]

    if export_quality:
        result = result[
            result["Export_Quality"] == export_quality
        ]

    if yield_category:
        result = result[
            result["Yield_Category"] == yield_category
        ]

    return result


print("Smart Search Function Ready.")
print("\n")
print("="*60)
print("RUNNING SAMPLE SEARCHES")
print("="*60)

# Search 1

kodagu = smart_search(
    district="Kodagu"
)

print("Kodagu Estates :", len(kodagu))

kodagu.to_csv(
    "Results/search_kodagu.csv",
    index=False
)

# Search 2

arabica = smart_search(
    coffee_type="Arabica"
)

print("Arabica Estates :", len(arabica))

arabica.to_csv(
    "Results/search_arabica.csv",
    index=False
)

# Search 3

washed = smart_search(
    processing_method="Washed"
)

print("Washed Estates :", len(washed))

washed.to_csv(
    "Results/search_washed.csv",
    index=False
)

# Search 4

export = smart_search(
    export_quality="Yes"
)

print("Export Estates :", len(export))

export.to_csv(
    "Results/search_export.csv",
    index=False
)

# Search 5

high_yield = smart_search(
    yield_category="High"
)

print("High Yield Estates :", len(high_yield))

high_yield.to_csv(
    "Results/search_high_yield.csv",
    index=False)

print("\nSample Search CSVs Saved.")
# ============================================================
# ADVANCED SMART SEARCH
# ============================================================

print("\n")
print("=" * 60)
print("ADVANCED SMART SEARCH")
print("=" * 60)

# Example:
# Kodagu + Arabica + Export Quality

advanced_search = smart_search(

    district="Kodagu",
    coffee_type="Arabica",
    export_quality="Yes"

)

print("Matching Estates :", len(advanced_search))

advanced_search.to_csv(
    "Results/advanced_search.csv",
    index=False
)

print("Advanced Search Saved.")

print("\n")

# ------------------------------------------------------------
# Search Summary
# ------------------------------------------------------------

summary = pd.DataFrame({

    "Search": [

        "Kodagu",
        "Arabica",
        "Washed",
        "Export",
        "High Yield",
        "Advanced Search"

    ],

    "Records": [

        len(kodagu),
        len(arabica),
        len(washed),
        len(export),
        len(high_yield),
        len(advanced_search)

    ]

})

print("=" * 60)
print("SEARCH SUMMARY")
print("=" * 60)

print(summary)

summary.to_csv(
    "Results/search_summary.csv",
    index=False
)

print("Search Summary Saved.")

print("\n")

# ------------------------------------------------------------
# Top Matching Estates
# ------------------------------------------------------------

if len(advanced_search) > 0:

    top_estates = advanced_search.sort_values(

        "Yield_kg_ha",

        ascending=False

    ).head(10)

    print("=" * 60)
    print("TOP MATCHING ESTATES")
    print("=" * 60)

    print(

        top_estates[

            [

                "District",
                "Coffee_Type",
                "Yield_kg_ha",
                "Bean_Quality_Score",
                "Market_Price_INR_kg",
                "Sustainability_Score"

            ]

        ]

    )

    top_estates.to_csv(

        "Results/top_matching_estates.csv",

        index=False

    )

    print("Top Matching Estates Saved.")

else:

    print("No Estates Found.")

# ============================================================
# SMART SEARCH KPI DASHBOARD
# ============================================================

import matplotlib.pyplot as plt

print("\n")
print("="*60)
print("SMART SEARCH KPI")
print("="*60)

print("Total Estates :", len(df))
print("Kodagu Estates :", len(kodagu))
print("Arabica Estates :", len(arabica))
print("Washed Estates :", len(washed))
print("Export Estates :", len(export))
print("High Yield Estates :", len(high_yield))
print("Advanced Search Results :", len(advanced_search))


# ============================================================
# SEARCH BAR CHART
# ============================================================

summary.plot(
    x="Search",
    y="Records",
    kind="bar",
    figsize=(9,5),
    legend=False
)

plt.title("Smart Search Results")
plt.ylabel("Number of Estates")

plt.tight_layout()

plt.savefig(
    "Results/search_bar.png",
    dpi=300
)

plt.close()

print("Search Bar Chart Saved.")


# ============================================================
# SEARCH PIE CHART
# ============================================================

summary.set_index("Search")["Records"].plot(

    kind="pie",
    autopct="%1.1f%%",
    figsize=(7,7)

)

plt.ylabel("")
plt.title("Search Distribution")

plt.tight_layout()

plt.savefig(
    "Results/search_pie.png",
    dpi=300
)

plt.close()

print("Search Pie Chart Saved.")


# ============================================================
# BEST SEARCH CATEGORY
# ============================================================

best = summary.sort_values(
    "Records",
    ascending=False
).iloc[0]

print("\n")
print("="*60)
print("MOST POPULATED SEARCH")
print("="*60)

print(best)


# ============================================================
# FILES GENERATED
# ============================================================

print("\n")
print("="*60)
print("FILES GENERATED")
print("="*60)

print("CSV FILES")
print("--------------------------------")
print("Results/search_kodagu.csv")
print("Results/search_arabica.csv")
print("Results/search_washed.csv")
print("Results/search_export.csv")
print("Results/search_high_yield.csv")
print("Results/advanced_search.csv")
print("Results/search_summary.csv")
print("Results/top_matching_estates.csv")

print()

print("CHARTS")
print("--------------------------------")
print("search_bar.png")
print("search_pie.png")
# ============================================================
# FINAL REPORT
# ============================================================

print("\n")
print("=" * 60)
print("SMART SEARCH REPORT")
print("=" * 60)

print(f"Dataset Size            : {len(df)} Estates")
print(f"Search Categories       : {len(summary)}")
print(f"Advanced Search Results : {len(advanced_search)}")
print(f"Largest Search Result   : {best['Search']}")
print(f"Matching Estates        : {best['Records']}")

print("\n")
print("=" * 60)
print("SEARCH STATISTICS")
print("=" * 60)

print(summary)

print("\n")

print("=" * 60)
print("GENERATED FILES")
print("=" * 60)

generated_files = [

    "Results/search_kodagu.csv",
    "Results/search_arabica.csv",
    "Results/search_washed.csv",
    "Results/search_export.csv",
    "Results/search_high_yield.csv",
    "Results/advanced_search.csv",
    "Results/search_summary.csv",
    "Results/top_matching_estates.csv",
    "Results/search_bar.png",
    "Results/search_pie.png"

]

for file in generated_files:
    print(file)

print("\n")
print("=" * 60)
print("SMART SEARCH ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 60)

