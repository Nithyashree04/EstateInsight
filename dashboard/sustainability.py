# ============================================================
# EstateInsight
# Sustainability Analytics
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# COLOUR PALETTE
# ============================================================

TEXT_DARK = "#2B211B"
TEXT_MUTED = "#766A5F"
GRID_COLOR = "#E5DDD5"

GREEN = "#2E7D32"
LIGHT_GREEN = "#66BB6A"
DARK_GREEN = "#1B5E20"
TEAL = "#00897B"
BLUE = "#1976D2"
ORANGE = "#EF6C00"
BROWN = "#795548"


# ============================================================
# DATA CLEANING
# ============================================================

def clean_dataframe(df):

    if df is None:
        return pd.DataFrame()

    data = df.copy()

    # Remove duplicate columns
    data = data.loc[
        :,
        ~data.columns.duplicated()
    ].copy()

    # Clean column names
    data.columns = [
        str(col).strip()
        for col in data.columns
    ]

    return data


# ============================================================
# FIND COLUMN
# ============================================================

def find_column(df, possible_names):

    # Exact
    for name in possible_names:

        if name in df.columns:
            return name

    # Case insensitive
    lower_map = {
        str(col).strip().lower(): col
        for col in df.columns
    }

    for name in possible_names:

        key = str(name).strip().lower()

        if key in lower_map:
            return lower_map[key]

    # Normalized
    def normalize(value):

        return (
            str(value)
            .lower()
            .strip()
            .replace("_", "")
            .replace(" ", "")
            .replace("%", "percent")
            .replace("/", "")
        )

    normalized_map = {
        normalize(col): col
        for col in df.columns
    }

    for name in possible_names:

        key = normalize(name)

        if key in normalized_map:
            return normalized_map[key]

    return None


# ============================================================
# CHART STYLE
# ============================================================

def style_chart(fig, height=400):

    fig.update_layout(

        height=height,

        template="plotly_white",

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="#FFFFFF",

        font=dict(
            family="Arial",
            color=TEXT_DARK,
            size=13
        ),

        title_font=dict(
            family="Arial",
            color=TEXT_DARK,
            size=18
        ),

        margin=dict(
            l=55,
            r=35,
            t=70,
            b=55
        ),

        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font_color=TEXT_DARK,
            font_size=13
        )
    )

    fig.update_xaxes(

        gridcolor=GRID_COLOR,

        zeroline=False,

        tickfont=dict(
            color=TEXT_DARK
        ),

        title_font=dict(
            color=TEXT_DARK
        )
    )

    fig.update_yaxes(

        gridcolor=GRID_COLOR,

        zeroline=False,

        tickfont=dict(
            color=TEXT_DARK
        ),

        title_font=dict(
            color=TEXT_DARK
        )
    )

    return fig


# ============================================================
# MAIN SUSTAINABILITY PAGE
# ============================================================

