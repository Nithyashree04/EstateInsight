# ============================================================
# ESTATEINSIGHT - REPORTS & EXPORT MODULE
# dashboard/reports.py
# ============================================================

import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

# ------------------------------------------------------------
# OPTIONAL REPORTLAB IMPORT
# ------------------------------------------------------------

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
        PageBreak,
    )

    REPORTLAB_AVAILABLE = True

except ImportError:
    REPORTLAB_AVAILABLE = False


# ============================================================
# DATAFRAME SAFETY HELPERS
# ============================================================

def remove_duplicate_columns(df):
    """
    Removes duplicate dataframe column names.

    Streamlit / PyArrow does not accept duplicate column names.
    The first occurrence of each column is retained.
    """
    if df is None:
        return df

    result = df.copy()

    if result.columns.duplicated().any():
        result = result.loc[
            :, ~result.columns.duplicated()
        ].copy()

    return result


def unique_columns(columns):
    """
    Returns a list of unique, valid column names while
    preserving their original order.
    """
    result = []
    seen = set()

    for column in columns:
        if column is None:
            continue

        if column not in seen:
            seen.add(column)
            result.append(column)

    return result


def safe_dataframe(df):
    """
    Final safety layer before sending a dataframe to Streamlit.
    """
    if df is None:
        return pd.DataFrame()

    result = df.copy()

    # Remove duplicate column names
    result = result.loc[
        :, ~result.columns.duplicated()
    ].copy()

    # Make absolutely sure columns are unique
    if result.columns.duplicated().any():
        result = result.loc[
            :, ~result.columns.duplicated()
        ].copy()

    return result


# ============================================================
# COLUMN DETECTION
# ============================================================

def normalize_column_name(name):
    """
    Normalizes column names for flexible matching.
    """
    return (
        str(name)
        .strip()
        .lower()
        .replace(" ", "")
        .replace("_", "")
        .replace("-", "")
        .replace(".", "")
        .replace("/", "")
        .replace("(", "")
        .replace(")", "")
        .replace("%", "percent")
    )


def find_column(df, possible_columns):
    """
    Finds the first matching dataframe column using:
    1. Exact match
    2. Normalized match
    3. Partial match
    """

    if df is None or df.empty:
        return None

    # Make sure duplicate source columns don't break lookup
    df = remove_duplicate_columns(df)

    actual_columns = list(df.columns)

    # --------------------------------------------------------
    # Exact match
    # --------------------------------------------------------

    for candidate in possible_columns:
        if candidate in actual_columns:
            return candidate

    # --------------------------------------------------------
    # Normalized match
    # --------------------------------------------------------

    normalized_actual = {}

    for column in actual_columns:
        normalized_actual[
            normalize_column_name(column)
        ] = column

    for candidate in possible_columns:
        normalized_candidate = normalize_column_name(candidate)

        if normalized_candidate in normalized_actual:
            return normalized_actual[
                normalized_candidate
            ]

    # --------------------------------------------------------
    # Partial match
    # --------------------------------------------------------

    for candidate in possible_columns:
        normalized_candidate = normalize_column_name(candidate)

        for column in actual_columns:
            normalized_column = normalize_column_name(column)

            if (
                normalized_candidate in normalized_column
                or normalized_column in normalized_candidate
            ):
                return column

    return None


# ============================================================
# NUMERIC HELPERS
# ============================================================

def to_numeric(series):
    """
    Safely converts a pandas Series to numeric.
    """
    if series is None:
        return pd.Series(dtype=float)

    try:
        return pd.to_numeric(
            series,
            errors="coerce"
        )
    except Exception:
        return pd.Series(dtype=float)


def safe_mean(df, column):
    """
    Returns the mean of a column.
    """
    if column is None or column not in df.columns:
        return None

    values = to_numeric(df[column]).dropna()

    if values.empty:
        return None

    return float(values.mean())


def safe_sum(df, column):
    """
    Returns the sum of a column.
    """
    if column is None or column not in df.columns:
        return None

    values = to_numeric(df[column]).dropna()

    if values.empty:
        return None

    return float(values.sum())


def safe_max(df, column):
    """
    Returns the maximum of a column.
    """
    if column is None or column not in df.columns:
        return None

    values = to_numeric(df[column]).dropna()

    if values.empty:
        return None

    return float(values.max())


def safe_min(df, column):
    """
    Returns the minimum of a column.
    """
    if column is None or column not in df.columns:
        return None

    values = to_numeric(df[column]).dropna()

    if values.empty:
        return None

    return float(values.min())


# ============================================================
# COLUMN DETECTION MAP
# ============================================================

