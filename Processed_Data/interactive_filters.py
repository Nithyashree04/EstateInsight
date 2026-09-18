# ============================================================
# COFFEE ESTATE ANALYTICS
# FILE : interactive_filters.py
# ============================================================

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Interactive Coffee Dashboard",
    layout="wide"
)

st.title("☕ Coffee Estate Analytics Dashboard")

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    return pd.read_excel(
        r"C:\Users\Admin\OneDrive\Desktop\Sujay Project\Karnataka_Coffee_Cleaned.xlsx"
    )

df = load_data()

st.success(f"Dataset Loaded Successfully ({len(df)} Estates)")

# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("Dashboard Filters")

district = st.sidebar.multiselect(
    "District",
    options=sorted(df["District"].unique()),
    default=sorted(df["District"].unique())
)

coffee = st.sidebar.multiselect(
    "Coffee Type",
    options=sorted(df["Coffee_Type"].unique()),
    default=sorted(df["Coffee_Type"].unique())
)

processing = st.sidebar.multiselect(
    "Processing Method",
    options=sorted(df["Processing_Method"].unique()),
    default=sorted(df["Processing_Method"].unique())
)

export = st.sidebar.multiselect(
    "Export Quality",
    options=sorted(df["Export_Quality"].unique()),
    default=sorted(df["Export_Quality"].unique())
)

yield_range = st.sidebar.slider(
    "Yield (kg/ha)",
    int(df["Yield_kg_ha"].min()),
    int(df["Yield_kg_ha"].max()),
    (
        int(df["Yield_kg_ha"].min()),
        int(df["Yield_kg_ha"].max())
    )
)

quality_range = st.sidebar.slider(
    "Bean Quality Score",
    int(df["Bean_Quality_Score"].min()),
    int(df["Bean_Quality_Score"].max()),
    (
        int(df["Bean_Quality_Score"].min()),
        int(df["Bean_Quality_Score"].max())
    )
)

st.sidebar.success("Filters Ready")
# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df[

    (df["District"].isin(district)) &
    (df["Coffee_Type"].isin(coffee)) &
    (df["Processing_Method"].isin(processing)) &
    (df["Export_Quality"].isin(export)) &
    (df["Yield_kg_ha"] >= yield_range[0]) &
    (df["Yield_kg_ha"] <= yield_range[1]) &
    (df["Bean_Quality_Score"] >= quality_range[0]) &
    (df["Bean_Quality_Score"] <= quality_range[1])

]

st.sidebar.success(
    f"{len(filtered_df)} Estates Found"
)

# ============================================================
# FILTERED DATA
# ============================================================

st.subheader("Filtered Coffee Estates")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=450
)

# ============================================================
# LIVE KPI DASHBOARD
# ============================================================

st.subheader("Dashboard KPI")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Estates",
    len(filtered_df)
)

col2.metric(
    "Average Yield",
    f"{filtered_df['Yield_kg_ha'].mean():.2f} kg/ha"
)

col3.metric(
    "Average Quality",
    f"{filtered_df['Bean_Quality_Score'].mean():.2f}"
)

col4.metric(
    "Average Sustainability",
    f"{filtered_df['Sustainability_Score'].mean():.2f}"
)

col5, col6, col7, col8 = st.columns(4)

col5.metric(
    "Average Health",
    f"{filtered_df['Estate_Health_Score'].mean():.2f}"
)

col6.metric(
    "Carbon Footprint",
    f"{filtered_df['Carbon_Footprint_tCO2e'].mean():.2f}"
)

col7.metric(
    "Market Price",
    f"₹ {filtered_df['Market_Price_INR_kg'].mean():.2f}"
)

col8.metric(
    "Average Rainfall",
    f"{filtered_df['Rainfall_mm'].mean():.2f} mm"
)

st.success("KPIs Updated Successfully")
# ============================================================
# INTERACTIVE VISUALIZATIONS
# ============================================================

import plotly.express as px

st.subheader("Interactive Analytics Dashboard")

# ============================================================
# ROW 1
# ============================================================

col1, col2 = st.columns(2)

