import streamlit as st
import pandas as pd
import os


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "Processed_Data",
    "Coffee_Estate_Master.xlsx"
)


# ============================================================
# LOAD MASTER DATASET
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_excel(DATA_PATH)

    return df


# ============================================================
# LOAD RESULTS CSV
# ============================================================

@st.cache_data
def load_result_csv(filename):

    path = os.path.join(
        BASE_DIR,
        "Results",
        filename
    )

    if os.path.exists(path):

        return pd.read_csv(path)

    return None


# ============================================================
# GET RESULT PATH
# ============================================================

def get_result_path(filename):

    return os.path.join(
        BASE_DIR,
        "Results",
        filename
    )


# ============================================================
# DATASET INFORMATION
# ============================================================

def get_dataset_info():

    df = load_data()

    info = {

        "rows": df.shape[0],

        "columns": df.shape[1],

        "districts": df["District"].nunique(),

        "coffee_types": df["Coffee_Type"].nunique()

    }

    return info