def detect_columns(df):

    df = remove_duplicate_columns(df)

    columns = {}

    columns["estate"] = find_column(
        df,
        [
            "Estate_ID",
            "Estate ID",
            "Estate",
            "Estate_Name",
            "Farm_ID",
            "Farm ID",
        ],
    )

    columns["district"] = find_column(
        df,
        [
            "District",
            "District_Name",
            "District Name",
            "Region",
        ],
    )

    columns["coffee_type"] = find_column(
        df,
        [
            "Coffee_Type",
            "Coffee Type",
            "Coffee",
            "Variety",
            "Coffee_Variety",
        ],
    )

    columns["processing"] = find_column(
        df,
        [
            "Processing_Method",
            "Processing Method",
            "Processing",
        ],
    )

    columns["yield"] = find_column(
        df,
        [
            "Yield_kg_ha",
            "Yield (kg/ha)",
            "Yield",
            "Yield_kg_per_ha",
            "Yield kg ha",
        ],
    )

    columns["revenue"] = find_column(
        df,
        [
            "Revenue",
            "Revenue_INR",
            "Revenue (INR)",
            "Annual_Revenue",
            "Total_Revenue",
        ],
    )

    columns["profit"] = find_column(
        df,
        [
            "Profit",
            "Profit_INR",
            "Profit (INR)",
            "Net_Profit",
            "Annual_Profit",
        ],
    )

    columns["farm_size"] = find_column(
        df,
        [
            "Farm_Size_Acres",
            "Farm Size Acres",
            "Farm_Size",
            "Farm Area",
            "Area_Acres",
        ],
    )

    columns["health"] = find_column(
        df,
        [
            "Estate_Health_Score",
            "Estate Health Score",
            "Health_Score",
            "Health Score",
            "Estate_Health",
        ],
    )

    columns["soil_health"] = find_column(
        df,
        [
            "Soil_Health_Score",
            "Soil Health Score",
            "Soil_Health",
        ],
    )

    columns["soil_ph"] = find_column(
        df,
        [
            "Soil_pH",
            "Soil pH",
            "pH",
            "SoilPH",
        ],
    )

    columns["soil_moisture"] = find_column(
        df,
        [
            "Soil_Moisture_%",
            "Soil Moisture %",
            "Soil_Moisture",
            "Soil Moisture",
        ],
    )

    columns["temperature"] = find_column(
        df,
        [
            "Temperature",
            "Temperature_C",
            "Temperature (°C)",
            "Avg_Temperature",
        ],
    )

    columns["rainfall"] = find_column(
        df,
        [
            "Rainfall",
            "Rainfall_mm",
            "Rainfall (mm)",
            "Annual_Rainfall",
        ],
    )

    columns["humidity"] = find_column(
        df,
        [
            "Humidity",
            "Humidity_%",
            "Humidity %",
            "Relative_Humidity",
        ],
    )

    columns["disease"] = find_column(
        df,
        [
            "Disease",
            "Disease_Risk",
            "Disease_Risk_Level",
            "Disease Risk",
        ],
    )

    columns["pest"] = find_column(
        df,
        [
            "Pest",
            "Pest_Risk",
            "Pest_Risk_Level",
            "Pest Risk",
        ],
    )

    columns["sustainability"] = find_column(
        df,
        [
            "Sustainability_Score",
            "Sustainability Score",
            "Sustainability",
        ],
    )

    columns["carbon"] = find_column(
        df,
        [
            "Carbon_Footprint_tCO2e",
            "Carbon Footprint tCO2e",
            "Carbon_Footprint",
            "Carbon Footprint",
        ],
    )

    return columns


# ============================================================
# FORMATTING HELPERS
# ============================================================

def format_number(value, decimals=1):

    if value is None:
        return "N/A"

    try:
        return f"{value:,.{decimals}f}"
    except Exception:
        return "N/A"


def format_currency(value):

    if value is None:
        return "N/A"

    try:
        return f"₹{value:,.0f}"
    except Exception:
        return "N/A"


def format_percent(value):

    if value is None:
        return "N/A"

    try:
        return f"{value:.1f}%"
    except Exception:
        return "N/A"


# ============================================================
# PDF FOOTER
# ============================================================

def add_pdf_footer(canvas, doc):

    canvas.saveState()

    width, height = A4

    canvas.setFont(
        "Helvetica",
        8
    )

    canvas.setFillColor(
        colors.HexColor("#666666")
    )

    canvas.drawString(
        0.6 * inch,
        0.35 * inch,
        "EstateInsight • Coffee Estate Analytics"
    )

    canvas.drawRightString(
        width - 0.6 * inch,
        0.35 * inch,
        f"Page {doc.page}"
    )

    canvas.restoreState()


