# ============================================================
# ESTATEINSIGHT - ESTATE HEALTH DASHBOARD
# dashboard/health.py
# FINAL NATIVE STREAMLIT VERSION
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def find_column(df, possible_names):
    """Find the first matching column in the dataframe."""
    for col in possible_names:
        if col in df.columns:
            return col
    return None


def safe_mean(df, column):
    """Safely calculate the mean of a numeric column."""

    if column is None or column not in df.columns:
        return None

    values = pd.to_numeric(
        df[column],
        errors="coerce"
    ).dropna()

    if values.empty:
        return None

    return values.mean()


def health_status(score):
    """Return health category."""

    if score >= 80:
        return "Excellent", "🟢"

    elif score >= 65:
        return "Good", "🟡"

    elif score >= 50:
        return "Moderate", "🟠"

    else:
        return "Critical", "🔴"


# ============================================================
# MAIN HEALTH DASHBOARD
# ============================================================

def show_health(df):

    # --------------------------------------------------------
    # DATA VALIDATION
    # --------------------------------------------------------

    if df is None or df.empty:

        st.warning(
            "No data available for Estate Health analysis."
        )

        return


    # --------------------------------------------------------
    # IDENTIFY COLUMNS
    # --------------------------------------------------------

    health_col = find_column(
        df,
        [
            "Estate_Health_Index",
            "Health_Index",
            "Health_Score",
            "Estate Health Index",
            "Estate_Health"
        ]
    )


    disease_col = find_column(
        df,
        [
            "Disease_Risk",
            "Disease_Risk_Score",
            "Pest_Risk",
            "Disease Risk",
            "Disease_Risk_Index"
        ]
    )


    soil_col = find_column(
        df,
        [
            "Soil_Health_Index",
            "Soil_Quality",
            "Soil_Health",
            "Soil Health Index",
            "Soil_Health_Score"
        ]
    )


    yield_col = find_column(
        df,
        [
            "Yield_kg",
            "Yield",
            "Coffee_Yield",
            "Production_kg",
            "Production"
        ]
    )


    district_col = find_column(
        df,
        [
            "District",
            "district",
            "Region",
            "Location"
        ]
    )


    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.title("❤️ Estate Health Dashboard")

    st.caption(
        "Monitor estate health, risk indicators and productivity "
        "to identify issues before they impact your coffee yield."
    )

    st.write("")


    # ========================================================
    # CALCULATE HEALTH METRICS
    # ========================================================

    avg_health = safe_mean(
        df,
        health_col
    )


    # Estimate health if direct health column doesn't exist

    if avg_health is None:

        factors = []


        if soil_col:

            soil_value = safe_mean(
                df,
                soil_col
            )

            if soil_value is not None:

                factors.append(
                    min(
                        max(soil_value, 0),
                        100
                    )
                )


        if disease_col:

            disease_value = safe_mean(
                df,
                disease_col
            )

            if disease_value is not None:

                disease_health = (
                    100 - disease_value
                )

                factors.append(
                    min(
                        max(disease_health, 0),
                        100
                    )
                )


        if factors:

            avg_health = (
                sum(factors)
                / len(factors)
            )

        else:

            avg_health = 75


    # Keep score between 0 and 100

    avg_health = min(
        max(avg_health, 0),
        100
    )


    # --------------------------------------------------------

    avg_disease = safe_mean(
        df,
        disease_col
    )

    if avg_disease is None:

        avg_disease = (
            100 - avg_health
        )


    avg_disease = min(
        max(avg_disease, 0),
        100
    )


    # --------------------------------------------------------

    avg_soil = safe_mean(
        df,
        soil_col
    )

    if avg_soil is None:

        avg_soil = 72


    avg_soil = min(
        max(avg_soil, 0),
        100
    )


    # --------------------------------------------------------

    avg_yield = safe_mean(
        df,
        yield_col
    )

    if avg_yield is None:

        avg_yield = 0


    # --------------------------------------------------------

    status_text, status_icon = health_status(
        avg_health
    )


    # ========================================================
    # OVERALL HEALTH SECTION
    # ========================================================

    left_col, right_col = st.columns(
        [1, 1.6]
    )


    # --------------------------------------------------------
    # HEALTH GAUGE
    # --------------------------------------------------------

    with left_col:

        health_container = st.container(
            border=True
        )

        with health_container:

            st.subheader(
                "Overall Estate Health"
            )


            fig_gauge = go.Figure(

                go.Indicator(

                    mode="gauge+number",

                    value=round(
                        avg_health,
                        1
                    ),

                    number={
                        "suffix": "%",
                        "font": {
                            "size": 42,
                            "color": "#2F241B"
                        }
                    },

                    title={
                        "text": f"{status_icon} {status_text}",
                        "font": {
                            "size": 18
                        }
                    },

                    gauge={

                        "axis": {
                            "range": [0, 100]
                        },

                        "bar": {
                            "color": "#5C7A57"
                        },

                        "bgcolor": "white",

                        "borderwidth": 0,

                        "steps": [

                            {
                                "range": [0, 50],
                                "color": "#F3E3E0"
                            },

                            {
                                "range": [50, 65],
                                "color": "#F7E9D2"
                            },

                            {
                                "range": [65, 80],
                                "color": "#E8F0E4"
                            },

                            {
                                "range": [80, 100],
                                "color": "#DDEBDF"
                            }

                        ]

                    }

                )

            )


            fig_gauge.update_layout(

                height=300,

                margin=dict(
                    l=20,
                    r=20,
                    t=40,
                    b=20
                ),

                paper_bgcolor="rgba(0,0,0,0)",

                font=dict(
                    color="#2F241B"
                )

            )


            st.plotly_chart(

                fig_gauge,

                use_container_width=True,

                config={
                    "displayModeBar": False
                }

            )


    # --------------------------------------------------------
    # HEALTH SUMMARY
    # --------------------------------------------------------

    with right_col:

        summary_container = st.container(
            border=True
        )

        with summary_container:

            st.subheader(
                "Health Summary"
            )

            st.caption(
                "Key indicators across the selected estates"
            )

            st.write("")


            row1_col1, row1_col2 = st.columns(2)


            with row1_col1:

                st.metric(

                    "Current Health Status",

                    f"{status_icon} {status_text}"

                )


            with row1_col2:

                st.metric(

                    "Average Disease Risk",

                    f"{avg_disease:.1f}%"

                )


            st.write("")


            row2_col1, row2_col2 = st.columns(2)


            with row2_col1:

                st.metric(

                    "Soil Health Score",

                    f"{avg_soil:.1f}/100"

                )


            with row2_col2:

                st.metric(

                    "Average Yield",

                    f"{avg_yield:,.0f} kg"

                )


    # ========================================================
    # HEALTH FACTOR ANALYSIS
    # ========================================================

    st.divider()

    st.subheader(
        "🌿 Health Factor Analysis"
    )

    st.caption(
        "Compare the major indicators influencing estate health."
    )


    factor_df = pd.DataFrame({

        "Factor": [

            "Estate Health",

            "Soil Health",

            "Disease Control"

        ],

        "Score": [

            avg_health,

            avg_soil,

            max(
                0,
                100 - avg_disease
            )

        ]

    })


    fig_factors = px.bar(

        factor_df,

        x="Score",

        y="Factor",

        orientation="h",

        text="Score",

        color="Score",

        color_continuous_scale=[
            "#E8D5C4",
            "#9B7B5A",
            "#5C7A57"
        ]

    )


    fig_factors.update_traces(

        texttemplate="%{text:.1f}",

        textposition="outside"

    )


    fig_factors.update_layout(

        height=360,

        showlegend=False,

        coloraxis_showscale=False,

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        xaxis=dict(

            range=[0, 110],

            title="Health Score"

        ),

        yaxis=dict(
            title=""
        ),

        margin=dict(
            l=20,
            r=40,
            t=20,
            b=20
        )

    )


    st.plotly_chart(

        fig_factors,

        use_container_width=True,

        config={
            "displayModeBar": False
        }

    )


    # ========================================================
    # DISTRICT COMPARISON
    # ========================================================

    if district_col and health_col:


        st.divider()

        st.subheader(
            "🗺️ District Health Comparison"
        )

        st.caption(
            "Compare average estate health across districts."
        )


        district_data = df.copy()

        district_data[health_col] = pd.to_numeric(

            district_data[health_col],

            errors="coerce"

        )


        district_data = district_data.dropna(

            subset=[
                health_col,
                district_col
            ]

        )


        if not district_data.empty:


            district_health = (

                district_data

                .groupby(
                    district_col
                )[health_col]

                .mean()

                .reset_index()

            )


            district_health.columns = [

                "District",

                "Average Health Score"

            ]


            district_health = (

                district_health

                .sort_values(

                    "Average Health Score",

                    ascending=False

                )

            )


            fig_district = px.bar(

                district_health,

                x="District",

                y="Average Health Score",

                text_auto=".1f",

                color="Average Health Score",

                color_continuous_scale=[
                    "#FFA33A",
                    "#8A6A4A",
                    "#5C7A57"
                ]

            )


            fig_district.update_layout(

                height=420,

                coloraxis_showscale=False,

                paper_bgcolor="rgba(0,0,0,0)",

                plot_bgcolor="rgba(0,0,0,0)",

                xaxis_title="District",

                yaxis_title="Health Score"

            )


            st.plotly_chart(

                fig_district,

                use_container_width=True,

                config={
                    "displayModeBar": False
                }

            )


    # ========================================================
    # HEALTH DISTRIBUTION
    # ========================================================

    if health_col:


        health_data = pd.to_numeric(

            df[health_col],

            errors="coerce"

        ).dropna()


        if not health_data.empty:


            st.divider()

            st.subheader(
                "📊 Estate Health Distribution"
            )

            st.caption(
                "Distribution of health scores across available estate records."
            )


            fig_distribution = px.histogram(

                x=health_data,

                nbins=20,

                labels={

                    "x": "Health Score",

                    "y": "Number of Estates"

                }

            )


            fig_distribution.update_traces(

                marker_color="#5C7A57"

            )


            fig_distribution.update_layout(

                height=380,

                paper_bgcolor="rgba(0,0,0,0)",

                plot_bgcolor="rgba(0,0,0,0)",

                bargap=0.08

            )


            st.plotly_chart(

                fig_distribution,

                use_container_width=True,

                config={
                    "displayModeBar": False
                }

            )


    # ========================================================
    # SMART RECOMMENDATIONS
    # ========================================================

    st.divider()

    st.subheader(
        "🤖 Smart Health Recommendations"
    )

    st.caption(
        "AI-inspired recommendations based on current estate indicators."
    )


    recommendations = []


    # --------------------------------------------------------

    if avg_health < 60:

        recommendations.append(

            (

                "🔴 Immediate Attention Required",

                "Overall estate health is below the recommended range. "
                "Inspect affected plots and prioritize corrective actions."

            )

        )


    elif avg_health < 75:

        recommendations.append(

            (

                "🟡 Increase Monitoring",

                "Estate health is moderate. Increase field inspections "
                "and closely monitor changes in soil and crop conditions."

            )

        )


    else:

        recommendations.append(

            (

                "🟢 Maintain Current Practices",

                "Estate health is performing well. Continue regular "
                "monitoring and preventive management practices."

            )

        )


    # --------------------------------------------------------

    if avg_disease > 40:

        recommendations.append(

            (

                "🦠 Monitor Disease-Prone Areas",

                "Disease risk is elevated. Conduct early-stage crop "
                "inspection and monitor vulnerable areas closely."

            )

        )


    # --------------------------------------------------------

    if avg_soil < 65:

        recommendations.append(

            (

                "🌱 Improve Soil Conditions",

                "Soil health indicators are below the optimal range. "
                "Review nutrient management and soil improvement practices."

            )

        )


    # --------------------------------------------------------

    if avg_yield > 0 and avg_health < 70:

        recommendations.append(

            (

                "📉 Protect Future Productivity",

                "Current health indicators could affect future yield. "
                "Prioritize preventive interventions."

            )

        )


    # --------------------------------------------------------
    # DISPLAY RECOMMENDATIONS
    # --------------------------------------------------------

    for title, recommendation in recommendations:

        with st.expander(
            title,
            expanded=False
        ):

            st.write(
                recommendation
            )


    # ========================================================
    # FOOTER NOTE
    # ========================================================

    st.divider()

    st.caption(
        "ℹ️ Estate Health scores are calculated from available "
        "soil, disease, productivity and environmental indicators."
    )