def show_sustainability(df):

    # ========================================================
    # HEADER
    # ========================================================

    st.title("♻️ Sustainability Analytics")

    st.caption(
        "Monitor sustainability performance, carbon footprint "
        "and resource indicators across the coffee estate."
    )

    # ========================================================
    # VALIDATION
    # ========================================================

    if df is None:

        st.error(
            "Sustainability dataset could not be loaded."
        )

        return

    if df.empty:

        st.warning(
            "No sustainability records are available "
            "for the current filters."
        )

        return

    # ========================================================
    # CLEAN DATA
    # ========================================================

    df = clean_dataframe(df)

    # ========================================================
    # FIND ACTUAL DATASET COLUMNS
    # ========================================================

    sustainability_col = find_column(
        df,
        [
            "Sustainability_Score",
            "Sustainability Score",
            "SustainabilityScore"
        ]
    )

    carbon_col = find_column(
        df,
        [
            "Carbon_Footprint_tCO2e",
            "Carbon Footprint tCO2e",
            "Carbon_Footprint",
            "Carbon Footprint"
        ]
    )

    yield_col = find_column(
        df,
        [
            "Yield_kg_ha",
            "Yield kg/ha",
            "Yield",
            "Yield_kg"
        ]
    )

    moisture_col = find_column(
        df,
        [
            "Soil_Moisture_%",
            "Soil Moisture %",
            "Soil_Moisture",
            "Soil Moisture"
        ]
    )

    farm_size_col = find_column(
        df,
        [
            "Farm_Size_Acres",
            "Farm Size Acres",
            "Farm_Size",
            "Farm Size"
        ]
    )

    district_col = find_column(
        df,
        [
            "District"
        ]
    )

    coffee_type_col = find_column(
        df,
        [
            "Coffee_Type",
            "Coffee Type"
        ]
    )

    processing_col = find_column(
        df,
        [
            "Processing_Method",
            "Processing Method"
        ]
    )

    # ========================================================
    # NUMERIC CONVERSION
    # ========================================================

    numeric_columns = [
        sustainability_col,
        carbon_col,
        yield_col,
        moisture_col,
        farm_size_col
    ]

    for column in numeric_columns:

        if column is not None:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # ========================================================
    # CALCULATE MAIN VALUES
    # ========================================================

    sustainability_avg = None
    carbon_avg = None
    yield_avg = None
    moisture_avg = None

    if (
        sustainability_col is not None
        and df[sustainability_col].notna().any()
    ):

        sustainability_avg = (
            df[sustainability_col].mean()
        )

    if (
        carbon_col is not None
        and df[carbon_col].notna().any()
    ):

        carbon_avg = (
            df[carbon_col].mean()
        )

    if (
        yield_col is not None
        and df[yield_col].notna().any()
    ):

        yield_avg = (
            df[yield_col].mean()
        )

    if (
        moisture_col is not None
        and df[moisture_col].notna().any()
    ):

        moisture_avg = (
            df[moisture_col].mean()
        )

    # ========================================================
    # ESTATE SNAPSHOT
    # ========================================================

    st.subheader(
        "🌿 Estate Sustainability Snapshot"
    )

    k1, k2, k3, k4 = st.columns(4)

    # --------------------------------------------------------
    # SUSTAINABILITY SCORE
    # --------------------------------------------------------

    with k1:

        if sustainability_avg is not None:

            st.metric(
                "🌱 Sustainability Score",
                f"{sustainability_avg:.1f}"
            )

        else:

            st.metric(
                "🌱 Sustainability Score",
                "—"
            )

    # --------------------------------------------------------
    # CARBON
    # --------------------------------------------------------

    with k2:

        if carbon_avg is not None:

            st.metric(
                "🌍 Carbon Footprint",
                f"{carbon_avg:.2f} tCO₂e"
            )

        else:

            st.metric(
                "🌍 Carbon Footprint",
                "—"
            )

    # --------------------------------------------------------
    # YIELD
    # --------------------------------------------------------

    with k3:

        if yield_avg is not None:

            st.metric(
                "☕ Average Yield",
                f"{yield_avg:,.0f} kg/ha"
            )

        else:

            st.metric(
                "☕ Average Yield",
                "—"
            )

    # --------------------------------------------------------
    # SOIL MOISTURE
    # --------------------------------------------------------

    with k4:

        if moisture_avg is not None:

            st.metric(
                "💧 Soil Moisture",
                f"{moisture_avg:.1f}%"
            )

        else:

            st.metric(
                "💧 Soil Moisture",
                "—"
            )

    # ========================================================
    # OVERALL STATUS
    # ========================================================

    if sustainability_avg is not None:

        if sustainability_avg >= 80:

            st.success(
                f"🌿 **Strong Sustainability Performance** — "
                f"the estate has an average sustainability "
                f"score of **{sustainability_avg:.1f}**."
            )

        elif sustainability_avg >= 65:

            st.info(
                f"🌱 **Moderate Sustainability Performance** — "
                f"the average sustainability score is "
                f"**{sustainability_avg:.1f}**."
            )

        else:

            st.warning(
                f"🌾 **Sustainability Needs Attention** — "
                f"the average sustainability score is "
                f"**{sustainability_avg:.1f}**."
            )

    # ========================================================
    # DISTRICT ANALYSIS
    # ========================================================

    st.divider()

    st.subheader(
        "📍 Sustainability by District"
    )

    st.caption(
        "Compare sustainability performance across "
        "the major coffee-growing districts."
    )

    # ========================================================
    # SUSTAINABILITY SCORE BY DISTRICT
    # ========================================================

    if (
        district_col is not None
        and sustainability_col is not None
    ):

        district_data = (

            df.groupby(district_col)[sustainability_col]

            .mean()

            .reset_index()

            .dropna()
        )

        district_data = district_data.sort_values(
            sustainability_col,
            ascending=False
        )

        if not district_data.empty:

            fig_district = px.bar(

                district_data,

                x=district_col,

                y=sustainability_col,

                color=district_col,

                text=sustainability_col,

                color_discrete_sequence=[
                    DARK_GREEN,
                    GREEN,
                    LIGHT_GREEN
                ],

                title="🌱 Average Sustainability Score by District",

                labels={
                    district_col:
                        "District",

                    sustainability_col:
                        "Average Sustainability Score"
                }
            )

            fig_district.update_traces(

                texttemplate="%{text:.1f}",

                textposition="outside",

                marker_line_width=0
            )

            fig_district.update_layout(
                showlegend=False
            )

            fig_district = style_chart(
                fig_district,
                410
            )

            st.plotly_chart(
                fig_district,
                use_container_width=True
            )

    # ========================================================
    # COFFEE TYPE ANALYSIS
    # ========================================================

    st.divider()

    st.subheader(
        "☕ Sustainability by Coffee Type"
    )

    st.caption(
        "See how recorded sustainability scores differ "
        "between coffee types."
    )

    if (
        coffee_type_col is not None
        and sustainability_col is not None
    ):

        coffee_data = (

            df.groupby(coffee_type_col)[
                sustainability_col
            ]

            .mean()

            .reset_index()

            .dropna()
        )

        coffee_data = coffee_data.sort_values(
            sustainability_col,
            ascending=False
        )

        if not coffee_data.empty:

            fig_coffee = px.bar(

                coffee_data,

                x=coffee_type_col,

                y=sustainability_col,

                color=coffee_type_col,

                text=sustainability_col,

                color_discrete_sequence=[
                    BROWN,
                    GREEN,
                    TEAL,
                    ORANGE
                ],

                title="☕ Average Sustainability Score by Coffee Type",

                labels={
                    coffee_type_col:
                        "Coffee Type",

                    sustainability_col:
                        "Average Sustainability Score"
                }
            )

            fig_coffee.update_traces(

                texttemplate="%{text:.1f}",

                textposition="outside",

                marker_line_width=0
            )

            fig_coffee.update_layout(
                showlegend=False
            )

            fig_coffee = style_chart(
                fig_coffee,
                400
            )

            st.plotly_chart(
                fig_coffee,
                use_container_width=True
            )

    # ========================================================
    # SIMPLE INSIGHTS
    # ========================================================

    st.divider()

    st.subheader(
        "📋 Sustainability Insights"
    )

    col1, col2, col3 = st.columns(3)

    # ========================================================
    # BEST DISTRICT
    # ========================================================

    with col1:

        if (
            district_col is not None
            and sustainability_col is not None
        ):

            district_scores = (

                df.groupby(district_col)[
                    sustainability_col
                ]

                .mean()

                .dropna()
            )

            if not district_scores.empty:

                best_district = (
                    district_scores.idxmax()
                )

                best_score = (
                    district_scores.max()
                )

                st.success(
                    f"🌱 **Top District**\n\n"
                    f"**{best_district}**\n\n"
                    f"Score: {best_score:.1f}"
                )

    # ========================================================
    # LOWEST CARBON
    # ========================================================

    with col2:

        if (
            district_col is not None
            and carbon_col is not None
        ):

            carbon_by_district = (

                df.groupby(district_col)[
                    carbon_col
                ]

                .mean()

                .dropna()
            )

            if not carbon_by_district.empty:

                low_carbon_district = (
                    carbon_by_district.idxmin()
                )

                low_carbon_value = (
                    carbon_by_district.min()
                )

                st.info(
                    f"🌍 **Lowest Recorded Carbon**\n\n"
                    f"**{low_carbon_district}**\n\n"
                    f"{low_carbon_value:.2f} tCO₂e"
                )

    # ========================================================
    # BEST COFFEE TYPE
    # ========================================================

    with col3:

        if (
            coffee_type_col is not None
            and sustainability_col is not None
        ):

            coffee_scores = (

                df.groupby(coffee_type_col)[
                    sustainability_col
                ]

                .mean()

                .dropna()
            )

            if not coffee_scores.empty:

                best_coffee = (
                    coffee_scores.idxmax()
                )

                best_coffee_score = (
                    coffee_scores.max()
                )

                st.warning(
                    f"☕ **Top Coffee Type**\n\n"
                    f"**{best_coffee}**\n\n"
                    f"Score: {best_coffee_score:.1f}"
                )

    # ========================================================
    # SUSTAINABILITY EXPLANATION
    # ========================================================

    st.divider()

    st.subheader(
        "💡 Understanding Sustainability"
    )

    with st.expander(
        "🌱 Sustainability Score"
    ):

        st.write(
            "The sustainability score provides an overall "
            "indicator of sustainability performance in "
            "the estate dataset. Higher scores indicate "
            "stronger recorded sustainability performance."
        )

    with st.expander(
        "🌍 Carbon Footprint"
    ):

        st.write(
            "Carbon footprint represents the recorded "
            "carbon emissions associated with the estate "
            "data. Lower recorded values indicate a lower "
            "carbon footprint."
        )

    with st.expander(
        "☕ Production & Sustainability"
    ):

        st.write(
            "Yield and sustainability should be considered "
            "together when evaluating estate performance. "
            "The dashboard presents these indicators "
            "separately so estate managers can compare "
            "production and sustainability."
        )

    # ========================================================
    # DATA COVERAGE
    # ========================================================

    with st.expander(
        "🔎 Data Coverage"
    ):

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Records",
                f"{len(df):,}"
            )

        with c2:

            st.metric(
                "Districts",
                (
                    f"{df[district_col].nunique():,}"
                    if district_col is not None
                    else "—"
                )
            )

        with c3:

            st.metric(
                "Coffee Types",
                (
                    f"{df[coffee_type_col].nunique():,}"
                    if coffee_type_col is not None
                    else "—"
                )
            )

        with c4:

            available = sum(
                column is not None
                for column in [
                    sustainability_col,
                    carbon_col,
                    yield_col,
                    moisture_col
                ]
            )

            st.metric(
                "Key Indicators",
                f"{available}/4"
            )

    # ========================================================
    # FOOTER
    # ========================================================

    st.caption(
        "EstateInsight • Sustainability Analytics ☕🌱"
    )