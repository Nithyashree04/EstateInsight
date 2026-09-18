# dashboard/disease.py

import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# ESTATEINSIGHT
# DISEASE & PEST ANALYTICS
# ============================================================


# ============================================================
# THEME
# ============================================================

TEXT_DARK = "#2B211B"
TEXT_MUTED = "#766A5F"
GRID_COLOR = "#E7DED5"

DISEASE_COLOR = "#C62828"
PEST_COLOR = "#EF6C00"

DISTRICT_COLORS = [
    "#2E7D32",
    "#1976D2",
    "#F9A825",
    "#8E24AA",
    "#00838F",
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def find_column(df, exact_name, alternatives=None):

    # Exact match first
    if exact_name in df.columns:
        return exact_name

    # Alternative names
    if alternatives:

        for column in alternatives:

            if column in df.columns:
                return column

    return None


def numeric(series):

    return pd.to_numeric(
        series,
        errors="coerce"
    )


def style_chart(fig, height=380):

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
            r=30,
            t=65,
            b=55
        ),

        hoverlabel=dict(
            bgcolor="white",
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
            color=TEXT_DARK,
            size=13
        )
    )

    fig.update_yaxes(

        gridcolor=GRID_COLOR,

        zeroline=False,

        tickfont=dict(
            color=TEXT_DARK
        ),

        title_font=dict(
            color=TEXT_DARK,
            size=13
        )
    )

    return fig


# ============================================================
# RISK CLASSIFICATION
# ============================================================

def risk_level(value):

    if pd.isna(value):
        return "Unknown"

    if value <= 3:
        return "Low"

    elif value <= 6:
        return "Moderate"

    else:
        return "High"


# ============================================================
# MAIN FUNCTION
# ============================================================

