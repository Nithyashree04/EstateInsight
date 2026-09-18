# ============================================================
# COFFEE ESTATE ANALYTICS PROJECT
# FILE : 04_data_preprocessing.py
# ============================================================

import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

# ============================================================
# LOAD DATASET
# ============================================================

print("=" * 60)
print("LOADING DATASET")
print("=" * 60)

df = pd.read_csv(
    r"C:\Users\Admin\Downloads\Karnataka_Coffee_Master_V3_15000.csv"
)

print(df.shape)

# ============================================================
# REMOVE ID COLUMN
# ============================================================

print("\nRemoving Estate_ID column...")

if "Estate_ID" in df.columns:
    df.drop(columns=["Estate_ID"], inplace=True)

print("Estate_ID removed.")

# ============================================================
# TARGET COLUMN
# ============================================================

target_column = "Yield_kg_ha"

X = df.drop(
    columns=[
        "Yield_kg_ha",
        "Yield_Category"       # Prevent target leakage
    ]
)

y = df[target_column]

print("\nFeatures Shape :", X.shape)
print("Target Shape   :", y.shape)

# ============================================================
# IDENTIFY COLUMN TYPES
# ============================================================

categorical_columns = X.select_dtypes(
    include=["object", "string"]
).columns.tolist()

numerical_columns = X.select_dtypes(
    exclude=["object", "string"]
).columns.tolist()

print("\nCategorical Columns")
print(categorical_columns)

print("\nNumerical Columns")
print(numerical_columns)

# ============================================================
# PREPROCESSOR
# ============================================================

print("\nApplying One-Hot Encoding + Scaling...")

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(
                drop="first",
                handle_unknown="ignore",
                sparse_output=False
            ),
            categorical_columns
        ),
        (
            "num",
            StandardScaler(),
            numerical_columns
        )
    ]
)

X_processed = preprocessor.fit_transform(X)

feature_names = preprocessor.get_feature_names_out()

X_processed = pd.DataFrame(
    X_processed,
    columns=feature_names
)

print("Encoding & Scaling Completed.")

print("\nTotal Features After Encoding :", len(feature_names))

# ============================================================
# TRAIN TEST SPLIT
# ============================================================

print("\nSplitting Dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X_processed,
    y,
    test_size=0.20,
    random_state=42
)

print("Training Samples :", len(X_train))
print("Testing Samples  :", len(X_test))

print("\nFeature Names Preserved Successfully.")
print(X_train.columns.tolist())

# ============================================================
# CREATE OUTPUT FOLDERS
# ============================================================

os.makedirs("Processed_Data", exist_ok=True)
os.makedirs("Models", exist_ok=True)

# ============================================================
# SAVE DATASETS
# ============================================================

X_train.to_csv(
    "Processed_Data/X_train.csv",
    index=False
)

X_test.to_csv(
    "Processed_Data/X_test.csv",
    index=False
)

y_train.to_frame().to_csv(
    "Processed_Data/y_train.csv",
    index=False
)

y_test.to_frame().to_csv(
    "Processed_Data/y_test.csv",
    index=False
)

# ============================================================
# SAVE PREPROCESSOR
# ============================================================

joblib.dump(
    preprocessor,
    "Models/preprocessor.pkl"
)

# ============================================================
# SAVE FEATURE NAMES
# ============================================================

joblib.dump(
    feature_names.tolist(),
    "Models/feature_names.pkl"
)

# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("PREPROCESSING SUMMARY")
print("=" * 60)

print("Original Dataset :", df.shape)
print("Training Set     :", X_train.shape)
print("Testing Set      :", X_test.shape)

print("\nOriginal Features :", X.shape[1])
print("Features After One-Hot Encoding :", len(feature_names))

print("\nSaved Files")
print("Processed_Data/X_train.csv")
print("Processed_Data/X_test.csv")
print("Processed_Data/y_train.csv")
print("Processed_Data/y_test.csv")
print("Models/preprocessor.pkl")
print("Models/feature_names.pkl")

print("\nPreprocessing Completed Successfully.")
print("=" * 60)