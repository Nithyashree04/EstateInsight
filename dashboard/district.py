# ============================================================
# ESTATEINSIGHT
# DISTRICT ANALYTICS MODULE
# File: dashboard/district.py
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# COLUMN HELPER
# ============================================================

def find_column(df, possible_names):
    """
    Finds the first matching column from a list of possible names.
    Returns None if no column is found.
    """

    for name in possible_names:
        if name in df.columns:
            return name

    return None


# ============================================================
# NUMERIC CONVERSION HELPER
# ============================================================

def to_numeric(df, column):
    """
    Safely converts a dataframe column to numeric values.
    """

    if column is None or column not in df.columns:
        return pd.Series(dtype="float64")

    return pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ============================================================
# CHART LAYOUT
# ============================================================

def clean_chart(fig, height=420):
    """
    Applies common styling to Plotly charts.
    """

    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        )
    )

    return fig


# ============================================================
# MAIN FUNCTION
# ============================================================

def show_district(df):

    # ========================================================
    # DATA VALIDATION
    # ========================================================

    if df is None:

        st.warning(
            "No dataset was provided."
        )

        return


    if df.empty:

        st.warning(
            "No estate data is available for District Analytics."
        )

        return


    # ========================================================
    # DETECT COLUMNS
    # ========================================================

    district_col = find_column(
        df,
        [
            "District",
            "district",
            "DISTRICT",
            "Region",
            "Location"
        ]
    )


    yield_col = find_column(
        df,
        [
            "Yield_kg_ha",
            "Yield (kg/ha)",
            "Yield_kg/ha",
            "Yield",
            "Coffee_Yield",
            "Coffee Yield",
            "Production_kg",
            "Production"
        ]
    )


    revenue_col = find_column(
        df,
        [
            "Revenue",
            "Revenue_INR",
            "Revenue_₹",
            "Revenue (₹)",
            "Total_Revenue",
            "Total Revenue"
        ]
    )


    profit_col = find_column(
        df,
        [
            "Profit",
            "Profit_INR",
            "Profit_₹",
            "Profit (₹)",
            "Net_Profit",
            "Net Profit"
        ]
    )


    health_col = find_column(
        df,
        [
            "Estate_Health_Index",
            "Estate Health Index",
            "Health_Index",
            "Health Index",
            "Health_Score",
            "Health Score",
            "Estate_Health"
        ]
    )


    sustainability_col = find_column(
        df,
        [
            "Sustainability_Score",
            "Sustainability Score",
            "Sustainability",
            "Sustainability_Index",
            "Sustainability Index"
        ]
    )


    temperature_col = find_column(
        df,
        [
            "Temperature",
            "Temperature_C",
            "Temperature (°C)",
            "Avg_Temperature",
            "Average_Temperature",
            "Temp_C"
        ]
    )


    rainfall_col = find_column(
        df,
        [
            "Rainfall",
            "Rainfall_mm",
            "Rainfall (mm)",
            "Average_Rainfall",
            "Avg_Rainfall"
        ]
    )


    humidity_col = find_column(
        df,
        [
            "Humidity",
            "Humidity_%",
            "Humidity (%)",
            "Relative_Humidity"
        ]
    )


    farm_size_col = find_column(
        df,
        [
            "Farm_Size_Acres",
            "Farm Size Acres",
            "Farm_Size",
            "Farm Size",
            "Area_Acres",
            "Area"
        ]
    )


    # ========================================================
    # HEADER
    # ========================================================

    st.title(
        "📍 District Analytics"
    )

    st.caption(
        "Compare coffee estate productivity, financial performance, "
        "health, sustainability and climate conditions across districts."
    )

    st.write("")


    # ========================================================
    # DISTRICT VALIDATION
    # ========================================================

    if district_col is None:

        st.error(
            "❌ District information could not be found in the dataset."
        )

        st.info(
            "The dashboard expects a column such as "
            "'District', 'Region', or 'Location'."
        )

        return


    # ========================================================
    # CLEAN DATA
    # ========================================================

    data = df.copy()


    data[district_col] = (
        data[district_col]
        .astype(str)
        .str.strip()
    )


    data = data[
        (data[district_col] != "")
        &
        (data[district_col] != "nan")
        &
        (data[district_col] != "None")
    ].copy()


    if data.empty:

        st.warning(
            "No valid district records are available."
        )

        return


    # ========================================================
    # DISTRICT SELECTOR
    # ========================================================

    district_list = sorted(
        data[district_col]
        .dropna()
        .unique()
        .tolist()
    )


    selected_district = st.selectbox(
        "📍 Select District",
        options=[
            "All Districts"
        ] + district_list,
        index=0
    )


    if selected_district == "All Districts":

        selected_data = data.copy()

    else:

        selected_data = data[
            data[district_col] == selected_district
        ].copy()


    # ========================================================
    # BASIC METRICS
    # ========================================================

    number_of_estates = len(
        selected_data
    )


    number_of_districts = selected_data[
        district_col
    ].nunique()


    # --------------------------------------------------------
    # YIELD
    # --------------------------------------------------------

    avg_yield = None

    if yield_col:

        yield_values = to_numeric(
            selected_data,
            yield_col
        )

        avg_yield = yield_values.mean()


    # --------------------------------------------------------
    # REVENUE
    # --------------------------------------------------------

    avg_revenue = None

    if revenue_col:

        revenue_values = to_numeric(
            selected_data,
            revenue_col
        )

        avg_revenue = revenue_values.mean()


    # --------------------------------------------------------
    # PROFIT
    # --------------------------------------------------------

    avg_profit = None

    if profit_col:

        profit_values = to_numeric(
            selected_data,
            profit_col
        )

        avg_profit = profit_values.mean()


    # --------------------------------------------------------
    # HEALTH
    # --------------------------------------------------------

    avg_health = None

    if health_col:

        health_values = to_numeric(
            selected_data,
            health_col
        )

        avg_health = health_values.mean()


    # --------------------------------------------------------
    # SUSTAINABILITY
    # --------------------------------------------------------

    avg_sustainability = None

    if sustainability_col:

        sustainability_values = to_numeric(
            selected_data,
            sustainability_col
        )

        avg_sustainability = (
            sustainability_values.mean()
        )


    # --------------------------------------------------------
    # TEMPERATURE
    # --------------------------------------------------------

    avg_temperature = None

    if temperature_col:

        temperature_values = to_numeric(
            selected_data,
            temperature_col
        )

        avg_temperature = (
            temperature_values.mean()
        )


    # ========================================================
    # MAIN KPI SECTION
    # ========================================================

    st.subheader(
        "📊 District Overview"
    )


    k1, k2, k3, k4 = st.columns(4)


    # --------------------------------------------------------
    # KPI 1
    # --------------------------------------------------------

    with k1:

        st.metric(
            "📍 Districts",
            f"{number_of_districts:,}"
        )


    # --------------------------------------------------------
    # KPI 2
    # --------------------------------------------------------

    with k2:

        st.metric(
            "🌱 Estate Records",
            f"{number_of_estates:,}"
        )


    # --------------------------------------------------------
    # KPI 3
    # --------------------------------------------------------

    with k3:

        if avg_yield is not None and not pd.isna(avg_yield):

            st.metric(
                "☕ Average Yield",
                f"{avg_yield:,.0f} kg/ha"
            )

        else:

            st.metric(
                "☕ Average Yield",
                "—"
            )


    # --------------------------------------------------------
    # KPI 4
    # --------------------------------------------------------

    with k4:

        if avg_health is not None and not pd.isna(avg_health):

            st.metric(
                "❤️ Health Score",
                f"{avg_health:,.1f}"
            )

        else:

            st.metric(
                "❤️ Health Score",
                "—"
            )

