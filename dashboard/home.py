# ============================================================
# COFFEE ESTATE ANALYTICS DASHBOARD
# FILE: dashboard/home.py
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_mean(df, column, default=0):
    """Safely calculate mean of a numeric column."""
    if column in df.columns:
        value = pd.to_numeric(df[column], errors="coerce").mean()

        if pd.notna(value):
            return value

    return default


def safe_sum(df, column, default=0):
    """Safely calculate sum of a numeric column."""
    if column in df.columns:
        value = pd.to_numeric(df[column], errors="coerce").sum()

        if pd.notna(value):
            return value

    return default


def count_category(df, column, keywords):
    """Count rows containing one or more keywords."""

    if column not in df.columns:
        return 0

    series = df[column].astype(str).str.lower()

    mask = pd.Series(
        False,
        index=df.index
    )

    for keyword in keywords:

        mask = mask | series.str.contains(
            keyword.lower(),
            na=False
        )

    return int(mask.sum())


# ============================================================
# NAVIGATION
# ============================================================

def go_to_page(page):
    """Navigate to another dashboard page."""

    st.session_state.page = page
    st.rerun()


# ============================================================
# FEATURE CARD
# ============================================================

def feature_card(
    column,
    icon,
    title,
    description,
    page
):

    with column:

        st.markdown(
            f"""
<div class="feature-card">

<div class="feature-icon">
{icon}
</div>

<div class="feature-title">
{title}
</div>

<div class="feature-description">
{description}
</div>

</div>
""",
            unsafe_allow_html=True
        )

        if st.button(
            "Explore →",
            key=f"explore_{page}",
            use_container_width=True
        ):

            go_to_page(page)


# ============================================================
# MAIN DASHBOARD
# ============================================================