# ============================================================
# PDF TABLE HELPER
# ============================================================

def create_pdf_table(
    data,
    column_widths=None,
    header_background="#4E342E",
):

    table = Table(
        data,
        colWidths=column_widths,
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        header_background
                    ),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "LEFT",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#D0D0D0"),
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#F7F3EF"),
                    ],
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
            ]
        )
    )

    return table


# ============================================================
# PDF REPORT GENERATOR
# ============================================================

def generate_pdf_report(
    df,
    report_scope="Complete Portfolio",
):

    if not REPORTLAB_AVAILABLE:
        return None

    # --------------------------------------------------------
    # SANITIZE DATAFRAME
    # --------------------------------------------------------

    df = remove_duplicate_columns(df)

    if df is None or df.empty:
        return None

    columns = detect_columns(df)

    # --------------------------------------------------------
    # PDF BUFFER
    # --------------------------------------------------------

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#3E2723"),
        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#6D4C41"),
        spaceAfter=18,
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#4E342E"),
        spaceBefore=12,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#333333"),
        spaceAfter=7,
    )

    small_style = ParagraphStyle(
        "Small",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#555555"),
    )

    story = []

    # ========================================================
    # TITLE
    # ========================================================

    story.append(
        Paragraph(
            "EstateInsight",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "Coffee Estate Analytics Report",
            subtitle_style,
        )
    )

    story.append(
        Paragraph(
            f"<b>Report Scope:</b> {report_scope}<br/>"
            f"<b>Generated:</b> "
            f"{datetime.now().strftime('%d %B %Y, %I:%M %p')}<br/>"
            f"<b>Records:</b> {len(df):,}",
            body_style,
        )
    )

    # ========================================================
    # EXECUTIVE SUMMARY
    # ========================================================

    story.append(
        Paragraph(
            "Executive Summary",
            heading_style,
        )
    )

    summary_parts = []

    if columns["estate"]:
        estate_count = df[
            columns["estate"]
        ].nunique()

        summary_parts.append(
            f"The portfolio contains "
            f"<b>{estate_count:,}</b> estates."
        )

    if columns["district"]:
        district_count = df[
            columns["district"]
        ].nunique()

        summary_parts.append(
            f"The dataset covers "
            f"<b>{district_count}</b> districts."
        )

    if columns["yield"]:
        avg_yield = safe_mean(
            df,
            columns["yield"],
        )

        if avg_yield is not None:
            summary_parts.append(
                f"Average yield is "
                f"<b>{format_number(avg_yield)} kg/ha</b>."
            )

    if columns["health"]:
        avg_health = safe_mean(
            df,
            columns["health"],
        )

        if avg_health is not None:
            summary_parts.append(
                f"Average estate health score is "
                f"<b>{format_number(avg_health)}</b>."
            )

    if columns["sustainability"]:
        avg_sustainability = safe_mean(
            df,
            columns["sustainability"],
        )

        if avg_sustainability is not None:
            summary_parts.append(
                f"Average sustainability score is "
                f"<b>{format_number(avg_sustainability)}</b>."
            )

    if summary_parts:
        story.append(
            Paragraph(
                " ".join(summary_parts),
                body_style,
            )
        )
    else:
        story.append(
            Paragraph(
                "Portfolio summary metrics could not be "
                "calculated from the available fields.",
                body_style,
            )
        )

    # ========================================================
    # PORTFOLIO OVERVIEW
    # ========================================================

    story.append(
        Paragraph(
            "Portfolio Overview",
            heading_style,
        )
    )

    overview_data = [
        ["Metric", "Value"]
    ]

    overview_data.append(
        [
            "Total records",
            f"{len(df):,}",
        ]
    )

    if columns["estate"]:
        overview_data.append(
            [
                "Unique estates",
                f"{df[columns['estate']].nunique():,}",
            ]
        )

    if columns["district"]:
        overview_data.append(
            [
                "Districts",
                f"{df[columns['district']].nunique():,}",
            ]
        )

    if columns["coffee_type"]:
        overview_data.append(
            [
                "Coffee types",
                f"{df[columns['coffee_type']].nunique():,}",
            ]
        )

    if columns["processing"]:
        overview_data.append(
            [
                "Processing methods",
                f"{df[columns['processing']].nunique():,}",
            ]
        )

    story.append(
        create_pdf_table(
            overview_data,
            column_widths=[
                3.1 * inch,
                2.8 * inch,
            ],
        )
    )

    # ========================================================
    # PERFORMANCE METRICS
    # ========================================================

    story.append(
        Paragraph(
            "Performance & Financial Metrics",
            heading_style,
        )
    )

    performance_data = [
        ["Metric", "Average", "Maximum", "Minimum"]
    ]

    metric_columns = [
        (
            "Yield (kg/ha)",
            columns["yield"],
        ),
        (
            "Estate Health Score",
            columns["health"],
        ),
        (
            "Sustainability Score",
            columns["sustainability"],
        ),
        (
            "Soil Health Score",
            columns["soil_health"],
        ),
    ]

    for label, column in metric_columns:

        if column is None:
            continue

        performance_data.append(
            [
                label,
                format_number(
                    safe_mean(df, column)
                ),
                format_number(
                    safe_max(df, column)
                ),
                format_number(
                    safe_min(df, column)
                ),
            ]
        )

    if len(performance_data) > 1:

        story.append(
            create_pdf_table(
                performance_data,
                column_widths=[
                    2.3 * inch,
                    1.4 * inch,
                    1.4 * inch,
                    1.4 * inch,
                ],
            )
        )

    financial_data = [
        ["Financial Metric", "Total", "Average"]
    ]

    if columns["revenue"]:

        financial_data.append(
            [
                "Revenue",
                format_currency(
                    safe_sum(
                        df,
                        columns["revenue"],
                    )
                ),
                format_currency(
                    safe_mean(
                        df,
                        columns["revenue"],
                    )
                ),
            ]
        )

    if columns["profit"]:

        financial_data.append(
            [
                "Profit",
                format_currency(
                    safe_sum(
                        df,
                        columns["profit"],
                    )
                ),
                format_currency(
                    safe_mean(
                        df,
                        columns["profit"],
                    )
                ),
            ]
        )

    if len(financial_data) > 1:

        story.append(Spacer(1, 8))

        story.append(
            create_pdf_table(
                financial_data,
                column_widths=[
                    2.3 * inch,
                    2.1 * inch,
                    2.1 * inch,
                ],
            )
        )

    # ========================================================
    # CLIMATE & ENVIRONMENT
    # ========================================================

    climate_available = any(
        [
            columns["temperature"],
            columns["rainfall"],
            columns["humidity"],
            columns["soil_ph"],
            columns["soil_moisture"],
            columns["carbon"],
        ]
    )

    if climate_available:

        story.append(
            Paragraph(
                "Climate & Environmental Indicators",
                heading_style,
            )
        )

        climate_data = [
            ["Indicator", "Average", "Maximum", "Minimum"]
        ]

        climate_metrics = [
            (
                "Temperature",
                columns["temperature"],
            ),
            (
                "Rainfall",
                columns["rainfall"],
            ),
            (
                "Humidity",
                columns["humidity"],
            ),
            (
                "Soil pH",
                columns["soil_ph"],
            ),
            (
                "Soil Moisture",
                columns["soil_moisture"],
            ),
            (
                "Carbon Footprint",
                columns["carbon"],
            ),
        ]

        for label, column in climate_metrics:

            if column is None:
                continue

            climate_data.append(
                [
                    label,
                    format_number(
                        safe_mean(df, column)
                    ),
                    format_number(
                        safe_max(df, column)
                    ),
                    format_number(
                        safe_min(df, column)
                    ),
                ]
            )

        story.append(
            create_pdf_table(
                climate_data,
                column_widths=[
                    2.3 * inch,
                    1.4 * inch,
                    1.4 * inch,
                    1.4 * inch,
                ],
            )
        )

    # ========================================================
    # DISEASE & PEST
    # ========================================================

    disease_available = (
        columns["disease"] is not None
        or columns["pest"] is not None
    )

    if disease_available:

        story.append(
            Paragraph(
                "Disease & Pest Risk",
                heading_style,
            )
        )

        risk_data = [
            ["Risk Indicator", "Category", "Count"]
        ]

        if columns["disease"]:

            disease_counts = (
                df[columns["disease"]]
                .dropna()
                .astype(str)
                .value_counts()
                .head(5)
            )

            for category, count in disease_counts.items():

                risk_data.append(
                    [
                        "Disease",
                        str(category),
                        f"{count:,}",
                    ]
                )

        if columns["pest"]:

            pest_counts = (
                df[columns["pest"]]
                .dropna()
                .astype(str)
                .value_counts()
                .head(5)
            )

            for category, count in pest_counts.items():

                risk_data.append(
                    [
                        "Pest",
                        str(category),
                        f"{count:,}",
                    ]
                )

        if len(risk_data) > 1:

            story.append(
                create_pdf_table(
                    risk_data,
                    column_widths=[
                        1.7 * inch,
                        2.8 * inch,
                        1.2 * inch,
                    ],
                )
            )

    # ========================================================
    # DISTRICT SUMMARY
    # ========================================================

    if columns["district"]:

        story.append(
            Paragraph(
                "District Performance Summary",
                heading_style,
            )
        )

        group_columns = unique_columns(
            [
                columns["district"],
                columns["yield"],
                columns["health"],
                columns["sustainability"],
            ]
        )

        if columns["district"]:

            district_df = df.copy()

            district_column = columns["district"]

            aggregation = {}

            if columns["yield"]:
                aggregation[
                    columns["yield"]
                ] = "mean"

            if columns["health"]:
                aggregation[
                    columns["health"]
                ] = "mean"

            if columns["sustainability"]:
                aggregation[
                    columns["sustainability"]
                ] = "mean"

            if aggregation:

                district_summary = (
                    district_df
                    .groupby(
                        district_column,
                        dropna=False,
                    )
                    .agg(aggregation)
                    .reset_index()
                )

                district_summary = safe_dataframe(
                    district_summary
                )

                district_summary = (
                    district_summary
                    .sort_values(
                        by=(
                            columns["yield"]
                            if columns["yield"]
                            in district_summary.columns
                            else district_column
                        ),
                        ascending=False,
                    )
                    .head(10)
                )

                district_data = [
                    [
                        "District",
                        "Avg Yield",
                        "Avg Health",
                        "Avg Sustainability",
                    ]
                ]

                for _, row in district_summary.iterrows():

                    district_name = str(
                        row[district_column]
                    )

                    yield_value = (
                        row[columns["yield"]]
                        if columns["yield"]
                        and columns["yield"]
                        in row.index
                        else None
                    )

                    health_value = (
                        row[columns["health"]]
                        if columns["health"]
                        and columns["health"]
                        in row.index
                        else None
                    )

                    sustainability_value = (
                        row[columns["sustainability"]]
                        if columns["sustainability"]
                        and columns["sustainability"]
                        in row.index
                        else None
                    )

                    district_data.append(
                        [
                            district_name,
                            format_number(
                                yield_value
                            ),
                            format_number(
                                health_value
                            ),
                            format_number(
                                sustainability_value
                            ),
                        ]
                    )

                story.append(
                    create_pdf_table(
                        district_data,
                        column_widths=[
                            1.8 * inch,
                            1.5 * inch,
                            1.5 * inch,
                            1.7 * inch,
                        ],
                    )
                )

    # ========================================================
    # TOP ESTATES
    # ========================================================

    if (
        columns["estate"]
        and columns["yield"]
    ):

        story.append(
            Paragraph(
                "Top Performing Estates",
                heading_style,
            )
        )

        ranking_columns = unique_columns(
            [
                columns["estate"],
                columns["district"],
                columns["yield"],
                columns["health"],
                columns["sustainability"],
            ]
        )

        top_df = df[
            ranking_columns
        ].copy()

        top_df["__yield_sort__"] = to_numeric(
            top_df[columns["yield"]]
        )

        top_df = (
            top_df
            .sort_values(
                "__yield_sort__",
                ascending=False,
            )
            .head(10)
        )

        top_data = [
            [
                "Estate",
                "District",
                "Yield",
                "Health",
                "Sustainability",
            ]
        ]

        for _, row in top_df.iterrows():

            estate_name = (
                str(row[columns["estate"]])
                if columns["estate"]
                else "N/A"
            )

            district_name = (
                str(row[columns["district"]])
                if columns["district"]
                else "N/A"
            )

            yield_value = (
                row[columns["yield"]]
                if columns["yield"]
                else None
            )

            health_value = (
                row[columns["health"]]
                if columns["health"]
                else None
            )

            sustainability_value = (
                row[columns["sustainability"]]
                if columns["sustainability"]
                else None
            )

            top_data.append(
                [
                    estate_name,
                    district_name,
                    format_number(
                        yield_value
                    ),
                    format_number(
                        health_value
                    ),
                    format_number(
                        sustainability_value
                    ),
                ]
            )

        story.append(
            create_pdf_table(
                top_data,
                column_widths=[
                    1.4 * inch,
                    1.4 * inch,
                    1.2 * inch,
                    1.2 * inch,
                    1.5 * inch,
                ],
            )
        )

    # ========================================================
    # MANAGEMENT INSIGHTS
    # ========================================================

    story.append(
        Paragraph(
            "Management Insights",
            heading_style,
        )
    )

    insights = []

    if columns["yield"]:

        avg_yield = safe_mean(
            df,
            columns["yield"],
        )

        max_yield = safe_max(
            df,
            columns["yield"],
        )

        if (
            avg_yield is not None
            and max_yield is not None
        ):
            insights.append(
                f"Portfolio average yield is "
                f"{format_number(avg_yield)} kg/ha, "
                f"while the highest observed yield is "
                f"{format_number(max_yield)} kg/ha."
            )

    if columns["health"]:

        avg_health = safe_mean(
            df,
            columns["health"],
        )

        if avg_health is not None:

            if avg_health >= 80:
                status = "strong"
            elif avg_health >= 60:
                status = "moderate"
            else:
                status = "an area requiring attention"

            insights.append(
                f"The overall estate health score averages "
                f"{format_number(avg_health)}, indicating "
                f"{status} portfolio health."
            )

    if columns["sustainability"]:

        avg_sustainability = safe_mean(
            df,
            columns["sustainability"],
        )

        if avg_sustainability is not None:

            insights.append(
                f"Average sustainability performance is "
                f"{format_number(avg_sustainability)}, "
                f"which can be used as a baseline for "
                f"future sustainability initiatives."
            )

    if columns["carbon"]:

        total_carbon = safe_sum(
            df,
            columns["carbon"],
        )

        if total_carbon is not None:

            insights.append(
                f"Recorded portfolio carbon footprint totals "
                f"{format_number(total_carbon)} tCO₂e."
            )

    if not insights:

        insights.append(
            "Additional management insights require "
            "more compatible analytical fields in the dataset."
        )

    for insight in insights:

        story.append(
            Paragraph(
                f"• {insight}",
                body_style,
            )
        )

    # ========================================================
    # METHODOLOGY
    # ========================================================

    story.append(
        Paragraph(
            "Methodology & Notes",
            heading_style,
        )
    )

    methodology = (
        "This report is generated from the currently filtered "
        "EstateInsight dataset. Numeric performance indicators "
        "are summarized using descriptive statistics such as "
        "mean, minimum and maximum values. District and estate "
        "rankings are based on the available yield field. "
        "Missing or incompatible values are excluded from "
        "numeric calculations."
    )

    story.append(
        Paragraph(
            methodology,
            body_style,
        )
    )

    story.append(
        Paragraph(
            "Report generated automatically by EstateInsight "
            "Coffee Estate Analytics.",
            small_style,
        )
    )

    # ========================================================
    # BUILD PDF
    # ========================================================

    try:

        document.build(
            story,
            onFirstPage=add_pdf_footer,
            onLaterPages=add_pdf_footer,
        )

        buffer.seek(0)

        return buffer.getvalue()

    except Exception:
        return None


