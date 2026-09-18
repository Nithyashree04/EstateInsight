# dashboard/quality.py

import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# THEME
# ============================================================

TEXT_DARK = "#2B211B"
TEXT_MUTED = "#766A5F"
GRID_COLOR = "#E7DED5"


# ============================================================
# COLUMN HELPERS
# ============================================================

def find_column(df, candidates):
    """
    Find a dataframe column using:
    1. Exact match
    2. Case-insensitive match
    3. Normalized match
    4. Partial match
    """

    if df is None or df.empty:
        return None

    columns = list(df.columns)

    # Exact
    for candidate in candidates:
        if candidate in columns:
            return candidate

    # Case-insensitive
    lower_map = {str(col).lower(): col for col in columns}

    for candidate in candidates:
        if str(candidate).lower() in lower_map:
            return lower_map[str(candidate).lower()]

    # Normalized
    def normalize(value):
        return (
            str(value)
            .lower()
            .replace("_", "")
            .replace("-", "")
            .replace(" ", "")
            .replace("%", "")
            .replace("(", "")
            .replace(")", "")
        )

    normalized_map = {
        normalize(col): col
        for col in columns
    }

    for candidate in candidates:
        normalized_candidate = normalize(candidate)

        if normalized_candidate in normalized_map:
            return normalized_map[normalized_candidate]

    # Partial match
    for candidate in candidates:
        candidate_norm = normalize(candidate)

        for col in columns:
            col_norm = normalize(col)

            if candidate_norm in col_norm or col_norm in candidate_norm:
                return col

    return None


def to_numeric(series):
    """
    Safely convert a series to numeric.
    """
    return pd.to_numeric(series, errors="coerce")


# ============================================================
# CHART STYLE
# ============================================================

def style_chart(fig, height=390):

    fig.update_layout(
        height=height,
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="white",
        font=dict(
            family="Arial",
            color=TEXT_DARK,
            size=13
        ),
        title_font=dict(
            color=TEXT_DARK,
            size=18
        ),
        margin=dict(
            l=45,
            r=25,
            t=55,
            b=50
        ),
        legend=dict(
            font=dict(
                color=TEXT_DARK
            )
        )
    )

    fig.update_xaxes(
        title_font=dict(
            color=TEXT_DARK,
            size=13
        ),
        tickfont=dict(
            color=TEXT_DARK
        ),
        gridcolor=GRID_COLOR,
        zeroline=False
    )

    fig.update_yaxes(
        title_font=dict(
            color=TEXT_DARK,
            size=13
        ),
        tickfont=dict(
            color=TEXT_DARK
        ),
        gridcolor=GRID_COLOR,
        zeroline=False
    )

    return fig


# ============================================================
# SAFE TEXT
# ============================================================

def safe_text(value, default="—"):

    if value is None:
        return default

    if pd.isna(value):
        return default

    text = str(value).strip()

    if not text:
        return default

    return text


# ============================================================
# MAIN PAGE
# ============================================================

