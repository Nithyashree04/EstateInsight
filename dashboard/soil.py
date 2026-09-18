# ============================================================
# EstateInsight
# Soil & Nutrient Analytics
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# COLOURS
# ============================================================

TEXT_DARK = "#2B211B"
TEXT_MUTED = "#766A5F"
GRID_COLOR = "#E5DDD5"

SOIL_GREEN = "#43A047"
MOISTURE_BLUE = "#0288D1"
ZINC_BLUE = "#1976D2"
IRON_ORANGE = "#EF6C00"
MAGNESIUM_PURPLE = "#7B1FA2"
SULFUR_YELLOW = "#F9A825"


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

def find_column(df, names):

    # Exact match
    for name in names:

        if name in df.columns:
            return name

    # Case-insensitive match
    lower_map = {
        str(col).strip().lower(): col
        for col in df.columns
    }

    for name in names:

        key = str(name).strip().lower()

        if key in lower_map:
            return lower_map[key]

    # Normalized match
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

    for name in names:

        key = normalize(name)

        if key in normalized_map:
            return normalized_map[key]

    return None


# ============================================================
# NUMERIC CONVERSION
# ============================================================

def numeric_column(df, column):

    if column is None:
        return pd.Series(dtype="float64")

    return pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ============================================================
# CHART STYLE
# ============================================================

