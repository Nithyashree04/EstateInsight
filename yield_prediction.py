# ============================================================
# COFFEE ESTATE ANALYTICS
# FILE : 05_yield_prediction.py
# ============================================================

import pandas as pd
import numpy as np
import os
import joblib
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# ============================================================
# LOAD PREPROCESSED DATA
# ============================================================

print("=" * 60)
print("LOADING PREPROCESSED DATA")
print("=" * 60)

X_train = pd.read_csv("Processed_Data/X_train.csv")
X_test = pd.read_csv("Processed_Data/X_test.csv")

y_train = pd.read_csv("Processed_Data/y_train.csv").values.ravel()
y_test = pd.read_csv("Processed_Data/y_test.csv").values.ravel()

# Load original feature names
feature_names = joblib.load("Models/feature_names.pkl")

print("Training Shape :", X_train.shape)
print("Testing Shape  :", X_test.shape)

# ============================================================
# CREATE MODELS
# ============================================================
models = {

    "Linear Regression": LinearRegression(),

    "Decision Tree": DecisionTreeRegressor(
        random_state=42,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2
    ),

    "Random Forest": RandomForestRegressor(
        n_estimators=300,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features="sqrt",
        random_state=42,
        n_jobs=-1
    ),

    "Gradient Boosting": GradientBoostingRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=4,
        subsample=0.8,
        random_state=42
    )

}

results = []

best_model = None
best_model_name = ""
best_score = -999

# ============================================================
# TRAIN MODELS
# ============================================================

for name, model in models.items():

    print("\n" + "=" * 60)
    print(name.upper())
    print("=" * 60)

    # Train Model
    model.fit(X_train, y_train)

    # Predictions
    predictions = model.predict(X_test)

    # Evaluation Metrics
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)

    print(f"MAE  : {mae:.2f}")
    print(f"MSE  : {mse:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"R2   : {r2:.4f}")

    results.append({
        "Model": name,
        "MAE": mae,
        "MSE": mse,
        "RMSE": rmse,
        "R2": r2
    })

    if r2 > best_score:
        best_score = r2
        best_model = model
        best_model_name = name

# ============================================================
# MODEL COMPARISON
# ============================================================

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    by="R2",
    ascending=False
)

print("\n")
print("=" * 60)
print("MODEL COMPARISON")
print("=" * 60)

print(results_df)

# ============================================================
# SAVE RESULTS
# ============================================================

os.makedirs("Results", exist_ok=True)
os.makedirs("Models", exist_ok=True)

results_df.to_csv(
    "Results/model_comparison.csv",
    index=False
)

joblib.dump(
    best_model,
    "Models/yield_prediction_model.pkl"
)

print("\nResults saved.")
print("Best Model Saved.")
print("Best Model :", best_model_name)
print("Best R2 Score :", round(best_score, 4))


# ============================================================
# FEATURE IMPORTANCE / COEFFICIENTS
# ============================================================

importance = None

# Tree Models
if hasattr(best_model, "feature_importances_"):

    importance = pd.DataFrame({
        "Feature": feature_names,
        "Importance": best_model.feature_importances_
    })

# Linear Regression
elif hasattr(best_model, "coef_"):

    importance = pd.DataFrame({
        "Feature": feature_names,
        "Importance": np.abs(best_model.coef_)
    })

if importance is not None:

    importance = importance.sort_values(
        by="Importance",
        ascending=False
    )

    print("\n" + "=" * 60)
    print("TOP 15 IMPORTANT FEATURES")
    print("=" * 60)

    print(importance.head(15))

    importance.to_csv(
        "Results/feature_importance.csv",
        index=False
    )

    plt.figure(figsize=(12,7))

    plt.barh(
        importance["Feature"][:15],
        importance["Importance"][:15],
        color="steelblue"
    )

    plt.gca().invert_yaxis()

    plt.xlabel("Importance")
    plt.ylabel("Features")
    plt.title(f"Top 15 Important Features ({best_model_name})")

    plt.tight_layout()

    plt.savefig(
        "Results/feature_importance.png",
        dpi=300
    )

    plt.close()

    print("\nFeature Importance Graph Saved.")

else:

    print("\nFeature importance not available.")
# ============================================================
# ACTUAL VS PREDICTED GRAPH
# ============================================================

predictions = best_model.predict(X_test)

plt.figure(figsize=(8, 8))

plt.scatter(
    y_test,
    predictions,
    alpha=0.5
)

minimum = min(y_test.min(), predictions.min())
maximum = max(y_test.max(), predictions.max())

plt.plot(
    [minimum, maximum],
    [minimum, maximum],
    'r--',
    linewidth=2
)

plt.xlabel("Actual Yield (kg/ha)")
plt.ylabel("Predicted Yield (kg/ha)")
plt.title("Actual vs Predicted Yield")

plt.tight_layout()

plt.savefig(
    "Results/actual_vs_predicted.png",
    dpi=300
)

plt.close()

print("Prediction Graph Saved.")

# ============================================================
# COMPLETED
# ============================================================

print("\n")
print("=" * 60)
print("YIELD PREDICTION COMPLETED SUCCESSFULLY")
print("=" * 60)

print("Best Model :", best_model_name)
print("Best R2 Score :", round(best_score, 4))
print("Model Saved : Models/yield_prediction_model.pkl")
print("Comparison  : Results/model_comparison.csv")
print("Feature Importance : Results/feature_importance.csv")
print("Graphs Saved : Results Folder")
print("=" * 60)