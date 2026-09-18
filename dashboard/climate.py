# ============================================================
# ESTATEINSIGHT | CLIMATE ANALYTICS
# FILE: dashboard/climate.py
# FINAL VERSION
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

TEXT_DARK = "#2F241B"
TEXT_MUTED = "#75695D"
GRID_COLOR = "#DED3C8"

MONTHS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def find_column(df, possible_columns):
    """
    Find the first matching column.
    Supports exact and case-insensitive matching.
    """

    if df is None or df.empty:
        return None

    # Exact match
    for column in possible_columns:
        if column in df.columns:
            return column

    # Case-insensitive match
    lookup = {
        str(column).strip().lower(): column
        for column in df.columns
    }

    for column in possible_columns:
        key = str(column).strip().lower()

        if key in lookup:
            return lookup[key]

    return None


def numeric_values(df, column):
    """
    Safely convert a dataframe column to numeric.
    """

    if column is None or column not in df.columns:
        return pd.Series(dtype="float64")

    return pd.to_numeric(
        df[column],
        errors="coerce"
    ).dropna()


def safe_mean(df, column):
    """
    Safely calculate mean.
    """

    values = numeric_values(df, column)

    if values.empty:
        return None

    return float(values.mean())


def format_value(value, decimals=1, suffix=""):
    """
    Format numeric values safely.
    """

    if value is None or pd.isna(value):
        return "—"

    return f"{value:,.{decimals}f}{suffix}"


def create_monthly_climate_data(df):
    """
    Convert monthly temperature and rainfall columns
    into a clean 12-month dataframe.

    Example:
        Temp_Jan_C
        Rain_Jan_mm

    becomes:

        Month | Temperature | Rainfall
    """

    rows = []

    for month in MONTHS:

        temp_col = find_column(
            df,
            [
                f"Temp_{month}_C",
                f"Temperature_{month}_C",
                f"Temperature_{month}",
            ]
        )

        rain_col = find_column(
            df,
            [
                f"Rain_{month}_mm",
                f"Rainfall_{month}_mm",
                f"Rainfall_{month}",
            ]
        )

        temp_value = safe_mean(df, temp_col)
        rain_value = safe_mean(df, rain_col)

        rows.append(
            {
                "Month": month,
                "Temperature": temp_value,
                "Rainfall": rain_value,
            }
        )

    monthly_df = pd.DataFrame(rows)

    monthly_df["Temperature"] = pd.to_numeric(
        monthly_df["Temperature"],
        errors="coerce"
    )

    monthly_df["Rainfall"] = pd.to_numeric(
        monthly_df["Rainfall"],
        errors="coerce"
    )

    return monthly_df


def chart_layout(fig, height=430):
    """
    Apply consistent professional Plotly styling.
    """

    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(255,255,255,0)",
        plot_bgcolor="rgba(255,255,255,0)",
        font=dict(
            family="DM Sans, Arial, sans-serif",
            color=TEXT_DARK,
            size=13
        ),
        title_font=dict(
            family="DM Sans, Arial, sans-serif",
            color=TEXT_DARK,
            size=18
        ),
        margin=dict(
            l=55,
            r=35,
            t=65,
            b=55
        ),
        legend=dict(
            bgcolor="rgba(255,255,255,0.75)",
            bordercolor=GRID_COLOR,
            borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="DM Sans, Arial, sans-serif"
        ),
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor=GRID_COLOR,
        zeroline=False,
        title_font=dict(
            color=TEXT_DARK,
            size=13
        ),
        tickfont=dict(
            color=TEXT_DARK
        )
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID_COLOR,
        zeroline=False,
        title_font=dict(
            color=TEXT_DARK,
            size=13
        ),
        tickfont=dict(
            color=TEXT_DARK
        )
    )

    return fig


# ============================================================
# MAIN CLIMATE DASHBOARD
# ============================================================