def style_chart(fig, height=390):

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
        ),

        legend=dict(
            font=dict(
                color=TEXT_DARK
            )
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
# MAIN PAGE
# ============================================================

def show_soil(df):

    # ========================================================
    # HEADER
    # ========================================================

    st.title("🌱 Soil & Nutrient Analytics")

    st.caption(
        "Monitor soil moisture and essential micronutrients "
        "to understand soil conditions across the coffee estate."
    )

    # ========================================================
    # VALIDATION
    # ========================================================

    if df is None:

        st.error(
            "Soil dataset could not be loaded."
        )

        return

    if df.empty:

        st.warning(
            "No soil records are available for the current filters."
        )

        return

    # ========================================================
    # CLEAN DATA
    # ========================================================

    df = clean_dataframe(df)

    # ========================================================
    # ACTUAL DATASET COLUMNS
    # ========================================================

    moisture_col = find_column(
        df,
        [
            "Soil_Moisture_%",
            "Soil Moisture %",
            "Soil_Moisture",
            "Soil Moisture"
        ]
    )

    zinc_col = find_column(
        df,
        [
            "Zn_ppm",
            "Zinc_ppm",
            "Zinc",
            "Zn"
        ]
    )

    iron_col = find_column(
        df,
        [
            "Fe_ppm",
            "Iron_ppm",
            "Iron",
            "Fe"
        ]
    )

    magnesium_col = find_column(
        df,
        [
            "Mg_ppm",
            "Magnesium_ppm",
            "Magnesium",
            "Mg"
        ]
    )

    sulfur_col = find_column(
        df,
        [
            "S_ppm",
            "Sulfur_ppm",
            "Sulphur_ppm",
            "Sulfur",
            "Sulphur",
            "S"
        ]
    )

    district_col = find_column(
        df,
        [
            "District"
        ]
    )

    # ========================================================
    # CONVERT TO NUMERIC
    # ========================================================

    for col in [
        moisture_col,
        zinc_col,
        iron_col,
        magnesium_col,
        sulfur_col
    ]:

        if col is not None:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # ========================================================
    # CALCULATE AVERAGES
    # ========================================================

    moisture_avg = (
        df[moisture_col].mean()
        if moisture_col
        and df[moisture_col].notna().any()
        else None
    )

    zinc_avg = (
        df[zinc_col].mean()
        if zinc_col
        and df[zinc_col].notna().any()
        else None
    )

    iron_avg = (
        df[iron_col].mean()
        if iron_col
        and df[iron_col].notna().any()
        else None
    )

    magnesium_avg = (
        df[magnesium_col].mean()
        if magnesium_col
        and df[magnesium_col].notna().any()
        else None
    )

    sulfur_avg = (
        df[sulfur_col].mean()
        if sulfur_col
        and df[sulfur_col].notna().any()
        else None
    )

    # ========================================================
    # SNAPSHOT
    # ========================================================

    st.markdown(
        "### 🌿 Estate Soil Snapshot"
    )

    k1, k2, k3, k4 = st.columns(4)

    # --------------------------------------------------------
    # SOIL MOISTURE
    # --------------------------------------------------------

    with k1:

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

    # --------------------------------------------------------
    # ZINC
    # --------------------------------------------------------

    with k2:

        if zinc_avg is not None:

            st.metric(
                "🔵 Zinc",
                f"{zinc_avg:.2f} ppm"
            )

        else:

            st.metric(
                "🔵 Zinc",
                "—"
            )

    # --------------------------------------------------------
    # IRON
    # --------------------------------------------------------

    with k3:

        if iron_avg is not None:

            st.metric(
                "🟠 Iron",
                f"{iron_avg:.2f} ppm"
            )

        else:

            st.metric(
                "🟠 Iron",
                "—"
            )

    # --------------------------------------------------------
    # MAGNESIUM
    # --------------------------------------------------------

    with k4:

        if magnesium_avg is not None:

            st.metric(
                "🟣 Magnesium",
                f"{magnesium_avg:.2f} ppm"
            )

        else:

            st.metric(
                "🟣 Magnesium",
                "—"
            )

    # ========================================================
    # SOIL MOISTURE STATUS
    # ========================================================

    if moisture_avg is not None:

        if moisture_avg < 30:

            st.warning(
                f"💧 **Soil Moisture: Relatively Low** — "
                f"average moisture is **{moisture_avg:.1f}%**."
            )

        elif moisture_avg <= 50:

            st.success(
                f"💧 **Soil Moisture: Moderate** — "
                f"average moisture is **{moisture_avg:.1f}%**."
            )

        else:

            st.info(
                f"💧 **Soil Moisture: Relatively High** — "
                f"average moisture is **{moisture_avg:.1f}%**."
            )

    # ========================================================
    # DISTRICT ANALYSIS
    # ========================================================

    st.divider()

    st.subheader(
        "📍 Soil Condition by District"
    )

    st.caption(
        "Compare soil moisture and micronutrient levels "
        "across the estate districts."
    )

    # ========================================================
    # SOIL MOISTURE BY DISTRICT
    # ========================================================

    if (
        district_col is not None
        and moisture_col is not None
    ):

        moisture_data = (

            df.groupby(district_col)[moisture_col]

            .mean()

            .reset_index()

            .dropna()
        )

        moisture_data = moisture_data.sort_values(
            moisture_col,
            ascending=False
        )

        if not moisture_data.empty:

            fig_moisture = px.bar(

                moisture_data,

                x=district_col,

                y=moisture_col,

                text=moisture_col,

                color=district_col,

                color_discrete_sequence=[
                    MOISTURE_BLUE,
                    SOIL_GREEN,
                    "#26A69A"
                ],

                title="💧 Average Soil Moisture by District",

                labels={
                    district_col: "District",
                    moisture_col:
                        "Average Soil Moisture (%)"
                }
            )

            fig_moisture.update_traces(

                texttemplate="%{text:.1f}%",

                textposition="outside",

                marker_line_width=0
            )

            fig_moisture.update_layout(
                showlegend=False
            )

            fig_moisture = style_chart(
                fig_moisture,
                390
            )

            st.plotly_chart(
                fig_moisture,
                use_container_width=True
            )

    # ========================================================
    # MICRONUTRIENTS BY DISTRICT
    # ========================================================

    nutrient_columns = {}

    if zinc_col is not None:
        nutrient_columns["Zinc"] = zinc_col

    if iron_col is not None:
        nutrient_columns["Iron"] = iron_col

    if magnesium_col is not None:
        nutrient_columns["Magnesium"] = magnesium_col

    if sulfur_col is not None:
        nutrient_columns["Sulfur"] = sulfur_col

    if (
        district_col is not None
        and nutrient_columns
    ):

        nutrient_rows = []

        for district, group in df.groupby(
            district_col
        ):

            for nutrient_name, column in (
                nutrient_columns.items()
            ):

                value = group[column].mean()

                if pd.notna(value):

                    nutrient_rows.append(
                        {
                            "District": district,
                            "Nutrient": nutrient_name,
                            "Average": value
                        }
                    )

        nutrient_df = pd.DataFrame(
            nutrient_rows
        )

        if not nutrient_df.empty:

            fig_nutrients = px.bar(

                nutrient_df,

                x="District",

                y="Average",

                color="Nutrient",

                barmode="group",

                text="Average",

                color_discrete_map={

                    "Zinc":
                        ZINC_BLUE,

                    "Iron":
                        IRON_ORANGE,

                    "Magnesium":
                        MAGNESIUM_PURPLE,

                    "Sulfur":
                        SULFUR_YELLOW
                },

                title="🧪 Micronutrient Levels by District",

                labels={
                    "District":
                        "District",

                    "Average":
                        "Average Level (ppm)",

                    "Nutrient":
                        "Nutrient"
                }
            )

            fig_nutrients.update_traces(

                texttemplate="%{text:.1f}",

                textposition="outside",

                marker_line_width=0
            )

            fig_nutrients = style_chart(
                fig_nutrients,
                430
            )

            st.plotly_chart(
                fig_nutrients,
                use_container_width=True
            )

    # ========================================================
    # SIMPLE INSIGHTS
    # ========================================================

    st.divider()

    st.subheader(
        "📋 Soil Health Summary"
    )

    insight1, insight2, insight3 = st.columns(3)

    # ========================================================
    # HIGHEST MOISTURE
    # ========================================================

    with insight1:

        if (
            district_col is not None
            and moisture_col is not None
        ):

            moisture_by_district = (
                df.groupby(district_col)[moisture_col]
                .mean()
                .dropna()
            )

            if not moisture_by_district.empty:

                highest_district = (
                    moisture_by_district.idxmax()
                )

                highest_value = (
                    moisture_by_district.max()
                )

                st.info(
                    f"💧 **Highest Soil Moisture**\n\n"
                    f"**{highest_district}**\n\n"
                    f"{highest_value:.1f}% average moisture"
                )

    # ========================================================
    # HIGHEST ZINC
    # ========================================================

    with insight2:

        if (
            district_col is not None
            and zinc_col is not None
        ):

            zinc_by_district = (
                df.groupby(district_col)[zinc_col]
                .mean()
                .dropna()
            )

            if not zinc_by_district.empty:

                zinc_district = (
                    zinc_by_district.idxmax()
                )

                zinc_value = (
                    zinc_by_district.max()
                )

                st.success(
                    f"🔵 **Highest Zinc Level**\n\n"
                    f"**{zinc_district}**\n\n"
                    f"{zinc_value:.2f} ppm average"
                )

    # ========================================================
    # HIGHEST MAGNESIUM
    # ========================================================

    with insight3:

        if (
            district_col is not None
            and magnesium_col is not None
        ):

            mg_by_district = (
                df.groupby(district_col)[magnesium_col]
                .mean()
                .dropna()
            )

            if not mg_by_district.empty:

                mg_district = (
                    mg_by_district.idxmax()
                )

                mg_value = (
                    mg_by_district.max()
                )

                st.warning(
                    f"🟣 **Highest Magnesium Level**\n\n"
                    f"**{mg_district}**\n\n"
                    f"{mg_value:.2f} ppm average"
                )

    # ========================================================
    # MICRONUTRIENT EXPLANATION
    # ========================================================

    st.divider()

    st.subheader(
        "💡 Understanding the Soil Data"
    )

    with st.expander(
        "💧 Soil Moisture"
    ):

        st.write(
            "Soil moisture indicates the amount of water "
            "available in the soil. Comparing districts "
            "helps identify areas with relatively drier "
            "or wetter soil conditions."
        )

    with st.expander(
        "🧪 Micronutrients"
    ):

        st.write(
            "The dataset records Zinc, Iron, Magnesium "
            "and Sulfur in ppm. The district comparison "
            "helps identify differences in recorded "
            "micronutrient levels."
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
                "Soil Moisture",
                "Available"
                if moisture_col is not None
                else "Not found"
            )

        with c3:

            st.metric(
                "Micronutrients",
                f"{len(nutrient_columns)}/4"
            )

        with c4:

            if district_col is not None:

                st.metric(
                    "Districts",
                    f"{df[district_col].nunique():,}"
                )

            else:

                st.metric(
                    "Districts",
                    "—"
                )

    # ========================================================
    # FOOTER
    # ========================================================

    st.caption(
        "EstateInsight • Soil & Nutrient Analytics ☕🌱"
    )