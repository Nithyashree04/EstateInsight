# ============================================================
# ESTATEINSIGHT - SMART SEARCH
# dashboard/search.py
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np


# ============================================================
# COLUMN DETECTION
# ============================================================

def find_column(df, candidates):
    """
    Finds a dataset column using exact, normalized and partial matching.
    """

    if df is None or df.empty:
        return None

    columns = list(df.columns)

    # Exact match
    for candidate in candidates:
        for col in columns:
            if str(col).strip().lower() == str(candidate).strip().lower():
                return col

    # Normalized match
    def normalize(value):
        return (
            str(value)
            .strip()
            .lower()
            .replace("_", "")
            .replace("-", "")
            .replace(" ", "")
            .replace("(", "")
            .replace(")", "")
            .replace("%", "")
        )

    normalized_columns = {
        normalize(col): col
        for col in columns
    }

    for candidate in candidates:
        key = normalize(candidate)

        if key in normalized_columns:
            return normalized_columns[key]

    # Partial match
    for candidate in candidates:
        key = normalize(candidate)

        for col in columns:
            normalized_col = normalize(col)

            if key in normalized_col or normalized_col in key:
                return col

    return None


def numeric_column(df, column):
    """
    Safely converts a dataframe column to numeric.
    """

    if column is None or column not in df.columns:
        return pd.Series(dtype=float)

    return pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ============================================================
# PAGE STYLING
# ============================================================