def show_disease(df):

    # ========================================================
    # HEADER
    # ========================================================

    st.title("🦠 Disease & Pest Analytics")

    st.caption(
        "Monitor disease and pest severity across the coffee "
        "estate to identify areas that need attention."
    )

    # ========================================================
    # DATA CHECK
    # ========================================================

    if df is None or df.empty:
        return

    # Remove duplicate columns
    df = df.loc[
        :,
        ~df.columns.duplicated()
    ].copy()

    # ========================================================
    # DATASET COLUMNS
    # ========================================================

    disease_col = find_column(
        df,
        "Disease_Severity_0_10",
        [
            "Disease Severity",
            "Disease_Severity",
            "Disease_Risk"
        ]
    )

    pest_col = find_column(
        df,
        "Pest_Severity_0_10",
        [
            "Pest Severity",
            "Pest_Severity",
            "Pest_Risk"
        ]
    )

    district_col = find_column(
        df,
        "District",
        [
            "District_Name",
            "Location"
        ]
    )

    estate_col = find_column(
        df,
        "Estate_ID",
        [
            "Estate ID",
            "Estate"
        ]
    )

    # ========================================================
    # CONVERT TO NUMERIC
    # ========================================================

    if disease_col:

        df[disease_col] = numeric(
            df[disease_col]
        )

    if pest_col:

        df[pest_col] = numeric(
            df[pest_col]
        )

    # ========================================================
    # CALCULATE AVERAGES
    # ========================================================

    if disease_col:

        average_disease = (
            df[disease_col]
            .mean()
        )

    else:

        average_disease = 0

    if pest_col:

        average_pest = (
            df[pest_col]
            .mean()
        )

    else:

        average_pest = 0

    # ========================================================
    # HIGH-RISK ESTATES
    # ========================================================

    if disease_col:

        high_disease_count = int(
            (
                df[disease_col] >= 7
            ).sum()
        )

    else:

        high_disease_count = 0

    if pest_col:

        high_pest_count = int(
            (
                df[pest_col] >= 7
            ).sum()
        )

    else:

        high_pest_count = 0

    # ========================================================
    # OVERALL RISK
    # ========================================================

    combined_average = (
        average_disease + average_pest
    ) / 2

    if combined_average <= 3:

        overall_risk = "Low"

    elif combined_average <= 6:

        overall_risk = "Moderate"

    else:

        overall_risk = "High"

    # ========================================================
    # KPI SECTION
    # ========================================================

    k1, k2, k3, k4 = st.columns(4)

    # --------------------------------------------------------
    # Disease
    # --------------------------------------------------------

    with k1:

        st.metric(
            "🦠 Avg Disease Severity",
            f"{average_disease:.1f} / 10"
        )

    # --------------------------------------------------------
    # Pest
    # --------------------------------------------------------

    with k2:

        st.metric(
            "🐛 Avg Pest Severity",
            f"{average_pest:.1f} / 10"
        )

    # --------------------------------------------------------
    # Disease High Risk
    # --------------------------------------------------------

    with k3:

        st.metric(
            "🚨 High Disease Risk",
            f"{high_disease_count:,}"
        )

    # --------------------------------------------------------
    # Pest High Risk
    # --------------------------------------------------------

    with k4:

        st.metric(
            "⚠️ High Pest Risk",
            f"{high_pest_count:,}"
        )

    # ========================================================
    # SIMPLE RISK STATUS
    # ========================================================

    if overall_risk == "Low":

        st.success(
            "🌿 **Overall Risk: Low** — "
            "Disease and pest pressure is generally low."
        )

    elif overall_risk == "Moderate":

        st.warning(
            "🟡 **Overall Risk: Moderate** — "
            "Regular monitoring is recommended."
        )

    else:

        st.error(
            "🔴 **Overall Risk: High** — "
            "High-risk areas should be prioritised for inspection."
        )

    # ========================================================
    # DISTRICT ANALYSIS
    # ========================================================

    st.divider()

    st.subheader(
        "📍 District Risk Overview"
    )

    st.caption(
        "Compare disease and pest severity across coffee-growing districts."
    )

    # ========================================================
    # DISEASE BY DISTRICT
    # ========================================================

    if district_col and disease_col:

        disease_district = (
            df.groupby(district_col)[
                disease_col
            ]
            .mean()
            .reset_index()
        )

        disease_district = (
            disease_district
            .dropna()
            .sort_values(
                disease_col,
                ascending=False
            )
        )

        if not disease_district.empty:

            fig_disease = px.bar(

                disease_district,

                x=district_col,

                y=disease_col,

                text=disease_col,

                color=district_col,

                color_discrete_sequence=(
                    DISTRICT_COLORS
                ),

                title=(
                    "🦠 Average Disease Severity by District"
                ),

                labels={
                    district_col: "District",
                    disease_col:
                        "Disease Severity (0–10)"
                }
            )

            fig_disease.update_traces(

                texttemplate="%{text:.1f}",

                textposition="outside",

                marker_line_width=0
            )

            fig_disease.update_layout(
                showlegend=False,
                yaxis=dict(
                    range=[
                        0,
                        max(
                            10,
                            disease_district[
                                disease_col
                            ].max() + 1
                        )
                    ]
                )
            )

            fig_disease = style_chart(
                fig_disease,
                height=390
            )

            st.plotly_chart(
                fig_disease,
                use_container_width=True
            )

    # ========================================================
    # PEST BY DISTRICT
    # ========================================================

    if district_col and pest_col:

        pest_district = (
            df.groupby(district_col)[
                pest_col
            ]
            .mean()
            .reset_index()
        )

        pest_district = (
            pest_district
            .dropna()
            .sort_values(
                pest_col,
                ascending=False
            )
        )

        if not pest_district.empty:

            fig_pest = px.bar(

                pest_district,

                x=district_col,

                y=pest_col,

                text=pest_col,

                color=district_col,

                color_discrete_sequence=(
                    DISTRICT_COLORS
                ),

                title=(
                    "🐛 Average Pest Severity by District"
                ),

                labels={
                    district_col: "District",
                    pest_col:
                        "Pest Severity (0–10)"
                }
            )

            fig_pest.update_traces(

                texttemplate="%{text:.1f}",

                textposition="outside",

                marker_line_width=0
            )

            fig_pest.update_layout(
                showlegend=False,
                yaxis=dict(
                    range=[
                        0,
                        max(
                            10,
                            pest_district[
                                pest_col
                            ].max() + 1
                        )
                    ]
                )
            )

            fig_pest = style_chart(
                fig_pest,
                height=390
            )

            st.plotly_chart(
                fig_pest,
                use_container_width=True
            )

    # ========================================================
    # RISK DISTRIBUTION
    # ========================================================

    st.divider()

    st.subheader(
        "📊 Risk Distribution"
    )

    st.caption(
        "See how many estate records fall into low, moderate and high risk."
    )

    # ========================================================
    # BUILD RISK DATA
    # ========================================================

    risk_rows = []

    if disease_col:

        disease_levels = (
            df[disease_col]
            .apply(risk_level)
            .value_counts()
            .reindex(
                ["Low", "Moderate", "High"],
                fill_value=0
            )
        )

        for level in [
            "Low",
            "Moderate",
            "High"
        ]:

            risk_rows.append(
                {
                    "Risk Level": level,
                    "Disease": int(
                        disease_levels[level]
                    )
                }
            )

    if pest_col:

        pest_levels = (
            df[pest_col]
            .apply(risk_level)
            .value_counts()
            .reindex(
                ["Low", "Moderate", "High"],
                fill_value=0
            )
        )

        for index, level in enumerate(
            [
                "Low",
                "Moderate",
                "High"
            ]
        ):

            if index < len(risk_rows):

                risk_rows[index]["Pest"] = int(
                    pest_levels[level]
                )

            else:

                risk_rows.append(
                    {
                        "Risk Level": level,
                        "Pest": int(
                            pest_levels[level]
                        )
                    }
                )

    if risk_rows:

        risk_df = pd.DataFrame(
            risk_rows
        )

        risk_long = risk_df.melt(
            id_vars="Risk Level",
            value_vars=[
                column
                for column in [
                    "Disease",
                    "Pest"
                ]
                if column in risk_df.columns
            ],
            var_name="Type",
            value_name="Estate Records"
        )

        fig_risk = px.bar(

            risk_long,

            x="Risk Level",

            y="Estate Records",

            color="Type",

            barmode="group",

            text="Estate Records",

            color_discrete_map={
                "Disease": DISEASE_COLOR,
                "Pest": PEST_COLOR
            },

            title=(
                "Disease & Pest Risk Distribution"
            ),

            labels={
                "Risk Level": "Risk Level",
                "Estate Records":
                    "Number of Records",
                "Type": "Risk Type"
            }
        )

        fig_risk.update_traces(

            textposition="outside",

            marker_line_width=0
        )

        fig_risk = style_chart(
            fig_risk,
            height=400
        )

        st.plotly_chart(
            fig_risk,
            use_container_width=True
        )

    # ========================================================
    # KEY INSIGHTS
    # ========================================================

    st.divider()

    st.subheader(
        "💡 Key Disease & Pest Insights"
    )

    insight_cols = st.columns(2)

    # ========================================================
    # DISEASE INSIGHT
    # ========================================================

    with insight_cols[0]:

        if average_disease <= 3:

            st.success(
                f"🦠 **Disease pressure is low**\n\n"
                f"The average disease severity is "
                f"**{average_disease:.1f}/10**."
            )

        elif average_disease <= 6:

            st.warning(
                f"🦠 **Disease pressure is moderate**\n\n"
                f"The average disease severity is "
                f"**{average_disease:.1f}/10**. "
                f"Regular crop inspection is recommended."
            )

        else:

            st.error(
                f"🦠 **Disease pressure is high**\n\n"
                f"The average disease severity is "
                f"**{average_disease:.1f}/10**. "
                f"High-risk estates should be prioritised."
            )

    # ========================================================
    # PEST INSIGHT
    # ========================================================

    with insight_cols[1]:

        if average_pest <= 3:

            st.success(
                f"🐛 **Pest pressure is low**\n\n"
                f"The average pest severity is "
                f"**{average_pest:.1f}/10**."
            )

        elif average_pest <= 6:

            st.warning(
                f"🐛 **Pest pressure is moderate**\n\n"
                f"The average pest severity is "
                f"**{average_pest:.1f}/10**. "
                f"Regular monitoring is recommended."
            )

        else:

            st.error(
                f"🐛 **Pest pressure is high**\n\n"
                f"The average pest severity is "
                f"**{average_pest:.1f}/10**. "
                f"High-risk estates should be inspected."
            )

    # ========================================================
    # HIGHEST RISK DISTRICT
    # ========================================================

    if district_col:

        district_summary = (
            df.groupby(district_col)
            .agg(
                Disease_Avg=(
                    disease_col,
                    "mean"
                ) if disease_col else (
                    district_col,
                    "size"
                ),
                Pest_Avg=(
                    pest_col,
                    "mean"
                ) if pest_col else (
                    district_col,
                    "size"
                )
            )
            .reset_index()
        )

        if (
            disease_col
            and pest_col
            and not district_summary.empty
        ):

            district_summary[
                "Overall_Risk"
            ] = (
                district_summary[
                    "Disease_Avg"
                ]
                +
                district_summary[
                    "Pest_Avg"
                ]
            ) / 2

            highest_risk = (
                district_summary
                .sort_values(
                    "Overall_Risk",
                    ascending=False
                )
                .iloc[0]
            )

            st.info(
                f"📍 **District requiring closest attention:** "
                f"**{highest_risk[district_col]}**\n\n"
                f"Combined average disease and pest severity: "
                f"**{highest_risk['Overall_Risk']:.1f}/10**."
            )

    # ========================================================
    # MANAGEMENT RECOMMENDATION
    # ========================================================

    with st.expander(
        "🌿 Recommended Management Approach"
    ):

        st.write(
            """
            **For low-risk areas**
            
            Continue routine field monitoring and maintain
            good estate hygiene.
            
            **For moderate-risk areas**
            
            Increase inspection frequency and monitor affected
            plants or sections more closely.
            
            **For high-risk areas**
            
            Prioritise field inspection, identify the source of
            the problem and take appropriate crop-management
            action based on the specific disease or pest.
            """
        )

    # ========================================================
    # DATA COVERAGE
    # ========================================================

    with st.expander(
        "🔎 Disease & Pest Data Coverage"
    ):

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Records",
                f"{len(df):,}"
            )

        with c2:

            st.metric(
                "Disease Data",
                (
                    "Available"
                    if disease_col
                    else "Unavailable"
                )
            )

        with c3:

            st.metric(
                "Pest Data",
                (
                    "Available"
                    if pest_col
                    else "Unavailable"
                )
            )

        with c4:

            if district_col:

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
        "EstateInsight • Disease & Pest Analytics ☕🌿"
    )