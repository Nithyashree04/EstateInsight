# ============================================================
# ESTATE INSIGHT - AI RECOMMENDATIONS
# dashboard/ai.py
# ============================================================

import streamlit as st
import pandas as pd


# ============================================================
# HELPERS
# ============================================================

def find_column(df, aliases):
    """Find the first matching column from a list of aliases."""
    if df is None or df.empty:
        return None

    normalized = {
        str(col).strip().lower().replace(" ", "_").replace("-", "_"): col
        for col in df.columns
    }

    for alias in aliases:
        key = str(alias).strip().lower().replace(" ", "_").replace("-", "_")

        if key in normalized:
            return normalized[key]

    # Partial matching
    for alias in aliases:
        key = str(alias).strip().lower().replace(" ", "_").replace("-", "_")

        for normalized_name, original_name in normalized.items():
            if key in normalized_name or normalized_name in key:
                return original_name

    return None


def to_numeric(series):
    """Safely convert a pandas series to numeric."""
    return pd.to_numeric(series, errors="coerce")


def safe_mean(df, column):
    """Return mean of a numeric column."""
    if column is None or column not in df.columns:
        return None

    values = to_numeric(df[column]).dropna()

    if values.empty:
        return None

    return float(values.mean())


def clamp(value, minimum=0, maximum=100):
    """Keep a score between minimum and maximum."""
    return max(minimum, min(maximum, value))


def format_number(value, decimals=1):
    """Format numeric values safely."""
    if value is None:
        return "N/A"

    return f"{value:,.{decimals}f}"


# ============================================================
# MAIN PAGE
# ============================================================

