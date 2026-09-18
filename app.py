# ============================================================
# ESTATEINSIGHT
# COFFEE ESTATE MANAGEMENT SYSTEM
# FINAL app.py
# ============================================================

import streamlit as st
import pandas as pd
import plotly.io as pio
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EstateInsight | Coffee Estate Analytics",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# APPLICATION SETTINGS
# ============================================================

APP_NAME = "EstateInsight"
APP_SUBTITLE = "COFFEE ESTATE MANAGEMENT SYSTEM"

LOGIN_PASSWORD = "Admin@"

PAGE_HOME = "🏠 Dashboard"
PAGE_HEALTH = "❤️ Estate Health"
PAGE_CLIMATE = "🌦️ Climate Analytics"
PAGE_QUALITY = "☕ Coffee Quality"
PAGE_DISEASE = "🦠 Disease & Pest"
PAGE_SOIL = "🌱 Soil & Nutrient"
PAGE_SUSTAINABILITY = "♻️ Sustainability"
PAGE_DISTRICT = "🗺️ District Analytics"
PAGE_AI = "🤖 AI Intelligence"
PAGE_SEARCH = "🔎 Smart Search"
PAGE_REPORTS = "📄 Reports & Export"

PAGES = [
    PAGE_HOME,
    PAGE_HEALTH,
    PAGE_CLIMATE,
    PAGE_QUALITY,
    PAGE_DISEASE,
    PAGE_SOIL,
    PAGE_SUSTAINABILITY,
    PAGE_DISTRICT,
    PAGE_AI,
    PAGE_SEARCH,
    PAGE_REPORTS,
]


# ============================================================
# PLOTLY DEFAULT
# ============================================================

pio.templates.default = "plotly_white"


# ============================================================
# SESSION STATE
# ============================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "page" not in st.session_state:
    st.session_state.page = PAGE_HOME