def show_climate(df):

    # --------------------------------------------------------
    # DATA VALIDATION
    # --------------------------------------------------------

    if df is None or df.empty:

        st.warning(
            "No climate records are available for the selected filters."
        )

        return

    # Work on a clean copy
    data = df.copy()

    data.columns = (
        data.columns
        .astype(str)
        .str.strip()
    )

    # Remove duplicate column names
    data = data.loc[
        :,
        ~data.columns.duplicated()
    ]

    # --------------------------------------------------------
    # MONTHLY CLIMATE DATA
    # --------------------------------------------------------

    monthly_df = create_monthly_climate_data(data)

    valid_temperature = monthly_df[
        monthly_df["Temperature"].notna()
    ]

    valid_rainfall = monthly_df[
        monthly_df["Rainfall"].notna()
    ]

    # Overall averages
    average_temperature = (
        valid_temperature["Temperature"].mean()
        if not valid_temperature.empty
        else None
    )

    average_rainfall = (
        valid_rainfall["Rainfall"].mean()
        if not valid_rainfall.empty
        else None
    )

    total_rainfall = (
        valid_rainfall["Rainfall"].sum()
        if not valid_rainfall.empty
        else None
    )

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    st.title("🌦️ Climate Analytics")

    st.caption(
        "Monitor temperature and rainfall patterns "
        "across the coffee estate to understand "
        "environmental growing conditions."
    )

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:

        st.metric(
            "🌡️ Average Temperature",
            format_value(
                average_temperature,
                1,
                " °C"
            )
        )

    with kpi2:

        st.metric(
            "🌧️ Average Monthly Rainfall",
            format_value(
                average_rainfall,
                1,
                " mm"
            )
        )

    with kpi3:

        st.metric(
            "💧 Annual Rainfall",
            format_value(
                total_rainfall,
                0,
                " mm"
            )
        )

    with kpi4:

        # ----------------------------------------------------
        # SIMPLE CLIMATE STATUS
        # ----------------------------------------------------

        if average_temperature is None:

            climate_status = "No Data"

        elif 18 <= average_temperature <= 28:

            climate_status = "Favourable"

        elif 15 <= average_temperature <= 30:

            climate_status = "Moderate"

        else:

            climate_status = "Needs Attention"

        st.metric(
            "🌱 Climate Status",
            climate_status
        )

    st.divider()

    # ========================================================
    # TEMPERATURE & RAINFALL SCATTER PLOT
    # ========================================================

    st.subheader("🌡️ Temperature vs Rainfall")

    st.caption(
        "The scatter plot shows how monthly rainfall "
        "varies with average temperature."
    )

    scatter_df = monthly_df.dropna(
        subset=[
            "Temperature",
            "Rainfall"
        ]
    ).copy()

    if not scatter_df.empty:

        fig_scatter = px.scatter(
            scatter_df,
            x="Rainfall",
            y="Temperature",
            text="Month",
            size="Rainfall",
            color="Temperature",
            color_continuous_scale=[
                "#2E7D32",
                "#F9A825",
                "#E65100"
            ],
            hover_name="Month",
            hover_data={
                "Rainfall": ":.1f",
                "Temperature": ":.1f"
            },
            labels={
                "Rainfall": "Average Rainfall (mm)",
                "Temperature": "Average Temperature (°C)",
                "color": "Temperature (°C)"
            }
        )

        fig_scatter.update_traces(
            marker=dict(
                opacity=0.85,
                line=dict(
                    width=1,
                    color="white"
                )
            ),
            textposition="top center",
            textfont=dict(
                size=11,
                color=TEXT_DARK
            )
        )

        fig_scatter.update_layout(
            coloraxis_colorbar=dict(
                title="Temperature °C"
            )
        )

        fig_scatter = chart_layout(
            fig_scatter,
            height=450
        )

        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )

    else:

        st.info(
            "Monthly temperature and rainfall records "
            "could not be calculated from the selected data."
        )

    # ========================================================
    # MONTHLY TEMPERATURE TREND
    # ========================================================

    st.subheader("🌡️ Monthly Temperature Trend")

    st.caption(
        "Average temperature recorded for each month "
        "across the selected estate records."
    )

    temperature_df = monthly_df.dropna(
        subset=["Temperature"]
    ).copy()

    if not temperature_df.empty:

        fig_temp = px.line(
            temperature_df,
            x="Month",
            y="Temperature",
            markers=True,
            labels={
                "Month": "Month",
                "Temperature": "Average Temperature (°C)"
            }
        )

        fig_temp.update_traces(
            line=dict(
                width=4
            ),
            marker=dict(
                size=9,
                line=dict(
                    width=1,
                    color="white"
                )
            ),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Temperature: %{y:.1f} °C"
                "<extra></extra>"
            )
        )

        fig_temp = chart_layout(
            fig_temp,
            height=400
        )

        st.plotly_chart(
            fig_temp,
            use_container_width=True
        )

    else:

        st.info(
            "Temperature data is not available for the "
            "selected records."
        )

    # ========================================================
    # CLIMATE SUMMARY
    # ========================================================

    st.subheader("📋 Climate Summary")

    if (
        average_temperature is not None
        and average_rainfall is not None
    ):

        # Warmest month
        warmest_row = (
            monthly_df
            .dropna(subset=["Temperature"])
            .sort_values(
                "Temperature",
                ascending=False
            )
            .iloc[0]
        )

        # Coolest month
        coolest_row = (
            monthly_df
            .dropna(subset=["Temperature"])
            .sort_values(
                "Temperature",
                ascending=True
            )
            .iloc[0]
        )

        # Wettest month
        wettest_row = (
            monthly_df
            .dropna(subset=["Rainfall"])
            .sort_values(
                "Rainfall",
                ascending=False
            )
            .iloc[0]
        )

        summary1, summary2, summary3 = st.columns(3)

        with summary1:

            st.info(
                f"🔥 **Warmest Month**\n\n"
                f"{warmest_row['Month']} — "
                f"{warmest_row['Temperature']:.1f} °C"
            )

        with summary2:

            st.info(
                f"❄️ **Coolest Month**\n\n"
                f"{coolest_row['Month']} — "
                f"{coolest_row['Temperature']:.1f} °C"
            )

        with summary3:

            st.info(
                f"🌧️ **Wettest Month**\n\n"
                f"{wettest_row['Month']} — "
                f"{wettest_row['Rainfall']:.1f} mm"
            )

    # ========================================================
    # CLIMATE INSIGHTS
    # ========================================================

    st.subheader("🤖 Smart Climate Insights")

    if average_temperature is not None:

        if 18 <= average_temperature <= 28:

            temperature_message = (
                "🌱 Temperature conditions are generally "
                "favourable for coffee cultivation."
            )

        elif average_temperature < 18:

            temperature_message = (
                "❄️ Average temperature is relatively low. "
                "Monitor cooler growing conditions."
            )

        else:

            temperature_message = (
                "☀️ Average temperature is relatively high. "
                "Monitor heat stress during warmer months."
            )

        st.write(temperature_message)

    if average_rainfall is not None:

        if average_rainfall >= 150:

            rainfall_message = (
                "🌧️ Rainfall levels are relatively high. "
                "Good water availability should be balanced "
                "with drainage management."
            )

        elif average_rainfall >= 80:

            rainfall_message = (
                "💧 Rainfall availability is moderate and "
                "should support normal moisture conditions."
            )

        else:

            rainfall_message = (
                "🌦️ Rainfall is relatively low. "
                "Soil moisture should be monitored carefully."
            )

        st.write(rainfall_message)

    # ========================================================
    # DATA COVERAGE
    # ========================================================

    with st.expander("📊 Climate Data Coverage"):

        coverage_df = pd.DataFrame(
            {
                "Month": MONTHS,
                "Temperature Available": [
                    (
                        "Yes"
                        if not pd.isna(
                            monthly_df.loc[
                                monthly_df["Month"] == month,
                                "Temperature"
                            ].iloc[0]
                        )
                        else "No"
                    )
                    for month in MONTHS
                ],
                "Rainfall Available": [
                    (
                        "Yes"
                        if not pd.isna(
                            monthly_df.loc[
                                monthly_df["Month"] == month,
                                "Rainfall"
                            ].iloc[0]
                        )
                        else "No"
                    )
                    for month in MONTHS
                ]
            }
        )

        st.dataframe(
            coverage_df,
            use_container_width=True,
            hide_index=True
        )

    # ========================================================
    # FOOTER
    # ========================================================

    st.divider()

    st.caption(
        "🌦️ Climate Analytics • "
        "EstateInsight Coffee Estate Intelligence Platform ☕"
    )