def show_quality(df):

    st.title("☕ Coffee Quality Analytics")

    st.caption(
        "Understand coffee quality, production performance, "
        "coffee types and processing patterns across the estate."
    )

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if df is None or df.empty:
        st.warning("No data available for Coffee Quality Analytics.")
        return

    # Remove duplicate dataframe columns
    df = df.loc[:, ~df.columns.duplicated()].copy()

    # --------------------------------------------------------
    # COLUMN DETECTION
    # --------------------------------------------------------

    quality_col = find_column(
        df,
        [
            "Quality_Score",
            "Quality Score",
            "Coffee_Quality_Score",
            "Coffee Quality Score",
            "Quality"
        ]
    )

    yield_col = find_column(
        df,
        [
            "Yield_kg_ha",
            "Yield (kg/ha)",
            "Yield",
            "Production_Yield"
        ]
    )

    district_col = find_column(
        df,
        [
            "District",
            "District_Name",
            "Location"
        ]
    )

    coffee_type_col = find_column(
        df,
        [
            "Coffee_Type",
            "Coffee Type",
            "CoffeeType",
            "Variety",
            "Coffee_Variety"
        ]
    )

    processing_col = find_column(
        df,
        [
            "Processing_Method",
            "Processing Method",
            "Processing",
            "Process"
        ]
    )

    estate_col = find_column(
        df,
        [
            "Estate_ID",
            "Estate ID",
            "Estate",
            "Farm_ID",
            "Farm ID"
        ]
    )

    # --------------------------------------------------------
    # PREPARE NUMERIC DATA
    # --------------------------------------------------------

    quality_values = None
    yield_values = None

    if quality_col:
        quality_values = to_numeric(df[quality_col])

    if yield_col:
        yield_values = to_numeric(df[yield_col])

    # ========================================================
    # KPI SECTION
    # ========================================================

    st.markdown("### 📊 Quality Overview")

    k1, k2, k3, k4 = st.columns(4)

    # Average Quality
    with k1:

        if quality_values is not None:
            avg_quality = quality_values.mean()

            st.metric(
                "Average Quality Score",
                f"{avg_quality:.1f}" if pd.notna(avg_quality) else "—"
            )
        else:
            st.metric(
                "Average Quality Score",
                "—"
            )

    # Average Yield
    with k2:

        if yield_values is not None:
            avg_yield = yield_values.mean()

            st.metric(
                "Average Yield",
                f"{avg_yield:,.0f} kg/ha"
                if pd.notna(avg_yield)
                else "—"
            )
        else:
            st.metric(
                "Average Yield",
                "—"
            )

    # Dominant Coffee Type
    with k3:

        if coffee_type_col:

            type_data = (
                df[coffee_type_col]
                .dropna()
                .astype(str)
                .str.strip()
            )

            if not type_data.empty:

                dominant_type = type_data.value_counts().idxmax()

                st.metric(
                    "Dominant Coffee Type",
                    safe_text(dominant_type)
                )

            else:

                st.metric(
                    "Dominant Coffee Type",
                    "—"
                )

        else:

            st.metric(
                "Dominant Coffee Type",
                "—"
            )

    # Main Processing Method
    with k4:

        if processing_col:

            process_data = (
                df[processing_col]
                .dropna()
                .astype(str)
                .str.strip()
            )

            if not process_data.empty:

                dominant_process = process_data.value_counts().idxmax()

                st.metric(
                    "Main Processing Method",
                    safe_text(dominant_process)
                )

            else:

                st.metric(
                    "Main Processing Method",
                    "—"
                )

        else:

            st.metric(
                "Main Processing Method",
                "—"
            )

    st.divider()

    # ========================================================
    # CHART 1
    # QUALITY BY DISTRICT
    # ========================================================

    if quality_col and district_col:

        st.subheader("📍 Quality Score by District")

        district_data = df[
            [district_col, quality_col]
        ].copy()

        district_data[quality_col] = to_numeric(
            district_data[quality_col]
        )

        district_data = district_data.dropna(
            subset=[district_col, quality_col]
        )

        if not district_data.empty:

            district_quality = (
                district_data
                .groupby(district_col)[quality_col]
                .mean()
                .reset_index()
                .sort_values(
                    quality_col,
                    ascending=False
                )
            )

            fig = px.bar(
                district_quality,
                x=district_col,
                y=quality_col,
                text_auto=".1f",
                labels={
                    district_col: "District",
                    quality_col: "Average Quality Score"
                }
            )

            fig.update_traces(
                textposition="outside"
            )

            fig.update_layout(
                showlegend=False
            )

            fig = style_chart(
                fig,
                height=400
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "District quality data is not available."
            )

    # ========================================================
    # CHART 2
    # QUALITY BY COFFEE TYPE
    # ========================================================

    if quality_col and coffee_type_col:

        st.subheader("☕ Quality Score by Coffee Type")

        type_data = df[
            [coffee_type_col, quality_col]
        ].copy()

        type_data[quality_col] = to_numeric(
            type_data[quality_col]
        )

        type_data = type_data.dropna(
            subset=[
                coffee_type_col,
                quality_col
            ]
        )

        type_data[coffee_type_col] = (
            type_data[coffee_type_col]
            .astype(str)
            .str.strip()
        )

        type_data = type_data[
            type_data[coffee_type_col] != ""
        ]

        if not type_data.empty:

            type_quality = (
                type_data
                .groupby(coffee_type_col)[quality_col]
                .mean()
                .reset_index()
                .sort_values(
                    quality_col,
                    ascending=False
                )
            )

            fig = px.bar(
                type_quality,
                x=coffee_type_col,
                y=quality_col,
                text_auto=".1f",
                labels={
                    coffee_type_col: "Coffee Type",
                    quality_col: "Average Quality Score"
                }
            )

            fig.update_traces(
                textposition="outside"
            )

            fig.update_layout(
                showlegend=False
            )

            fig = style_chart(
                fig,
                height=390
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Coffee type quality data is not available."
            )

    # ========================================================
    # CHART 3
    # PROCESSING METHOD DISTRIBUTION
    # ========================================================

    if processing_col:

        st.subheader("⚙️ Processing Method Distribution")

        processing_data = (
            df[processing_col]
            .dropna()
            .astype(str)
            .str.strip()
        )

        processing_data = processing_data[
            processing_data != ""
        ]

        if not processing_data.empty:

            process_counts = (
                processing_data
                .value_counts()
                .reset_index()
            )

            process_counts.columns = [
                "Processing Method",
                "Number of Records"
            ]

            fig = px.bar(
                process_counts,
                x="Processing Method",
                y="Number of Records",
                text_auto=True,
                labels={
                    "Processing Method": "Processing Method",
                    "Number of Records": "Records"
                }
            )

            fig.update_traces(
                textposition="outside"
            )

            fig.update_layout(
                showlegend=False
            )

            fig = style_chart(
                fig,
                height=390
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "Processing method data is not available."
            )

    # ========================================================
    # KEY INSIGHTS
    # ========================================================

    st.divider()

    st.subheader("💡 Key Quality Insights")

    insight_cols = st.columns(3)

    # District insight
    with insight_cols[0]:

        if (
            quality_col
            and district_col
            and quality_values is not None
        ):

            district_data = df[
                [district_col, quality_col]
            ].copy()

            district_data[quality_col] = to_numeric(
                district_data[quality_col]
            )

            district_data = district_data.dropna(
                subset=[
                    district_col,
                    quality_col
                ]
            )

            if not district_data.empty:

                district_avg = (
                    district_data
                    .groupby(district_col)[quality_col]
                    .mean()
                    .sort_values(
                        ascending=False
                    )
                )

                best_district = district_avg.index[0]
                best_score = district_avg.iloc[0]

                st.info(
                    f"🏆 **Top Quality District**\n\n"
                    f"{best_district} records the highest "
                    f"average quality score of "
                    f"**{best_score:.1f}**."
                )

            else:

                st.info(
                    "District-level quality insight "
                    "is unavailable."
                )

        else:

            st.info(
                "District-level quality insight "
                "is unavailable."
            )

    # Coffee type insight
    with insight_cols[1]:

        if quality_col and coffee_type_col:

            type_data = df[
                [coffee_type_col, quality_col]
            ].copy()

            type_data[quality_col] = to_numeric(
                type_data[quality_col]
            )

            type_data = type_data.dropna(
                subset=[
                    coffee_type_col,
                    quality_col
                ]
            )

            if not type_data.empty:

                type_avg = (
                    type_data
                    .groupby(coffee_type_col)[quality_col]
                    .mean()
                    .sort_values(
                        ascending=False
                    )
                )

                best_type = type_avg.index[0]
                best_type_score = type_avg.iloc[0]

                st.success(
                    f"☕ **Best Performing Coffee Type**\n\n"
                    f"{best_type} has the highest "
                    f"average quality score of "
                    f"**{best_type_score:.1f}**."
                )

            else:

                st.success(
                    "Coffee type quality insight "
                    "is unavailable."
                )

        else:

            st.success(
                "Coffee type quality insight "
                "is unavailable."
            )

    # Processing insight
    with insight_cols[2]:

        if processing_col:

            processing_data = (
                df[processing_col]
                .dropna()
                .astype(str)
                .str.strip()
            )

            if not processing_data.empty:

                dominant_process = (
                    processing_data
                    .value_counts()
                    .idxmax()
                )

                dominant_count = (
                    processing_data
                    .value_counts()
                    .max()
                )

                st.warning(
                    f"⚙️ **Most Used Processing Method**\n\n"
                    f"{dominant_process} is the most common "
                    f"processing method with "
                    f"**{dominant_count:,} records**."
                )

            else:

                st.warning(
                    "Processing insight is unavailable."
                )

        else:

            st.warning(
                "Processing insight is unavailable."
            )

    # ========================================================
    # DATA COVERAGE
    # ========================================================

    with st.expander("🔎 Data Coverage"):

        coverage_cols = st.columns(4)

        with coverage_cols[0]:
            st.metric(
                "Records",
                f"{len(df):,}"
            )

        with coverage_cols[1]:
            st.metric(
                "Columns",
                f"{len(df.columns):,}"
            )

        with coverage_cols[2]:

            if estate_col:

                estate_count = (
                    df[estate_col]
                    .nunique()
                )

                st.metric(
                    "Estates",
                    f"{estate_count:,}"
                )

            else:

                st.metric(
                    "Estates",
                    "—"
                )

        with coverage_cols[3]:

            if district_col:

                district_count = (
                    df[district_col]
                    .nunique()
                )

                st.metric(
                    "Districts",
                    f"{district_count:,}"
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
        "EstateInsight • Coffee Quality Analytics"
    )