if "username" not in st.session_state:
    st.session_state.username = "Estate Manager"


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       FONTS
    ======================================================== */

    @import url(
        'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap'
    );


    /* ========================================================
       GLOBAL APP
    ======================================================== */

    html,
    body,
    [class*="css"] {
        font-family: "DM Sans", sans-serif !important;
    }

    .stApp {
        background: #F7F3ED !important;
        color: #211811 !important;
    }

    [data-testid="stAppViewContainer"] {
        background: #F7F3ED !important;
    }

    [data-testid="stAppViewContainer"] .main {
        background: #F7F3ED !important;
    }


    /* ========================================================
       REMOVE STREAMLIT TOP HEADER
    ======================================================== */

    header,
    [data-testid="stHeader"] {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        visibility: hidden !important;
    }

    [data-testid="stToolbar"] {
        display: none !important;
    }

    [data-testid="stDecoration"] {
        display: none !important;
    }

    #MainMenu {
        visibility: hidden !important;
    }

    footer {
        visibility: hidden !important;
    }


    /* ========================================================
       MAIN CONTAINER
    ======================================================== */

    [data-testid="stAppViewContainer"]
    .main
    .block-container {

        max-width: 1500px !important;

        padding-top: 1.4rem !important;

        padding-bottom: 3rem !important;

        color: #211811 !important;
    }


    /* ========================================================
       ALL TEXT
    ======================================================== */

    .stApp p,
    .stApp label,
    .stApp span,
    .stApp small,
    .stApp div {
        color: #33271F;
    }

    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp h5,
    .stApp h6 {
        color: #211811 !important;
    }


    /* ========================================================
       SIDEBAR
    ======================================================== */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #2E1C15 0%,
                #1D110D 100%
            ) !important;

        border-right:
            1px solid #4B3327 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #F7EFE8 !important;
    }

    section[data-testid="stSidebar"] p {
        color: #D3C3B7 !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #584034 !important;
    }


    /* ========================================================
       SIDEBAR BUTTONS
    ======================================================== */

    section[data-testid="stSidebar"]
    .stButton > button {

        width: 100% !important;

        min-height: 42px !important;

        background: transparent !important;

        color: #F8F0E8 !important;

        border: 1px solid transparent !important;

        border-radius: 10px !important;

        text-align: left !important;

        padding-left: 13px !important;

        font-size: 14px !important;

        font-weight: 600 !important;

        transition:
            background 0.2s ease,
            border 0.2s ease,
            transform 0.2s ease !important;
    }

    section[data-testid="stSidebar"]
    .stButton > button:hover {

        background:
            rgba(255,255,255,0.10) !important;

        border:
            1px solid rgba(255,255,255,0.08) !important;

        color:
            #FFFFFF !important;

        transform:
            translateX(2px);
    }


    /* ========================================================
       MAIN BUTTONS
    ======================================================== */

    .stButton > button {

        background:
            #704A31 !important;

        color:
            #FFFFFF !important;

        border:
            none !important;

        border-radius:
            10px !important;

        font-weight:
            600 !important;

        transition:
            all 0.2s ease !important;
    }

    .stButton > button p,
    .stButton > button span {

        color:
            #FFFFFF !important;
    }

    .stButton > button:hover {

        background:
            #573923 !important;

        color:
            #FFFFFF !important;

        transform:
            translateY(-1px);
    }


    /* ========================================================
       INPUTS
    ======================================================== */

    .stTextInput input,
    .stTextArea textarea,
    input[type="text"],
    input[type="search"],
    input[type="password"] {

        background:
            #FFFFFF !important;

        color:
            #111111 !important;

        -webkit-text-fill-color:
            #111111 !important;

        caret-color:
            #111111 !important;

        border:
            1.5px solid #B9A99B !important;

        border-radius:
            11px !important;

        font-size:
            15px !important;

        font-weight:
            500 !important;

        opacity:
            1 !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder,
    input::placeholder {

        color:
            #665A52 !important;

        -webkit-text-fill-color:
            #665A52 !important;

        opacity:
            1 !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus,
    input[type="text"]:focus,
    input[type="search"]:focus,
    input[type="password"]:focus {

        background:
            #FFFFFF !important;

        color:
            #111111 !important;

        -webkit-text-fill-color:
            #111111 !important;

        caret-color:
            #111111 !important;

        border:
            2px solid #704A31 !important;

        box-shadow:
            0 0 0 3px
            rgba(112,74,49,0.12) !important;

        outline:
            none !important;
    }


    /* ========================================================
       SELECTBOX
    ======================================================== */

    [data-baseweb="select"] > div {

        background:
            #FFFFFF !important;

        color:
            #111111 !important;

        border:
            1.5px solid #B9A99B !important;

        border-radius:
            10px !important;
    }

    [data-baseweb="select"] span {
        color: #111111 !important;
    }

    [data-baseweb="select"] input {

        color:
            #111111 !important;

        -webkit-text-fill-color:
            #111111 !important;

        caret-color:
            #111111 !important;
    }

    [role="listbox"] {
        background: #FFFFFF !important;
    }

    [role="option"] {

        background:
            #FFFFFF !important;

        color:
            #111111 !important;
    }

    [role="option"]:hover {

        background:
            #F0E7DE !important;

        color:
            #111111 !important;
    }


    /* ========================================================
       MULTISELECT
    ======================================================== */

    [data-testid="stMultiSelect"] {
        color: #111111 !important;
    }

    [data-testid="stMultiSelect"] * {
        color: #111111 !important;
    }

    [data-testid="stMultiSelect"] input {

        color:
            #111111 !important;

        -webkit-text-fill-color:
            #111111 !important;
    }


    /* ========================================================
       METRIC CARDS
    ======================================================== */

    [data-testid="stMetric"] {

        background:
            #FFFFFF !important;

        border:
            1px solid #E2D5C8 !important;

        border-radius:
            16px !important;

        padding:
            17px !important;

        box-shadow:
            0 7px 20px
            rgba(64,43,28,0.07) !important;
    }

    [data-testid="stMetricLabel"] {
        color: #5E5048 !important;
    }

    [data-testid="stMetricLabel"] * {
        color: #5E5048 !important;
    }

    [data-testid="stMetricValue"] {
        color: #211811 !important;
    }

    [data-testid="stMetricValue"] * {
        color: #211811 !important;
    }


    /* ========================================================
       CARDS
    ======================================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {

        background:
            #FFFFFF !important;

        border:
            1px solid #E0D3C7 !important;

        border-radius:
            16px !important;

        box-shadow:
            0 7px 20px
            rgba(65,42,26,0.055) !important;
    }


    /* ========================================================
       DATAFRAMES
    ======================================================== */

    [data-testid="stDataFrame"] {

        background:
            #FFFFFF !important;

        border:
            1px solid #DED1C5 !important;

        border-radius:
            12px !important;
    }


    /* ========================================================
       EXPANDERS
    ======================================================== */

    [data-testid="stExpander"] {

        background:
            #FFFFFF !important;

        border:
            1px solid #DED1C5 !important;

        border-radius:
            12px !important;
    }


    /* ========================================================
       DOWNLOAD BUTTONS
    ======================================================== */

    .stDownloadButton > button {

        background:
            #704A31 !important;

        color:
            #FFFFFF !important;

        border:
            none !important;

        border-radius:
            10px !important;

        font-weight:
            600 !important;
    }

    .stDownloadButton > button * {
        color: #FFFFFF !important;
    }


    /* ========================================================
       PLOTLY / GRAPH TEXT
    ======================================================== */

    .js-plotly-plot,
    .plot-container {
        color: #211811 !important;
    }

    .js-plotly-plot svg text {
        fill: #211811 !important;
    }

    .js-plotly-plot .xtick text,
    .js-plotly-plot .ytick text,
    .js-plotly-plot .tick text,
    .js-plotly-plot .axis-title,
    .js-plotly-plot .gtitle,
    .js-plotly-plot .legendtext,
    .js-plotly-plot .annotation-text {

        fill: #211811 !important;

        color: #211811 !important;
    }

    .js-plotly-plot .axis path,
    .js-plotly-plot .axis line {
        stroke: #80736A !important;
    }

    .js-plotly-plot .gridlayer path {
        stroke: #DED7D0 !important;
    }


    /* ========================================================
       CHECKBOXES / RADIO LABELS
    ======================================================== */

    .stCheckbox label,
    .stRadio label {
        color: #211811 !important;
    }

    .stCheckbox label *,
    .stRadio label * {
        color: #211811 !important;
    }


    /* ========================================================
       CAPTIONS
    ======================================================== */

    .stCaption,
    [data-testid="stCaptionContainer"] {
        color: #655951 !important;
    }


    /* ========================================================
       DIVIDERS
    ======================================================== */

    hr {
        border-color: #DDD1C5 !important;
    }


    /* ========================================================
       SCROLLBAR
    ======================================================== */

    ::-webkit-scrollbar {

        width:
            8px;

        height:
            8px;
    }

    ::-webkit-scrollbar-track {
        background: #EFE8E0;
    }

    ::-webkit-scrollbar-thumb {

        background:
            #B5A497;

        border-radius:
            10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #8D7765;
    }


    /* ========================================================
       LOGIN
    ======================================================== */

    .login-spacer {
        height: 8vh;
    }


    /* ========================================================
       PAGE ANIMATION
    ======================================================== */

    @keyframes estateFadeIn {

        from {

            opacity:
                0;

            transform:
                translateY(8px);
        }

        to {

            opacity:
                1;

            transform:
                translateY(0);
        }
    }

    .main .block-container {

        animation:
            estateFadeIn
            0.35s
            ease-out;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOGIN PAGE
# ============================================================

def show_login():

    st.markdown(
        '<div class="login-spacer"></div>',
        unsafe_allow_html=True,
    )

    left, center, right = st.columns(
        [1, 1.35, 1]
    )

    with center:

        with st.container(border=True):

            st.markdown("## ☕")

            st.title("EstateInsight")

            st.caption(
                "COFFEE ESTATE MANAGEMENT SYSTEM"
            )

            st.divider()

            st.subheader("🔐 Sign in")

            username = st.text_input(
                "Username",
                placeholder="Enter your username",
                key="login_username",
            )

            password = st.text_input(
                "Password",
                placeholder="Enter your password",
                type="password",
                key="login_password",
            )

            st.write("")

            if st.button(
                "Sign In  →",
                use_container_width=True,
                key="login_button",
            ):

                if password == LOGIN_PASSWORD:

                    st.session_state.authenticated = True

                    if username.strip():

                        st.session_state.username = (
                            username.strip()
                        )

                    else:

                        st.session_state.username = (
                            "Estate Manager"
                        )

                    st.session_state.page = PAGE_HOME

                    st.rerun()

                else:

                    st.error(
                        "Incorrect password. Please try again."
                    )

            st.write("")

            st.caption(
                "EstateInsight • Intelligent Coffee Estate Analytics"
            )


# ============================================================
# SHOW LOGIN IF NOT AUTHENTICATED
# ============================================================

if not st.session_state.authenticated:

    show_login()

    st.stop()


# ============================================================
# IMPORT DASHBOARD MODULES
# ============================================================

from dashboard.data_loader import load_data
from dashboard.home import show_home
from dashboard.health import show_health
from dashboard.climate import show_climate
from dashboard.quality import show_quality
from dashboard.disease import show_disease
from dashboard.soil import show_soil
from dashboard.sustainability import show_sustainability
from dashboard.district import show_district
from dashboard.ai import show_ai
from dashboard.search import show_search
from dashboard.reports import show_reports


# ============================================================
# LOAD DATA
# ============================================================

try:

    df = load_data()

except Exception as error:

    st.error(
        "Unable to load the estate dataset."
    )

    st.exception(error)

    st.stop()


if df is None or df.empty:

    st.error(
        "The estate dataset is empty."
    )

    st.stop()


# ============================================================
# CLEAN DATAFRAME
# ============================================================

df = df.copy()

df.columns = [
    str(column).strip()
    for column in df.columns
]


# Remove duplicate column names.
if df.columns.duplicated().any():

    df = df.loc[
        :,
        ~df.columns.duplicated()
    ].copy()


# ============================================================
# COLUMN DETECTION
# ============================================================

def find_column(dataframe, names):

    if dataframe is None:
        return None

    columns = list(
        dataframe.columns
    )

    # --------------------------------------------------------
    # Exact match
    # --------------------------------------------------------

    for name in names:

        if name in columns:
            return name

    # --------------------------------------------------------
    # Case-insensitive
    # --------------------------------------------------------

    lowered = {
        str(column).lower(): column
        for column in columns
    }

    for name in names:

        key = str(name).lower()

        if key in lowered:
            return lowered[key]

    # --------------------------------------------------------
    # Normalized match
    # --------------------------------------------------------

    def normalize(value):

        return (
            str(value)
            .lower()
            .replace("_", "")
            .replace("-", "")
            .replace(" ", "")
        )

    normalized_columns = {
        normalize(column): column
        for column in columns
    }

    for name in names:

        key = normalize(name)

        if key in normalized_columns:
            return normalized_columns[key]

    return None


def numeric_series(dataframe, column):

    if (
        column is None
        or column not in dataframe.columns
    ):

        return pd.Series(
            0,
            index=dataframe.index,
            dtype=float,
        )

    return pd.to_numeric(
        dataframe[column],
        errors="coerce",
    ).fillna(0)


district_col = find_column(
    df,
    [
        "District",
        "district",
        "District_Name",
    ],
)

estate_col = find_column(
    df,
    [
        "Estate_ID",
        "Estate ID",
        "Estate",
        "Estate_Name",
        "Estate Name",
    ],
)

farm_size_col = find_column(
    df,
    [
        "Farm_Size_Acres",
        "Farm Size Acres",
        "Farm_Size",
        "Area_Acres",
        "Area",
    ],
)

yield_col = find_column(
    df,
    [
        "Yield_kg_ha",
        "Yield (kg/ha)",
        "Yield",
        "Yield_kg",
    ],
)

health_col = find_column(
    df,
    [
        "Estate_Health_Score",
        "Health_Score",
        "Estate Health",
        "Health",
    ],
)

sustainability_col = find_column(
    df,
    [
        "Sustainability_Score",
        "Sustainability Score",
        "Sustainability",
    ],
)


# ============================================================
# NAVIGATION
# ============================================================

def go_to_page(page):

    if page not in PAGES:
        page = PAGE_HOME

    st.session_state.page = page

    st.rerun()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # BRAND
    # --------------------------------------------------------

    st.title(
        "☕ EstateInsight"
    )

    st.caption(
        APP_SUBTITLE
    )

    st.divider()

    # --------------------------------------------------------
    # USER
    # --------------------------------------------------------

    st.subheader(
        "👤 Estate Manager"
    )

    st.caption(
        st.session_state.username
    )

    st.divider()

    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

    st.subheader(
        "Navigation"
    )

    for page in PAGES:

        if page == st.session_state.page:

            button_text = (
                "🔴  " + page
            )

        else:

            button_text = (
                "○  " + page
            )

        if st.button(
            button_text,
            use_container_width=True,
            key=f"sidebar_nav_{page}",
        ):

            go_to_page(page)

    st.divider()

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    st.subheader(
        "🎛️ Portfolio Filters"
    )

    filtered_df = df.copy()

    # --------------------------------------------------------
    # DISTRICT FILTER
    # --------------------------------------------------------

    if district_col:

        district_values = sorted(
            df[district_col]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_districts = st.multiselect(
            "District",
            district_values,
            default=district_values,
            key="global_district_filter",
        )

        if selected_districts:

            filtered_df = filtered_df[
                filtered_df[district_col]
                .astype(str)
                .isin(selected_districts)
            ]

    # --------------------------------------------------------
    # ESTATE FILTER
    # --------------------------------------------------------

    if estate_col:

        estate_values = sorted(
            filtered_df[estate_col]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_estates = st.multiselect(
            "Estate",
            estate_values,
            default=[],
            key="global_estate_filter",
        )

        if selected_estates:

            filtered_df = filtered_df[
                filtered_df[estate_col]
                .astype(str)
                .isin(selected_estates)
            ]

    st.divider()

    # --------------------------------------------------------
    # RECORD COUNT
    # --------------------------------------------------------

    st.caption(
        f"📊 Showing {len(filtered_df):,} "
        f"of {len(df):,} records"
    )

    # --------------------------------------------------------
    # LOGOUT
    # --------------------------------------------------------

    if st.button(
        "🚪 Logout",
        use_container_width=True,
        key="logout_button",
    ):

        st.session_state.authenticated = False

        st.session_state.page = PAGE_HOME

        st.rerun()


# ============================================================
# TOP BAR
# ============================================================

header_left, header_search, header_right = st.columns(
    [2.0, 2.0, 0.8]
)

with header_left:

    st.subheader(
        "☕ Coffee Estate Intelligence Platform"
    )

with header_search:

    global_search = st.text_input(
        "Search",
        placeholder="🔎 Search estates, districts, analytics...",
        label_visibility="collapsed",
        key="global_search_box",
    )

with header_right:

    st.markdown(
        "🟢 **ONLINE**"
    )

    st.caption(
        datetime.now().strftime(
            "%d %b %Y"
        )
    )

st.divider()


# ============================================================
# MAIN DASHBOARD
# ============================================================

def show_main_dashboard(data):

    # --------------------------------------------------------
    # KPI CALCULATIONS
    # Revenue has been completely removed.
    # --------------------------------------------------------

    total_area = (
        numeric_series(
            data,
            farm_size_col,
        ).sum()
        if farm_size_col
        else 0
    )

    average_yield = (
        numeric_series(
            data,
            yield_col,
        ).mean()
        if yield_col
        else 0
    )

    average_health = (
        numeric_series(
            data,
            health_col,
        ).mean()
        if health_col
        else 0
    )


    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    hero_left, hero_right = st.columns(
        [3.2, 1.0]
    )

    with hero_left:

        st.title(
            "Welcome back, Estate Manager! ☕"
        )

        st.caption(
            "Here's what's happening across your "
            "coffee estate portfolio today."
        )

    with hero_right:

        st.subheader(
            "📅 "
            + datetime.now().strftime(
                "%d %B %Y"
            )
        )

        st.caption(
            "Estate management dashboard"
        )

    st.write("")


    # --------------------------------------------------------
    # KPI CARDS
    # ONLY 3 CARDS
    # --------------------------------------------------------

    k1, k2, k3 = st.columns(3)

    with k1:

        st.metric(
            "🌿 Total Estate Area",
            (
                f"{total_area:,.1f} acres"
                if farm_size_col
                else "N/A"
            ),
        )

    with k2:

        st.metric(
            "☕ Average Yield",
            (
                f"{average_yield:,.0f} kg/ha"
                if yield_col
                else "N/A"
            ),
        )

    with k3:

        st.metric(
            "❤️ Estate Health",
            (
                f"{average_health:.1f}%"
                if health_col
                else "N/A"
            ),
        )

    st.write("")


    # --------------------------------------------------------
    # ESTATE INTELLIGENCE
    # --------------------------------------------------------

    st.subheader(
        "Estate Intelligence"
    )

    st.caption(
        "Access the tools you need to monitor, "
        "analyse and improve your estate."
    )


    # --------------------------------------------------------
    # MODULE CARDS
    # --------------------------------------------------------

    cards = [

        (
            "❤️",
            "Estate Health",
            "Monitor overall estate health and performance.",
            PAGE_HEALTH,
        ),

        (
            "🌦️",
            "Climate Analytics",
            "Understand weather conditions and climate patterns.",
            PAGE_CLIMATE,
        ),

        (
            "☕",
            "Coffee Quality",
            "Explore coffee quality and production indicators.",
            PAGE_QUALITY,
        ),

        (
            "🦠",
            "Disease & Pest",
            "Identify disease and pest risk across estates.",
            PAGE_DISEASE,
        ),

        (
            "🌱",
            "Soil & Nutrient",
            "Analyse soil characteristics and nutrient conditions.",
            PAGE_SOIL,
        ),

        (
            "♻️",
            "Sustainability",
            "Track sustainability and environmental performance.",
            PAGE_SUSTAINABILITY,
        ),

        (
            "🗺️",
            "District Analytics",
            "Compare estate performance across districts.",
            PAGE_DISTRICT,
        ),

        (
            "🤖",
            "AI Intelligence",
            "Get intelligent recommendations for estate management.",
            PAGE_AI,
        ),
    ]


    # --------------------------------------------------------
    # CARD GRID
    # --------------------------------------------------------

    for row_start in range(
        0,
        len(cards),
        4,
    ):

        row_cards = cards[
            row_start:
            row_start + 4
        ]

        columns = st.columns(4)

        for index, card in enumerate(
            row_cards
        ):

            icon, title, description, target_page = card

            with columns[index]:

                with st.container(
                    border=True
                ):

                    st.subheader(
                        f"{icon} {title}"
                    )

                    st.caption(
                        description
                    )

                    st.write("")

                    if st.button(
                        "Explore →",
                        use_container_width=True,
                        key=f"explore_button_{index}_{target_page}",
                    ):

                        go_to_page(
                            target_page
                        )

    st.write("")


    # --------------------------------------------------------
    # PORTFOLIO OVERVIEW
    # --------------------------------------------------------

    st.subheader(
        "Portfolio Overview"
    )

    overview_left, overview_right = st.columns(2)

    with overview_left:

        with st.container(
            border=True
        ):

            st.subheader(
                "📊 Portfolio Records"
            )

            st.metric(
                "Active Records",
                f"{len(data):,}",
            )

            if district_col:

                st.metric(
                    "Districts Covered",
                    f"{data[district_col].nunique():,}",
                )

    with overview_right:

        with st.container(
            border=True
        ):

            st.subheader(
                "🌱 System Status"
            )

            st.success(
                "Analytics engine operational"
            )

            st.caption(
                "All dashboard modules are connected "
                "to the master estate dataset."
            )

    st.write("")


    # --------------------------------------------------------
    # RECENT RECORDS
    # --------------------------------------------------------

    st.subheader(
        "Latest Estate Records"
    )

    preview_columns = []

    for column in [
        estate_col,
        district_col,
        yield_col,
        health_col,
        sustainability_col,
    ]:

        if (
            column is not None
            and column in data.columns
            and column not in preview_columns
        ):

            preview_columns.append(
                column
            )

    if preview_columns:

        preview_df = data[
            preview_columns
        ].head(10).copy()

        preview_df = preview_df.loc[
            :,
            ~preview_df.columns.duplicated(),
        ]

        st.dataframe(
            preview_df,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# PAGE ROUTER
# ============================================================

current_page = st.session_state.page


if current_page == PAGE_HOME:

    show_main_dashboard(
        filtered_df
    )

elif current_page == PAGE_HEALTH:

    show_health(
        filtered_df
    )

elif current_page == PAGE_CLIMATE:

    show_climate(
        filtered_df
    )

elif current_page == PAGE_QUALITY:

    show_quality(
        filtered_df
    )

elif current_page == PAGE_DISEASE:

    show_disease(
        filtered_df
    )

elif current_page == PAGE_SOIL:

    show_soil(
        filtered_df
    )

elif current_page == PAGE_SUSTAINABILITY:

    show_sustainability(
        filtered_df
    )

elif current_page == PAGE_DISTRICT:

    show_district(
        filtered_df
    )

elif current_page == PAGE_AI:

    show_ai(
        filtered_df
    )

elif current_page == PAGE_SEARCH:

    show_search(
        df
    )

elif current_page == PAGE_REPORTS:

    show_reports(
        filtered_df
    )

else:

    st.session_state.page = PAGE_HOME

    st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "☕ EstateInsight • Coffee Estate Intelligence Platform • "
    "Intelligent analytics for smarter coffee estate decisions."
)