# ============================================================
# REPORTS PAGE
# ============================================================

def show_reports(df):

    # --------------------------------------------------------
    # PAGE SAFETY
    # --------------------------------------------------------

    if df is None:

        st.error(
            "No dataset is available for report generation."
        )

        return

    # --------------------------------------------------------
    # REMOVE DUPLICATE COLUMNS IMMEDIATELY
    # --------------------------------------------------------

    working_df = remove_duplicate_columns(
        df.copy()
    )

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if working_df.empty:

        st.warning(
            "The current filtered dataset is empty."
        )

        return

    # --------------------------------------------------------
    # DETECT COLUMNS
    # --------------------------------------------------------

    columns = detect_columns(
        working_df
    )

    # ========================================================
    # HEADER
    # ========================================================

    st.title(
        "📑 Reports & Export"
    )

    st.caption(
        "Generate executive reports, export filtered data, "
        "and review portfolio performance."
    )

    st.divider()

    # ========================================================
    # REPORT SCOPE
    # ========================================================

    st.subheader(
        "Report Configuration"
    )

    scope_options = [
        "Complete Portfolio"
    ]

    if columns["district"]:
        scope_options.append(
            "Selected District"
        )

    if columns["estate"]:
        scope_options.append(
            "Selected Estate"
        )

    report_scope = st.selectbox(
        "Report scope",
        scope_options,
    )

    report_df = working_df.copy()

    # --------------------------------------------------------
    # SELECTED DISTRICT
    # --------------------------------------------------------

    if (
        report_scope
        == "Selected District"
        and columns["district"]
    ):

        districts = (
            working_df[
                columns["district"]
            ]
            .dropna()
            .astype(str)
            .sort_values()
            .unique()
            .tolist()
        )

        if districts:

            selected_district = st.selectbox(
                "Select district",
                districts,
            )

            report_df = working_df[
                working_df[
                    columns["district"]
                ].astype(str)
                == selected_district
            ].copy()

    # --------------------------------------------------------
    # SELECTED ESTATE
    # --------------------------------------------------------

    elif (
        report_scope
        == "Selected Estate"
        and columns["estate"]
    ):

        estates = (
            working_df[
                columns["estate"]
            ]
            .dropna()
            .astype(str)
            .sort_values()
            .unique()
            .tolist()
        )

        if estates:

            selected_estate = st.selectbox(
                "Select estate",
                estates,
            )

            report_df = working_df[
                working_df[
                    columns["estate"]
                ].astype(str)
                == selected_estate
            ].copy()

    # --------------------------------------------------------
    # FINAL SAFETY
    # --------------------------------------------------------

    report_df = remove_duplicate_columns(
        report_df
    )

    # ========================================================
    # REPORT KPIs
    # ========================================================

    st.subheader(
        "Report Overview"
    )

    metric_columns = st.columns(4)

    # --------------------------------------------------------
    # Records
    # --------------------------------------------------------

    with metric_columns[0]:

        st.metric(
            "Records",
            f"{len(report_df):,}",
        )

    # --------------------------------------------------------
    # Estates
    # --------------------------------------------------------

    with metric_columns[1]:

        if columns["estate"]:

            estate_count = (
                report_df[
                    columns["estate"]
                ].nunique()
            )

            st.metric(
                "Estates",
                f"{estate_count:,}",
            )

        else:

            st.metric(
                "Estates",
                "N/A",
            )

    # --------------------------------------------------------
    # Yield
    # --------------------------------------------------------

    with metric_columns[2]:

        avg_yield = safe_mean(
            report_df,
            columns["yield"],
        )

        if avg_yield is not None:

            st.metric(
                "Avg Yield",
                f"{avg_yield:,.1f} kg/ha",
            )

        else:

            st.metric(
                "Avg Yield",
                "N/A",
            )

    # --------------------------------------------------------
    # Health
    # --------------------------------------------------------

    with metric_columns[3]:

        avg_health = safe_mean(
            report_df,
            columns["health"],
        )

        if avg_health is not None:

            st.metric(
                "Avg Health",
                f"{avg_health:,.1f}",
            )

        else:

            st.metric(
                "Avg Health",
                "N/A",
            )

    st.divider()

    # ========================================================
    # EXPORT SECTION
    # ========================================================

    st.subheader(
        "Export Report"
    )

    export_col1, export_col2 = st.columns(2)

    # --------------------------------------------------------
    # CSV EXPORT
    # --------------------------------------------------------

    with export_col1:

        csv_data = report_df.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name=(
                "estateinsight_report_data.csv"
            ),
            mime="text/csv",
            use_container_width=True,
        )

    # --------------------------------------------------------
    # PDF EXPORT
    # --------------------------------------------------------

    with export_col2:

        if REPORTLAB_AVAILABLE:

            pdf_data = generate_pdf_report(
                report_df,
                report_scope=report_scope,
            )

            if pdf_data:

                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_data,
                    file_name=(
                        "estateinsight_"
                        "analytics_report.pdf"
                    ),
                    mime="application/pdf",
                    use_container_width=True,
                )

            else:

                st.warning(
                    "PDF generation could not be completed."
                )

        else:

            st.warning(
                "PDF export requires ReportLab."
            )

            st.code(
                "pip install reportlab"
            )

    st.divider()

    # ========================================================
    # REPORT CONTENT
    # ========================================================

    st.subheader(
        "Report Contents"
    )

    contents = [
        "Executive summary",
        "Portfolio overview",
        "Performance metrics",
        "Financial indicators",
        "Climate & environmental indicators",
        "Disease & pest risk",
        "District performance",
        "Top performing estates",
        "Management insights",
        "Methodology & notes",
    ]

    for item in contents:

        st.markdown(
            f"✓ {item}"
        )

    st.divider()

    # ========================================================
    # TOP PERFORMING ESTATES
    # ========================================================

    if (
        columns["estate"]
        and columns["yield"]
    ):

        st.subheader(
            "🏆 Top Performing Estates"
        )

        # ----------------------------------------------------
        # Build unique column list
        # ----------------------------------------------------

        display_columns = unique_columns(
            [
                columns["estate"],
                columns["district"],
                columns["yield"],
                columns["health"],
                columns["sustainability"],
            ]
        )

        # ----------------------------------------------------
        # Select only valid columns
        # ----------------------------------------------------

        display_columns = [
            column
            for column in display_columns
            if column in report_df.columns
        ]

        # ----------------------------------------------------
        # Create dataframe
        # ----------------------------------------------------

        top_df = report_df[
            display_columns
        ].copy()

        # ----------------------------------------------------
        # Remove duplicate columns again
        # ----------------------------------------------------

        top_df = safe_dataframe(
            top_df
        )

        # ----------------------------------------------------
        # Temporary numeric sort column
        # ----------------------------------------------------

        top_df[
            "__yield_sort__"
        ] = to_numeric(
            top_df[
                columns["yield"]
            ]
        )

        top_df = (
            top_df
            .sort_values(
                "__yield_sort__",
                ascending=False,
            )
            .head(10)
        )

        # ----------------------------------------------------
        # Remove temporary column
        # ----------------------------------------------------

        top_df = top_df.drop(
            columns=[
                "__yield_sort__"
            ],
            errors="ignore",
        )

        # ----------------------------------------------------
        # Final PyArrow safety
        # ----------------------------------------------------

        top_df = safe_dataframe(
            top_df
        )

        # ----------------------------------------------------
        # Rename for display
        # ----------------------------------------------------

        rename_map = {}

        if columns["estate"]:
            rename_map[
                columns["estate"]
            ] = "Estate"

        if columns["district"]:
            rename_map[
                columns["district"]
            ] = "District"

        if columns["yield"]:
            rename_map[
                columns["yield"]
            ] = "Yield (kg/ha)"

        if columns["health"]:
            rename_map[
                columns["health"]
            ] = "Health Score"

        if columns["sustainability"]:
            rename_map[
                columns["sustainability"]
            ] = "Sustainability"

        top_df = top_df.rename(
            columns=rename_map
        )

        # ----------------------------------------------------
        # FINAL duplicate protection after rename
        # ----------------------------------------------------

        top_df = safe_dataframe(
            top_df
        )

        st.dataframe(
            top_df,
            use_container_width=True,
            hide_index=True,
        )

    # ========================================================
    # DISTRICT SUMMARY
    # ========================================================

    if columns["district"]:

        st.subheader(
            "📍 District Summary"
        )

        aggregation = {}

        if columns["yield"]:
            aggregation[
                columns["yield"]
            ] = "mean"

        if columns["health"]:
            aggregation[
                columns["health"]
            ] = "mean"

        if columns["sustainability"]:
            aggregation[
                columns["sustainability"]
            ] = "mean"

        if aggregation:

            district_summary = (
                report_df
                .groupby(
                    columns["district"],
                    dropna=False,
                )
                .agg(aggregation)
                .reset_index()
            )

            district_summary = safe_dataframe(
                district_summary
            )

            rename_map = {
                columns["district"]:
                "District"
            }

            if columns["yield"]:
                rename_map[
                    columns["yield"]
                ] = "Avg Yield (kg/ha)"

            if columns["health"]:
                rename_map[
                    columns["health"]
                ] = "Avg Health"

            if columns["sustainability"]:
                rename_map[
                    columns["sustainability"]
                ] = "Avg Sustainability"

            district_summary = (
                district_summary
                .rename(
                    columns=rename_map
                )
            )

            district_summary = safe_dataframe(
                district_summary
            )

            st.dataframe(
                district_summary,
                use_container_width=True,
                hide_index=True,
            )

    # ========================================================
    # DATASET INFORMATION
    # ========================================================

    st.divider()

    st.subheader(
        "📊 Dataset Information"
    )

    info_col1, info_col2, info_col3 = st.columns(3)

    with info_col1:

        st.metric(
            "Rows",
            f"{len(report_df):,}",
        )

    with info_col2:

        st.metric(
            "Columns",
            f"{len(report_df.columns):,}",
        )

    with info_col3:

        missing_values = int(
            report_df.isna()
            .sum()
            .sum()
        )

        st.metric(
            "Missing Values",
            f"{missing_values:,}",
        )

    # ========================================================
    # AVAILABLE FIELDS
    # ========================================================

    with st.expander(
        "View Available Dataset Fields"
    ):

        field_df = pd.DataFrame(
            {
                "Field": list(
                    report_df.columns
                )
            }
        )

        field_df = safe_dataframe(
            field_df
        )

        st.dataframe(
            field_df,
            use_container_width=True,
            hide_index=True,
        )

    # ========================================================
    # REPORT TIP
    # ========================================================

    st.info(
        "💡 Tip: Use the report scope selector to generate "
        "a portfolio-wide report or focus the export on a "
        "specific district or estate."
    )

    # ========================================================
    # FOOTER
    # ========================================================

    st.divider()

    st.caption(
        "EstateInsight • Coffee Estate Analytics • "
        "Reports & Export"
    )