def show_ai(df):

    # --------------------------------------------------------
    # PAGE VALIDATION
    # --------------------------------------------------------

    if df is None or df.empty:
        st.warning("⚠️ No estate data is available for AI analysis.")
        return

    # --------------------------------------------------------
    # COLUMN DETECTION
    # --------------------------------------------------------

    district_col = find_column(
        df,
        [
            "District",
            "district_name",
            "district"
        ]
    )

    yield_col = find_column(
        df,
        [
            "Yield_kg_ha",
            "Yield",
            "Yield_kg",
            "yield_kg_ha",
            "production_yield"
        ]
    )

    health_col = find_column(
        df,
        [
            "Estate_Health_Index",
            "Health_Index",
            "Health_Score",
            "Estate_Health_Score",
            "Health"
        ]
    )

    sustainability_col = find_column(
        df,
        [
            "Sustainability_Score",
            "Sustainability_Index",
            "Sustainability"
        ]
    )

    soil_moisture_col = find_column(
        df,
        [
            "Soil_Moisture_%",
            "Soil_Moisture",
            "Soil_Moisture_Percent",
            "Moisture"
        ]
    )

    soil_health_col = find_column(
        df,
        [
            "Soil_Health_Index",
            "Soil_Health_Score",
            "Soil_Health"
        ]
    )

    temperature_col = find_column(
        df,
        [
            "Temperature",
            "Temperature_C",
            "Temperature_Celsius",
            "Avg_Temperature"
        ]
    )

    rainfall_col = find_column(
        df,
        [
            "Rainfall",
            "Rainfall_mm",
            "Annual_Rainfall",
            "Rainfall_mm_year"
        ]
    )

    humidity_col = find_column(
        df,
        [
            "Humidity",
            "Humidity_%",
            "Humidity_Percent",
            "Relative_Humidity"
        ]
    )

    disease_col = find_column(
        df,
        [
            "Disease_Risk",
            "Disease_Risk_Score",
            "Disease",
            "Disease_Status",
            "Disease_Severity"
        ]
    )

    pest_col = find_column(
        df,
        [
            "Pest_Risk",
            "Pest_Risk_Score",
            "Pest_Status",
            "Pest_Severity"
        ]
    )

    carbon_col = find_column(
        df,
        [
            "Carbon_Footprint_tCO2e",
            "Carbon_Footprint",
            "Carbon_Emission",
            "Carbon_Emissions"
        ]
    )

    farm_size_col = find_column(
        df,
        [
            "Farm_Size_Acres",
            "Farm_Size",
            "Estate_Size_Acres",
            "Area_Acres"
        ]
    )

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.title("🤖 AI Recommendations")

    st.caption(
        "Data-driven recommendations to help improve estate health, "
        "productivity, sustainability and operational decisions."
    )

    st.divider()

    # --------------------------------------------------------
    # DISTRICT FILTER
    # --------------------------------------------------------

    working_df = df.copy()

    if district_col:

        districts = (
            working_df[district_col]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist()
        )

        districts = sorted([d for d in districts if d])

        selected_district = st.selectbox(
            "📍 Select Estate Region",
            ["All Districts"] + districts
        )

        if selected_district != "All Districts":
            working_df = working_df[
                working_df[district_col].astype(str).str.strip()
                == selected_district
            ].copy()

    else:
        selected_district = "All Districts"

    if working_df.empty:
        st.warning("⚠️ No records available for the selected region.")
        return

    # --------------------------------------------------------
    # CALCULATE METRICS
    # --------------------------------------------------------

    yield_avg = safe_mean(working_df, yield_col)
    health_avg = safe_mean(working_df, health_col)
    sustainability_avg = safe_mean(
        working_df,
        sustainability_col
    )

    moisture_avg = safe_mean(
        working_df,
        soil_moisture_col
    )

    soil_health_avg = safe_mean(
        working_df,
        soil_health_col
    )

    temperature_avg = safe_mean(
        working_df,
        temperature_col
    )

    rainfall_avg = safe_mean(
        working_df,
        rainfall_col
    )

    humidity_avg = safe_mean(
        working_df,
        humidity_col
    )

    disease_avg = safe_mean(
        working_df,
        disease_col
    )

    pest_avg = safe_mean(
        working_df,
        pest_col
    )

    carbon_avg = safe_mean(
        working_df,
        carbon_col
    )

    farm_size_avg = safe_mean(
        working_df,
        farm_size_col
    )

    # --------------------------------------------------------
    # NORMALIZE RISK VALUES
    # --------------------------------------------------------

    disease_risk = disease_avg if disease_avg is not None else 0
    pest_risk = pest_avg if pest_avg is not None else 0

    # --------------------------------------------------------
    # AI SCORE
    # --------------------------------------------------------

    score_components = []

    if health_avg is not None:
        score_components.append(("health", clamp(health_avg)))

    if sustainability_avg is not None:
        score_components.append(
            ("sustainability", clamp(sustainability_avg))
        )

    if soil_health_avg is not None:
        score_components.append(
            ("soil", clamp(soil_health_avg))
        )

    if yield_avg is not None:
        # Yield is normalized relative to a practical benchmark.
        yield_score = clamp((yield_avg / 2500) * 100)
        score_components.append(("yield", yield_score))

    if score_components:
        ai_score = sum(
            value for _, value in score_components
        ) / len(score_components)
    else:
        ai_score = 0

    ai_score = clamp(ai_score)

    # --------------------------------------------------------
    # PRIORITY ALERTS
    # --------------------------------------------------------

    alerts = []

    if moisture_avg is not None:

        if moisture_avg < 25:
            alerts.append(
                (
                    "HIGH",
                    "💧 Soil moisture is low",
                    "Review irrigation scheduling and soil moisture retention."
                )
            )

        elif moisture_avg < 35:
            alerts.append(
                (
                    "MEDIUM",
                    "💧 Soil moisture needs attention",
                    "Monitor moisture levels and avoid unnecessary water stress."
                )
            )

    if health_avg is not None and health_avg < 60:

        alerts.append(
            (
                "HIGH",
                "❤️ Estate health requires attention",
                "Inspect soil, crop condition, disease indicators and nutrient availability."
            )
        )

    elif health_avg is not None and health_avg < 75:

        alerts.append(
            (
                "MEDIUM",
                "❤️ Estate health is below optimal",
                "Increase monitoring of crop and soil conditions."
            )
        )

    if disease_avg is not None:

        if disease_avg >= 70:
            alerts.append(
                (
                    "HIGH",
                    "🦠 Elevated disease risk",
                    "Increase field scouting and inspect affected crop areas."
                )
            )

        elif disease_avg >= 40:
            alerts.append(
                (
                    "MEDIUM",
                    "🦠 Moderate disease risk",
                    "Continue regular disease monitoring."
                )
            )

    if pest_avg is not None:

        if pest_avg >= 70:
            alerts.append(
                (
                    "HIGH",
                    "🐛 Elevated pest risk",
                    "Prioritize crop scouting and early identification of affected areas."
                )
            )

        elif pest_avg >= 40:
            alerts.append(
                (
                    "MEDIUM",
                    "🐛 Moderate pest risk",
                    "Maintain regular pest surveillance."
                )
            )

    if sustainability_avg is not None:

        if sustainability_avg < 50:
            alerts.append(
                (
                    "HIGH",
                    "♻️ Sustainability score is low",
                    "Prioritize soil conservation, water efficiency and carbon reduction."
                )
            )

        elif sustainability_avg < 70:
            alerts.append(
                (
                    "MEDIUM",
                    "♻️ Sustainability can improve",
                    "Focus on resource efficiency and sustainable estate practices."
                )
            )

    if yield_avg is not None and yield_avg < 1200:

        alerts.append(
            (
                "HIGH",
                "☕ Yield is below target range",
                "Investigate soil health, crop condition, climate and estate management factors."
            )
        )

    elif yield_avg is not None and yield_avg < 1700:

        alerts.append(
            (
                "MEDIUM",
                "☕ Yield has improvement potential",
                "Review productivity trends and identify limiting factors."
            )
        )

    if temperature_avg is not None:

        if temperature_avg > 28:
            alerts.append(
                (
                    "MEDIUM",
                    "🌡️ Higher temperature conditions",
                    "Monitor moisture stress and maintain suitable shade and soil moisture."
                )
            )

    if rainfall_avg is not None:

        if rainfall_avg < 1000:
            alerts.append(
                (
                    "MEDIUM",
                    "🌧️ Rainfall is relatively low",
                    "Monitor water availability and soil moisture during dry periods."
                )
            )

    # --------------------------------------------------------
    # KPI DASHBOARD
    # --------------------------------------------------------

    st.subheader("🧠 AI Estate Overview")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "AI Estate Score",
            f"{ai_score:.0f}/100"
        )

    with col2:
        st.metric(
            "Priority Alerts",
            len(alerts)
        )

    with col3:
        st.metric(
            "Average Yield",
            f"{yield_avg:,.0f}" if yield_avg is not None else "N/A"
        )

    with col4:
        st.metric(
            "Sustainability",
            f"{sustainability_avg:.0f}/100"
            if sustainability_avg is not None
            else "N/A"
        )

    with col5:
        st.metric(
            "Disease / Pest Risk",
            f"{max(disease_risk, pest_risk):.0f}/100"
            if disease_col or pest_col
            else "N/A"
        )

    # --------------------------------------------------------
    # AI STATUS
    # --------------------------------------------------------

    st.markdown("### 🔎 AI Estate Diagnosis")

    if ai_score >= 80:

        status = "🟢 Excellent"
        diagnosis = (
            "The available indicators suggest that the estate is "
            "performing strongly. Maintain current practices while "
            "continuing regular monitoring."
        )

    elif ai_score >= 65:

        status = "🟡 Stable"
        diagnosis = (
            "The estate is generally stable, but several indicators "
            "show opportunities for improvement. Targeted action can "
            "help improve long-term performance."
        )

    elif ai_score >= 50:

        status = "🟠 Needs Attention"
        diagnosis = (
            "Several estate indicators require attention. "
            "Prioritize the highest-severity recommendations below."
        )

    else:

        status = "🔴 Critical Attention"
        diagnosis = (
            "The available indicators show multiple areas requiring "
            "immediate review. Start with the high-priority actions."
        )

    st.info(f"**{status}**\n\n{diagnosis}")

    # --------------------------------------------------------
    # PRIORITY ACTIONS
    # --------------------------------------------------------

    st.subheader("🚨 Priority Actions")

    if not alerts:

        st.success(
            "✅ No major priority alerts were detected from the available data."
        )

    else:

        severity_order = {
            "HIGH": 0,
            "MEDIUM": 1,
            "LOW": 2
        }

        alerts = sorted(
            alerts,
            key=lambda x: severity_order.get(x[0], 3)
        )

        for severity, title, recommendation in alerts:

            if severity == "HIGH":
                st.error(
                    f"🔴 **{severity} — {title}**\n\n"
                    f"{recommendation}"
                )

            elif severity == "MEDIUM":
                st.warning(
                    f"🟠 **{severity} — {title}**\n\n"
                    f"{recommendation}"
                )

            else:
                st.info(
                    f"🟢 **{severity} — {title}**\n\n"
                    f"{recommendation}"
                )

    # --------------------------------------------------------
    # RECOMMENDATION ENGINE
    # --------------------------------------------------------

    st.subheader("🌱 AI Recommendations")

    recommendation_cards = []

    # Soil recommendation
    if moisture_avg is not None:

        if moisture_avg < 25:
            recommendation_cards.append(
                (
                    "💧 Irrigation & Soil Moisture",
                    "High Priority",
                    "Soil moisture is below the preferred monitoring range.",
                    "Review irrigation timing, soil moisture retention and water availability."
                )
            )

        elif moisture_avg < 35:
            recommendation_cards.append(
                (
                    "💧 Irrigation & Soil Moisture",
                    "Monitor",
                    "Soil moisture is moderately low.",
                    "Continue monitoring and adjust irrigation according to field conditions."
                )
            )

        else:
            recommendation_cards.append(
                (
                    "💧 Irrigation & Soil Moisture",
                    "Healthy",
                    "Average soil moisture is currently stable.",
                    "Maintain monitoring to detect dry-period stress early."
                )
            )

    # Soil health recommendation
    if soil_health_avg is not None:

        if soil_health_avg < 50:
            recommendation_cards.append(
                (
                    "🌱 Soil Health",
                    "High Priority",
                    "The soil health indicator is relatively low.",
                    "Review soil condition, nutrient availability and organic matter management."
                )
            )

        elif soil_health_avg < 70:
            recommendation_cards.append(
                (
                    "🌱 Soil Health",
                    "Monitor",
                    "Soil health has room for improvement.",
                    "Track soil indicators regularly and prioritize long-term soil conservation."
                )
            )

        else:
            recommendation_cards.append(
                (
                    "🌱 Soil Health",
                    "Healthy",
                    "Soil health indicators are performing well.",
                    "Maintain current soil-management practices and continue periodic monitoring."
                )
            )

    # Climate recommendation
    climate_reason = []

    if temperature_avg is not None and temperature_avg > 28:
        climate_reason.append("higher average temperature")

    if rainfall_avg is not None and rainfall_avg < 1000:
        climate_reason.append("lower rainfall")

    if humidity_avg is not None and humidity_avg > 85:
        climate_reason.append("high humidity")

    if climate_reason:

        recommendation_cards.append(
            (
                "🌦️ Climate Management",
                "Monitor",
                "Climate indicators suggest " + ", ".join(climate_reason) + ".",
                "Monitor moisture stress, disease conditions and crop response closely."
            )
        )

    # Yield recommendation
    if yield_avg is not None:

        if yield_avg < 1200:

            recommendation_cards.append(
                (
                    "☕ Yield Improvement",
                    "High Priority",
                    "Average yield is relatively low.",
                    "Investigate soil health, crop condition, climate stress and estate-management factors."
                )
            )

        elif yield_avg < 1700:

            recommendation_cards.append(
                (
                    "☕ Yield Improvement",
                    "Monitor",
                    "Yield has improvement potential.",
                    "Compare productive and lower-performing areas to identify operational differences."
                )
            )

        else:

            recommendation_cards.append(
                (
                    "☕ Yield Improvement",
                    "Healthy",
                    "Yield performance is relatively strong.",
                    "Maintain current practices and monitor productivity trends."
                )
            )

    # Disease recommendation
    if disease_avg is not None:

        if disease_avg >= 70:

            recommendation_cards.append(
                (
                    "🦠 Disease Monitoring",
                    "High Priority",
                    "Disease-risk indicators are elevated.",
                    "Increase field scouting and investigate early symptoms in affected areas."
                )
            )

        elif disease_avg >= 40:

            recommendation_cards.append(
                (
                    "🦠 Disease Monitoring",
                    "Monitor",
                    "Moderate disease risk has been detected.",
                    "Maintain regular crop inspection and monitor changes over time."
                )
            )

        else:

            recommendation_cards.append(
                (
                    "🦠 Disease Monitoring",
                    "Healthy",
                    "Disease-risk indicators are currently relatively low.",
                    "Continue routine monitoring."
                )
            )

    # Pest recommendation
    if pest_avg is not None:

        if pest_avg >= 70:

            recommendation_cards.append(
                (
                    "🐛 Pest Monitoring",
                    "High Priority",
                    "Pest-risk indicators are elevated.",
                    "Increase field scouting and identify affected crop zones early."
                )
            )

        elif pest_avg >= 40:

            recommendation_cards.append(
                (
                    "🐛 Pest Monitoring",
                    "Monitor",
                    "Moderate pest risk has been detected.",
                    "Maintain regular surveillance and record changes in affected areas."
                )
            )

    # Sustainability recommendation
    if sustainability_avg is not None:

        if sustainability_avg < 50:

            recommendation_cards.append(
                (
                    "♻️ Sustainability",
                    "High Priority",
                    "The sustainability score is relatively low.",
                    "Focus on water efficiency, soil conservation and reducing unnecessary resource consumption."
                )
            )

        elif sustainability_avg < 70:

            recommendation_cards.append(
                (
                    "♻️ Sustainability",
                    "Improve",
                    "There is room to improve sustainability performance.",
                    "Prioritize efficient resource use and long-term soil and water conservation."
                )
            )

        else:

            recommendation_cards.append(
                (
                    "♻️ Sustainability",
                    "Strong",
                    "Sustainability performance is relatively strong.",
                    "Maintain current practices and continue tracking environmental indicators."
                )
            )

    # Carbon recommendation
    if carbon_avg is not None:

        if carbon_avg > 10:

            recommendation_cards.append(
                (
                    "🌍 Carbon Footprint",
                    "Improve",
                    "Average carbon footprint is relatively high.",
                    "Review resource-intensive operations and identify opportunities to improve efficiency."
                )
            )

        else:

            recommendation_cards.append(
                (
                    "🌍 Carbon Footprint",
                    "Positive",
                    "Carbon footprint indicators are relatively controlled.",
                    "Continue tracking emissions and resource efficiency."
                )
            )

    # --------------------------------------------------------
    # DISPLAY RECOMMENDATIONS
    # --------------------------------------------------------

    if recommendation_cards:

        for i in range(0, len(recommendation_cards), 2):

            cols = st.columns(2)

            for j, col in enumerate(cols):

                index = i + j

                if index >= len(recommendation_cards):
                    break

                title, priority, reason, action = recommendation_cards[index]

                with col:

                    with st.container(border=True):

                        st.markdown(f"### {title}")

                        if priority == "High Priority":
                            st.error(f"🔴 {priority}")

                        elif priority in ["Monitor", "Improve"]:
                            st.warning(f"🟠 {priority}")

                        else:
                            st.success(f"🟢 {priority}")

                        st.markdown(
                            f"**Why:** {reason}"
                        )

                        st.markdown(
                            f"**Recommended Action:** {action}"
                        )

    else:

        st.info(
            "ℹ️ Not enough indicators are available to generate detailed recommendations."
        )

    # --------------------------------------------------------
    # WHAT THE AI SEES
    # --------------------------------------------------------

    st.subheader("📊 What the AI Sees")

    insight_data = []

    if health_avg is not None:
        insight_data.append(
            ["Estate Health", f"{health_avg:.1f}/100"]
        )

    if sustainability_avg is not None:
        insight_data.append(
            ["Sustainability", f"{sustainability_avg:.1f}/100"]
        )

    if soil_health_avg is not None:
        insight_data.append(
            ["Soil Health", f"{soil_health_avg:.1f}/100"]
        )

    if moisture_avg is not None:
        insight_data.append(
            ["Soil Moisture", f"{moisture_avg:.1f}%"]
        )

    if temperature_avg is not None:
        insight_data.append(
            ["Temperature", f"{temperature_avg:.1f}"]
        )

    if rainfall_avg is not None:
        insight_data.append(
            ["Rainfall", f"{rainfall_avg:,.1f}"]
        )

    if humidity_avg is not None:
        insight_data.append(
            ["Humidity", f"{humidity_avg:.1f}%"]
        )

    if disease_avg is not None:
        insight_data.append(
            ["Disease Risk", f"{disease_avg:.1f}/100"]
        )

    if pest_avg is not None:
        insight_data.append(
            ["Pest Risk", f"{pest_avg:.1f}/100"]
        )

    if carbon_avg is not None:
        insight_data.append(
            ["Carbon Footprint", f"{carbon_avg:.2f}"]
        )

    if farm_size_avg is not None:
        insight_data.append(
            ["Average Farm Size", f"{farm_size_avg:.1f} acres"]
        )

    if insight_data:

        insight_df = pd.DataFrame(
            insight_data,
            columns=["Indicator", "Current Value"]
        )

        st.dataframe(
            insight_df,
            use_container_width=True,
            hide_index=True
        )

    # --------------------------------------------------------
    # ACTION PLAN
    # --------------------------------------------------------

    st.subheader("🎯 Recommended Action Plan")

    action_steps = []

    high_alerts = [
        alert for alert in alerts
        if alert[0] == "HIGH"
    ]

    if high_alerts:

        for _, title, recommendation in high_alerts[:3]:

            action_steps.append(
                recommendation
            )

    if not action_steps:

        action_steps.append(
            "Continue routine estate monitoring and maintain current management practices."
        )

    action_steps.append(
        "Track estate indicators regularly and compare performance across districts or estate zones."
    )

    action_steps.append(
        "Review yield, soil, climate, disease and sustainability trends together before making major operational decisions."
    )

    for number, step in enumerate(action_steps, start=1):

        st.markdown(
            f"**{number}.** {step}"
        )

    # --------------------------------------------------------
    # AI DISCLAIMER / TRANSPARENCY
    # --------------------------------------------------------

    st.divider()

    st.caption(
        "🤖 AI insight engine: recommendations are generated from "
        "the available estate indicators using transparent "
        "data-driven rules. They are intended as decision support "
        "and should be validated against field observations."
    )

    st.caption(
        f"📍 Analysis scope: {selected_district} • "
        f"Records analyzed: {len(working_df):,}"
    )