def apply_search_style():

    st.markdown(
        """
        <style>

        /* Search input */
        div[data-testid="stTextInput"] input {
            color: #222222 !important;
            background-color: #ffffff !important;
            -webkit-text-fill-color: #222222 !important;
            caret-color: #222222 !important;
            border-radius: 10px !important;
        }

        /* Select boxes */
        div[data-baseweb="select"] {
            border-radius: 10px !important;
        }

        /* Number inputs */
        div[data-testid="stNumberInput"] input {
            color: #222222 !important;
            background-color: #ffffff !important;
            -webkit-text-fill-color: #222222 !important;
        }

        /* Slider text */
        div[data-testid="stSlider"] {
            color: #33251F !important;
        }

        /* Result table */
        div[data-testid="stDataFrame"] {
            border-radius: 12px !important;
            overflow: hidden !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MAIN SEARCH PAGE
# ============================================================

def show_search(df):

    apply_search_style()

    # --------------------------------------------------------
    # Validate dataframe
    # --------------------------------------------------------

    if df is None or df.empty:

        st.title("🔎 Smart Search")

        st.info(
            "No estate records are currently available."
        )

        return

    # --------------------------------------------------------
    # Remove duplicate columns
    # --------------------------------------------------------

    df = df.loc[:, ~df.columns.duplicated()].copy()

    # --------------------------------------------------------
    # Detect important columns
    # --------------------------------------------------------

    district_col = find_column(
        df,
        [
            "District",
            "district",
            "Location"
        ]
    )

    coffee_col = find_column(
        df,
        [
            "Coffee_Type",
            "Coffee Type",
            "CoffeeType",
            "Type"
        ]
    )

    processing_col = find_column(
        df,
        [
            "Processing_Method",
            "Processing Method",
            "ProcessingMethod",
            "Processing"
        ]
    )

    yield_col = find_column(
        df,
        [
            "Yield_kg_ha",
            "Yield (kg/ha)",
            "Yield",
            "Production_Yield",
            "Production Yield"
        ]
    )

    health_col = find_column(
        df,
        [
            "Health_Score",
            "Health Score",
            "Estate_Health",
            "Estate Health",
            "Health"
        ]
    )

    sustainability_col = find_column(
        df,
        [
            "Sustainability_Score",
            "Sustainability Score",
            "Sustainability"
        ]
    )

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.title("🔎 Smart Search")

    st.caption(
        "Search, filter and explore coffee-estate records using "
        "operational, environmental and performance indicators."
    )

    st.divider()

    # ========================================================
    # KEYWORD SEARCH
    # ========================================================

    st.subheader("🔍 Search Estate Records")

    search_text = st.text_input(
        "Search",
        placeholder=(
            "Enter district, coffee type, processing method "
            "or any keyword..."
        ),
        label_visibility="collapsed"
    )

    st.caption(
        "Search works across all available dataset columns."
    )

    # ========================================================
    # SEARCH FILTERS
    # ========================================================

    st.subheader("🎛️ Search Filters")

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    # --------------------------------------------------------
    # District
    # --------------------------------------------------------

    with filter_col1:

        if district_col:

            districts = (
                df[district_col]
                .dropna()
                .astype(str)
                .str.strip()
                .replace("", np.nan)
                .dropna()
                .unique()
                .tolist()
            )

            districts = sorted(districts)

            selected_district = st.selectbox(
                "📍 District",
                ["All Districts"] + districts
            )

        else:

            selected_district = "All Districts"

    # --------------------------------------------------------
    # Coffee Type
    # --------------------------------------------------------

    with filter_col2:

        if coffee_col:

            coffee_types = (
                df[coffee_col]
                .dropna()
                .astype(str)
                .str.strip()
                .replace("", np.nan)
                .dropna()
                .unique()
                .tolist()
            )

            coffee_types = sorted(coffee_types)

            selected_coffee = st.selectbox(
                "☕ Coffee Type",
                ["All Types"] + coffee_types
            )

        else:

            selected_coffee = "All Types"

    # --------------------------------------------------------
    # Processing Method
    # --------------------------------------------------------

    with filter_col3:

        if processing_col:

            processing_methods = (
                df[processing_col]
                .dropna()
                .astype(str)
                .str.strip()
                .replace("", np.nan)
                .dropna()
                .unique()
                .tolist()
            )

            processing_methods = sorted(processing_methods)

            selected_processing = st.selectbox(
                "⚙️ Processing Method",
                ["All Methods"] + processing_methods
            )

        else:

            selected_processing = "All Methods"

    # ========================================================
    # PERFORMANCE FILTERS
    # ========================================================

    st.subheader("📊 Performance Filters")

    performance_col1, performance_col2, performance_col3 = st.columns(3)

    # --------------------------------------------------------
    # Yield
    # --------------------------------------------------------

    yield_values = numeric_column(df, yield_col)

    if not yield_values.empty and yield_values.notna().any():

        yield_min = float(yield_values.min())
        yield_max = float(yield_values.max())

        with performance_col1:

            min_yield = st.number_input(
                "🌱 Minimum Yield (kg/ha)",
                min_value=0.0,
                max_value=float(max(yield_max, 1)),
                value=0.0,
                step=50.0
            )

    else:

        min_yield = 0.0

    # --------------------------------------------------------
    # Health
    # --------------------------------------------------------

    health_values = numeric_column(df, health_col)

    if not health_values.empty and health_values.notna().any():

        health_max = float(health_values.max())

        with performance_col2:

            min_health = st.slider(
                "❤️ Minimum Health Score",
                min_value=0.0,
                max_value=float(max(health_max, 100)),
                value=0.0
            )

    else:

        min_health = 0.0

    # --------------------------------------------------------
    # Sustainability
    # --------------------------------------------------------

    sustainability_values = numeric_column(
        df,
        sustainability_col
    )

    if (
        not sustainability_values.empty
        and sustainability_values.notna().any()
    ):

        sustainability_max = float(
            sustainability_values.max()
        )

        with performance_col3:

            min_sustainability = st.slider(
                "♻️ Minimum Sustainability",
                min_value=0.0,
                max_value=float(
                    max(sustainability_max, 100)
                ),
                value=0.0
            )

    else:

        min_sustainability = 0.0

    st.divider()

    # ========================================================
    # APPLY FILTERS
    # ========================================================

    filtered_df = df.copy()

    # --------------------------------------------------------
    # Keyword search
    # --------------------------------------------------------

    if search_text.strip():

        keyword = search_text.strip().lower()

        # Convert every column to string and search across
        # the complete record.
        search_mask = pd.Series(
            False,
            index=filtered_df.index
        )

        for column in filtered_df.columns:

            values = (
                filtered_df[column]
                .astype(str)
                .str.lower()
                .str.contains(
                    keyword,
                    na=False,
                    regex=False
                )
            )

            search_mask = search_mask | values

        filtered_df = filtered_df.loc[search_mask]

    # --------------------------------------------------------
    # District
    # --------------------------------------------------------

    if (
        district_col
        and selected_district != "All Districts"
    ):

        filtered_df = filtered_df[
            filtered_df[district_col]
            .astype(str)
            .str.strip()
            .str.lower()
            == selected_district.lower()
        ]

    # --------------------------------------------------------
    # Coffee Type
    # --------------------------------------------------------

    if (
        coffee_col
        and selected_coffee != "All Types"
    ):

        filtered_df = filtered_df[
            filtered_df[coffee_col]
            .astype(str)
            .str.strip()
            .str.lower()
            == selected_coffee.lower()
        ]

    # --------------------------------------------------------
    # Processing Method
    # --------------------------------------------------------

    if (
        processing_col
        and selected_processing != "All Methods"
    ):

        filtered_df = filtered_df[
            filtered_df[processing_col]
            .astype(str)
            .str.strip()
            .str.lower()
            == selected_processing.lower()
        ]

    # --------------------------------------------------------
    # Minimum Yield
    # --------------------------------------------------------

    if yield_col and min_yield > 0:

        filtered_yield = numeric_column(
            filtered_df,
            yield_col
        )

        filtered_df = filtered_df[
            filtered_yield >= min_yield
        ]

    # --------------------------------------------------------
    # Minimum Health
    # --------------------------------------------------------

    if health_col and min_health > 0:

        filtered_health = numeric_column(
            filtered_df,
            health_col
        )

        filtered_df = filtered_df[
            filtered_health >= min_health
        ]

    # --------------------------------------------------------
    # Minimum Sustainability
    # --------------------------------------------------------

    if (
        sustainability_col
        and min_sustainability > 0
    ):

        filtered_sustainability = numeric_column(
            filtered_df,
            sustainability_col
        )

        filtered_df = filtered_df[
            filtered_sustainability >= min_sustainability
        ]

    # ========================================================
    # RESULTS SUMMARY
    # ========================================================

    st.subheader("📋 Search Results")

    result_count = len(filtered_df)
    total_count = len(df)

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    with summary_col1:

        st.metric(
            "Matching Records",
            f"{result_count:,}"
        )

    with summary_col2:

        st.metric(
            "Dataset Records",
            f"{total_count:,}"
        )

    with summary_col3:

        if total_count > 0:

            percentage = (
                result_count / total_count
            ) * 100

            st.metric(
                "Match Rate",
                f"{percentage:.1f}%"
            )

        else:

            st.metric(
                "Match Rate",
                "0%"
            )

    # ========================================================
    # DISPLAY RESULTS
    # ========================================================

    if filtered_df.empty:

        st.warning(
            "No records match the current search and filters."
        )

        st.caption(
            "Try removing a filter or using a broader keyword."
        )

        return

    # --------------------------------------------------------
    # Keep first 100 results for performance
    # --------------------------------------------------------

    display_df = filtered_df.head(100).copy()

    # --------------------------------------------------------
    # Improve displayed column names
    # --------------------------------------------------------

    rename_map = {}

    for column in display_df.columns:

        clean_name = (
            str(column)
            .replace("_", " ")
            .strip()
        )

        rename_map[column] = clean_name

    display_df = display_df.rename(
        columns=rename_map
    )

    # --------------------------------------------------------
    # Display table
    # --------------------------------------------------------

    st.dataframe(
        display_df,
        use_container_width=True,
        height=430,
        hide_index=True
    )

    # ========================================================
    # RESULT FOOTER
    # ========================================================

    if result_count > 100:

        st.caption(
            f"Showing the first 100 of "
            f"{result_count:,} matching records."
        )

    else:

        st.caption(
            f"Showing all {result_count:,} matching records."
        )

    # ========================================================
    # QUICK RESULT INSIGHTS
    # ========================================================

    st.divider()

    st.subheader("💡 Quick Result Insights")

    insight_col1, insight_col2 = st.columns(2)

    # --------------------------------------------------------
    # District insight
    # --------------------------------------------------------

    with insight_col1:

        if district_col and not filtered_df.empty:

            district_counts = (
                filtered_df[district_col]
                .dropna()
                .astype(str)
                .value_counts()
            )

            if not district_counts.empty:

                top_district = district_counts.index[0]
                top_count = district_counts.iloc[0]

                st.info(
                    f"📍 **Most represented district:** "
                    f"{top_district} "
                    f"({top_count:,} records)"
                )

    # --------------------------------------------------------
    # Coffee type insight
    # --------------------------------------------------------

    with insight_col2:

        if coffee_col and not filtered_df.empty:

            coffee_counts = (
                filtered_df[coffee_col]
                .dropna()
                .astype(str)
                .value_counts()
            )

            if not coffee_counts.empty:

                top_coffee = coffee_counts.index[0]
                top_coffee_count = coffee_counts.iloc[0]

                st.info(
                    f"☕ **Most represented coffee type:** "
                    f"{top_coffee} "
                    f"({top_coffee_count:,} records)"
                )

    # ========================================================
    # NO ESTATE DETAILS SECTION
    # ========================================================
    #
    # IMPORTANT:
    # The old Smart Search page contained an "Estate Details"
    # section that attempted to identify an Estate_ID column.
    #
    # That section has intentionally been removed.
    #
    # The search page now ends after the search results and
    # quick insights.
    #
    # ========================================================

    st.divider()

    st.caption(
        "🔎 EstateInsight • Smart Search • "
        "Coffee Estate Intelligence Platform"
    )