with col1:

    district_yield = (
        filtered_df
        .groupby("District")["Yield_kg_ha"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        district_yield,
        x="District",
        y="Yield_kg_ha",
        color="District",
        title="Average Yield by District"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    sustainability = (
        filtered_df
        .groupby("District")["Sustainability_Score"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        sustainability,
        x="District",
        y="Sustainability_Score",
        color="District",
        title="Sustainability Score"
    )

    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# ROW 2
# ============================================================

col3, col4 = st.columns(2)

with col3:

    coffee = (
        filtered_df["Coffee_Type"]
        .value_counts()
        .reset_index()
    )

    coffee.columns = ["Coffee_Type", "Count"]

    fig = px.pie(
        coffee,
        names="Coffee_Type",
        values="Count",
        title="Coffee Type Distribution",
        hole=0.45
    )

    st.plotly_chart(fig, use_container_width=True)

with col4:

    quality = (
        filtered_df
        .groupby("Coffee_Type")["Bean_Quality_Score"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        quality,
        x="Coffee_Type",
        y="Bean_Quality_Score",
        color="Coffee_Type",
        title="Bean Quality Comparison"
    )

    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# ROW 3
# ============================================================

col5, col6 = st.columns(2)

with col5:

    rainfall = (
        filtered_df
        .groupby("District")["Rainfall_mm"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        rainfall,
        x="District",
        y="Rainfall_mm",
        color="District",
        title="Average Rainfall"
    )

    st.plotly_chart(fig, use_container_width=True)

with col6:

    carbon = (
        filtered_df
        .groupby("District")["Carbon_Footprint_tCO2e"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        carbon,
        x="District",
        y="Carbon_Footprint_tCO2e",
        color="District",
        title="Carbon Footprint"
    )

    st.plotly_chart(fig, use_container_width=True)

st.success("Interactive Charts Updated Successfully")
# ============================================================
# ADVANCED VISUALIZATIONS
# ============================================================

st.subheader("Advanced Analytics")

# ============================================================
# ROW 1
# ============================================================

col1, col2 = st.columns(2)

with col1:

    fig = px.scatter(

        filtered_df,

        x="Yield_kg_ha",
        y="Bean_Quality_Score",

        color="Coffee_Type",

        size="Sustainability_Score",

        hover_data=[
            "District",
            "Processing_Method",
            "Market_Price_INR_kg"
        ],

        title="Yield vs Bean Quality"

    )

    st.plotly_chart(fig, use_container_width=True)


with col2:

    fig = px.scatter(

        filtered_df,

        x="Carbon_Footprint_tCO2e",
        y="Sustainability_Score",

        color="District",

        size="Yield_kg_ha",

        hover_data=[
            "Coffee_Type",
            "Bean_Quality_Score"
        ],

        title="Carbon vs Sustainability"

    )

    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# ROW 2
# ============================================================

col3, col4 = st.columns(2)

with col3:

    fig = px.box(

        filtered_df,

        x="Coffee_Type",
        y="Yield_kg_ha",

        color="Coffee_Type",

        title="Yield Distribution"

    )

    st.plotly_chart(fig, use_container_width=True)


with col4:

    fig = px.box(

        filtered_df,

        x="District",
        y="Bean_Quality_Score",

        color="District",

        title="Quality Distribution"

    )

    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# ESTATE LOCATION MAP
# ============================================================

st.subheader("Estate Location Map")

fig = px.scatter_map(

    filtered_df,

    lat="Latitude",

    lon="Longitude",

    color="District",

    size="Yield_kg_ha",

    hover_name="Coffee_Type",

    hover_data=[

        "Bean_Quality_Score",

        "Sustainability_Score",

        "Market_Price_INR_kg"

    ],

    zoom=6,

    height=650

)

st.plotly_chart(fig, use_container_width=True)


# ============================================================
# TOP 10 ESTATES
# ============================================================

st.subheader("Top 10 Performing Estates")

top10 = (

    filtered_df

    .sort_values(

        "Yield_kg_ha",

        ascending=False

    )

    .head(10)

)

st.dataframe(

    top10[

        [

            "District",

            "Coffee_Type",

            "Yield_kg_ha",

            "Bean_Quality_Score",

            "Sustainability_Score",

            "Market_Price_INR_kg"

        ]

    ],

    use_container_width=True

)

st.success("Advanced Visualizations Loaded Successfully")
# ============================================================
# DOWNLOADS, SUMMARY & SEARCH
# ============================================================

st.subheader("Download & Search")

# ============================================================
# DOWNLOAD FILTERED DATA
# ============================================================

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(

    label="📥 Download Filtered Data (CSV)",

    data=csv,

    file_name="filtered_coffee_estates.csv",

    mime="text/csv"

)

# ============================================================
# SUMMARY STATISTICS
# ============================================================

st.subheader("Summary Statistics")

st.dataframe(

    filtered_df.describe().round(2),

    use_container_width=True

)

# ============================================================
# ESTATE SEARCH
# ============================================================

st.subheader("Search Estate")

search_option = st.radio(

    "Search By",

    ["Estate_ID", "Owner_Name"],

    horizontal=True

)

if search_option == "Estate_ID":

    estate_id = st.text_input("Enter Estate ID")

    if estate_id:

        result = filtered_df[
            filtered_df["Estate_ID"].astype(str) == estate_id
        ]

        if len(result) > 0:
            st.success("Estate Found")
            st.dataframe(result, use_container_width=True)
        else:
            st.error("Estate Not Found")

else:

    owner = st.text_input("Enter Owner Name")

    if owner:

        result = filtered_df[
            filtered_df["Owner_Name"]
        ].astype(str).str.contains(
            owner,
            case=False,
            na=False
        )

        result = filtered_df[result]

        if len(result) > 0:
            st.success(f"{len(result)} Estate(s) Found")
            st.dataframe(result, use_container_width=True)
        else:
            st.error("No Matching Owner Found")

# ============================================================
# QUICK INSIGHTS
# ============================================================

st.subheader("Quick Insights")

col1, col2 = st.columns(2)

with col1:

    st.info(
        f"""
**Highest Yield District**

{
filtered_df.groupby("District")["Yield_kg_ha"]
.mean()
.idxmax()
}
"""
    )

    st.info(
        f"""
**Highest Bean Quality**

{
filtered_df.groupby("Coffee_Type")["Bean_Quality_Score"]
.mean()
.idxmax()
}
"""
    )

with col2:

    st.info(
        f"""
**Most Sustainable District**

{
filtered_df.groupby("District")["Sustainability_Score"]
.mean()
.idxmax()
}
"""
    )

    st.info(
        f"""
**Lowest Carbon Footprint**

{
filtered_df.groupby("District")["Carbon_Footprint_tCO2e"]
.mean()
.idxmin()
}
"""
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
"""
### ☕ AI-Powered Coffee Estate Analytics

Developed using:

- Streamlit
- Python
- Plotly
- Pandas
- Machine Learning

Interactive Dashboard for Karnataka Coffee Estates.
"""
)

st.success("Dashboard Loaded Successfully")