def show_home(df):

    # ========================================================
    # DATA VALIDATION
    # ========================================================

    if df is None or df.empty:

        st.warning(
            "No estate data available."
        )

        return


    # ========================================================
    # CUSTOM CSS
    # ========================================================

    st.markdown(
        """
<style>

/* =========================================================
   MAIN APPLICATION
========================================================= */

.stApp {
    background-color: #F6F3EE;
}


/* =========================================================
   PAGE CONTAINER
========================================================= */

.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}


/* =========================================================
   HIDE STREAMLIT DEFAULT ELEMENTS
========================================================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* =========================================================
   HEADINGS
========================================================= */

.main-heading {
    font-size: 42px;
    font-weight: 800;
    color: #2F241B;
    font-family: Georgia, serif;
    margin-bottom: 5px;
}

.sub-heading {
    font-size: 17px;
    color: #776C61;
    margin-bottom: 25px;
}

.section-heading {
    font-size: 25px;
    font-weight: 700;
    color: #30251D;
    margin-top: 30px;
    margin-bottom: 15px;
    font-family: Georgia, serif;
}


/* =========================================================
   METRIC CARDS
========================================================= */

[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #E7DED2;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0px 5px 18px rgba(60, 45, 30, 0.07);
}

[data-testid="stMetricLabel"] {
    font-size: 15px;
    color: #75695D;
}

[data-testid="stMetricValue"] {
    font-size: 30px;
    color: #2E261F;
}


/* =========================================================
   FEATURE CARDS
========================================================= */

.feature-card {
    background-color: white;
    border: 1px solid #E7DED2;
    border-radius: 18px;
    padding: 22px;
    min-height: 175px;
    box-shadow: 0px 5px 18px rgba(60, 45, 30, 0.07);
    margin-bottom: 8px;
}

.feature-icon {
    font-size: 34px;
    margin-bottom: 10px;
}

.feature-title {
    font-size: 18px;
    font-weight: 700;
    color: #342A22;
    margin-bottom: 8px;
}

.feature-description {
    font-size: 13px;
    color: #756A60;
    line-height: 1.5;
}


/* =========================================================
   EXPLORE BUTTON
========================================================= */

.stButton > button {
    background-color: #8A5A2B;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    min-height: 40px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    background-color: #6F451F;
    color: white;
    border: none;
}


/* =========================================================
   CONTENT CARDS
========================================================= */

.content-card {
    background-color: white;
    border: 1px solid #E7DED2;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0px 5px 18px rgba(60, 45, 30, 0.07);
}


/* =========================================================
   DIVIDERS
========================================================= */

hr {
    border: none;
    border-top: 1px solid #E8DED4;
    margin-top: 25px;
    margin-bottom: 25px;
}

</style>
""",
        unsafe_allow_html=True
    )


    # ========================================================
    # KPI VALUES
    # ========================================================

    total_estates = len(df)

    average_yield = safe_mean(
        df,
        "Yield_kg_ha"
    )

    estate_health = safe_mean(
        df,
        "Estate_Health_Score"
    )

    sustainability_score = safe_mean(
        df,
        "Sustainability_Score"
    )

    total_area = safe_sum(
        df,
        "Farm_Size_Acres"
    )

    average_price = safe_mean(
        df,
        "Market_Price_INR_kg"
    )

    healthy_count = count_category(
        df,
        "Health_Category",
        [
            "healthy",
            "excellent",
            "good"
        ]
    )

    high_risk_count = count_category(
        df,
        "Risk_Category",
        [
            "high",
            "critical"
        ]
    )

    low_health_count = count_category(
        df,
        "Health_Category",
        [
            "poor",
            "critical",
            "low"
        ]
    )


    # ========================================================
    # HERO SECTION
    # ========================================================

    st.markdown(
        """
<div style="
background: linear-gradient(
    135deg,
    #FFFFFF,
    #EFE2D0
);

padding: 38px;

border-radius: 22px;

border: 1px solid #E4D6C5;

box-shadow:
0px 8px 25px rgba(60,45,30,0.08);

margin-bottom: 25px;
">

<div style="
font-size: 42px;
font-weight: 800;
color: #2F241B;
font-family: Georgia, serif;
">

☕ Welcome back, Estate Manager!

</div>

<div style="
font-size: 17px;
color: #756A60;
margin-top: 8px;
">

Here's what's happening across your coffee estates today.

</div>

</div>
""",
        unsafe_allow_html=True
    )


    # ========================================================
    # KPI SECTION
    #
    # IMPORTANT:
    # TOTAL REVENUE CARD HAS BEEN COMPLETELY REMOVED.
    # ========================================================

    col1, col2, col3 = st.columns(3)


    # --------------------------------------------------------
    # TOTAL ESTATES
    # --------------------------------------------------------

    with col1:

        st.metric(
            label="🌿 Total Estates",
            value=f"{total_estates:,}",
            help="Total estate records in the dataset"
        )


    # --------------------------------------------------------
    # AVERAGE YIELD
    # --------------------------------------------------------

    with col2:

        st.metric(
            label="📈 Average Yield",
            value=f"{average_yield:,.0f} kg/ha",
            help="Average coffee yield in kilograms per hectare"
        )


    # --------------------------------------------------------
    # ESTATE HEALTH
    # --------------------------------------------------------

    with col3:

        st.metric(
            label="💚 Estate Health",
            value=f"{estate_health:.1f}%",
            help="Average estate health score"
        )


    # ========================================================
    # ESTATE INTELLIGENCE
    # ========================================================

    st.markdown(
        '<div class="section-heading">'
        'Estate Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Access the tools you need to monitor, analyse "
        "and improve your coffee estate."
    )


    # ========================================================
    # FIRST FEATURE ROW
    # ========================================================

    features = [

        (
            "🤖",
            "AI Yield Forecast",
            "Predict coffee yield and identify future "
            "harvest patterns using machine learning.",
            "🤖 AI Intelligence"
        ),

        (
            "🌦️",
            "Climate Analytics",
            "Monitor rainfall and temperature patterns "
            "affecting coffee production.",
            "🌦️ Climate Analytics"
        ),

        (
            "🛡️",
            "Health Monitoring",
            "Analyze estate health and identify "
            "potential plantation risks.",
            "❤️ Estate Health"
        ),

        (
            "📊",
            "Quality Analytics",
            "Evaluate bean quality and export readiness "
            "across estates.",
            "☕ Coffee Quality"
        ),

        (
            "🌱",
            "Soil Intelligence",
            "Track nutrients and soil moisture for "
            "better plantation management.",
            "🌱 Soil & Nutrient"
        )

    ]


    feature_columns = st.columns(5)


    for column, feature in zip(
        feature_columns,
        features
    ):

        icon, title, description, page = feature

        feature_card(
            column,
            icon,
            title,
            description,
            page
        )


    # ========================================================
    # SECOND FEATURE ROW
    # ========================================================

    features2 = [

        (
            "📍",
            "District Analysis",
            "Compare coffee estates across districts "
            "and identify regional performance.",
            "🗺️ District Analytics"
        ),

        (
            "♻️",
            "Sustainability",
            "Analyze environmental impact and carbon "
            "footprint across estates.",
            "♻️ Sustainability"
        ),

        (
            "🔎",
            "Smart Search",
            "Search estates based on district, yield, "
            "quality and performance.",
            "🔎 Smart Search"
        ),

        (
            "📄",
            "Smart Reports",
            "Generate downloadable reports with "
            "important estate insights.",
            "📄 Reports & Export"
        )

    ]


    feature_columns2 = st.columns(4)


    for column, feature in zip(
        feature_columns2,
        features2
    ):

        icon, title, description, page = feature

        feature_card(
            column,
            icon,
            title,
            description,
            page
        )


    # ========================================================
    # ESTATE OVERVIEW
    # ========================================================

    st.markdown(
        '<div class="section-heading">'
        'Estate Overview'
        '</div>',
        unsafe_allow_html=True
    )


    chart_col, activity_col, alert_col = st.columns(
        [1.6, 1, 1]
    )


    # ========================================================
    # PRODUCTION CHART
    # ========================================================

    with chart_col:

        st.markdown(
            '<div class="content-card">',
            unsafe_allow_html=True
        )

        st.subheader(
            "🌿 Production Overview"
        )

        st.caption(
            "Average coffee yield across districts"
        )


        if (
            "District" in df.columns
            and
            "Yield_kg_ha" in df.columns
        ):

            chart_data = (
                df.groupby("District")[
                    "Yield_kg_ha"
                ]
                .mean()
                .reset_index()
                .sort_values(
                    "Yield_kg_ha",
                    ascending=False
                )
            )


            fig = px.bar(
                chart_data,
                x="District",
                y="Yield_kg_ha",
                text_auto=".0f"
            )


            fig.update_traces(
                marker_color="#8A5A2B",
                textposition="outside"
            )


            fig.update_layout(
                height=330,

                paper_bgcolor="rgba(0,0,0,0)",

                plot_bgcolor="rgba(0,0,0,0)",

                margin=dict(
                    l=10,
                    r=10,
                    t=20,
                    b=10
                ),

                xaxis_title="",

                yaxis_title="Yield (kg/ha)",

                showlegend=False
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )


        else:

            st.info(
                "Yield or District column not available."
            )


    # ========================================================
    # RECENT ACTIVITIES
    # ========================================================

    with activity_col:

        st.markdown(
            """
<div class="content-card">

<h3>⚡ Recent Activities</h3>

<p style="color:#756A60;">
Latest analytics updates
</p>

<hr>

<p>
🌱 <b>Estate health updated</b>
</p>

<p style="
color:#8A8178;
font-size:13px;
">

Health analytics completed

</p>

<hr>

<p>
🌦️ <b>Climate analysis ready</b>
</p>

<p style="
color:#8A8178;
font-size:13px;
">

Rainfall trends processed

</p>

<hr>

<p>
🤖 <b>AI recommendations generated</b>
</p>

<p style="
color:#8A8178;
font-size:13px;
">

Estate insights updated

</p>

</div>
""",
            unsafe_allow_html=True
        )


    # ========================================================
    # TASKS & ALERTS
    # ========================================================

    with alert_col:

        st.markdown(
            """
<div class="content-card">

<h3>🔔 Tasks & Alerts</h3>

<p style="color:#756A60;">

Important estate indicators

</p>

</div>
""",
            unsafe_allow_html=True
        )


        st.metric(
            "⚠️ High Risk Estates",
            f"{high_risk_count:,}"
        )


        st.metric(
            "💚 Healthy Estates",
            f"{healthy_count:,}"
        )


        st.metric(
            "🛡️ Health Alerts",
            f"{low_health_count:,}"
        )


    # ========================================================
    # QUICK ESTATE INSIGHTS
    # ========================================================

    st.markdown(
        '<div class="section-heading">'
        'Quick Estate Insights'
        '</div>',
        unsafe_allow_html=True
    )


    insight_col1, insight_col2, insight_col3 = st.columns(3)


    # --------------------------------------------------------
    # TOTAL AREA
    # --------------------------------------------------------

    with insight_col1:

        st.markdown(
            """
<div class="content-card">

<h3>🌿 Total Estate Area</h3>

</div>
""",
            unsafe_allow_html=True
        )


        st.metric(
            "Total Acres",
            f"{total_area:,.0f}"
        )


    # --------------------------------------------------------
    # MARKET PRICE
    # --------------------------------------------------------

    with insight_col2:

        st.markdown(
            """
<div class="content-card">

<h3>☕ Market Intelligence</h3>

</div>
""",
            unsafe_allow_html=True
        )


        st.metric(
            "Average Market Price",
            f"₹{average_price:,.0f}"
        )


    # --------------------------------------------------------
    # DISTRICT COVERAGE
    # --------------------------------------------------------

    with insight_col3:

        district_count = (

            df["District"].nunique()

            if "District" in df.columns

            else 0

        )


        st.markdown(
            """
<div class="content-card">

<h3>📍 Coverage</h3>

</div>
""",
            unsafe_allow_html=True
        )


        st.metric(
            "Districts Covered",
            f"{district_count}"
        )


    # ========================================================
    # FOOTER
    # ========================================================

    st.divider()

    st.caption(
        "☕ Coffee Estate Analytics Platform | "
        "AI Powered Estate Intelligence 🌿"
    )