import numpy as np
import xgboost as xgb
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV


def train_models(X_train, y_train):
    print("Training Linear Regression (Baseline)...")
    lr = LinearRegression()
    lr.fit(X_train, y_train)

    print("Tuning Random Forest...")
    rf_param_grid = {
        'n_estimators': [100, 300],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5]
    }
    rf_grid = GridSearchCV(
        RandomForestRegressor(random_state=42), 
        rf_param_grid, 
        cv=3, 
        scoring='neg_root_mean_squared_error', 
        n_jobs=-1
    )
    rf_grid.fit(X_train, y_train)
    print(f"Best RF Params: {rf_grid.best_params_}")

    print("Tuning XGBoost...")
    xgb_param_grid = {
        'n_estimators': [100, 300],
        'learning_rate': [0.05, 0.1, 0.2],
        'max_depth': [3, 5, 7]
    }
    xgb_grid = GridSearchCV(
        xgb.XGBRegressor(objective="reg:squarederror", random_state=42), 
        xgb_param_grid, 
        cv=3, 
        scoring='neg_root_mean_squared_error', 
        n_jobs=-1
    )
    xgb_grid.fit(X_train, y_train)
    print(f"Best XGB Params: {xgb_grid.best_params_}")

    models = {
        "Linear Regression": lr,
        "Random Forest": rf_grid.best_estimator_,
        "XGBoost": xgb_grid.best_estimator_
    }

    return models


def evaluate_models(models, X_test, y_test):
    results = {}

    for name, model in models.items():
        preds = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        results[name] = {"rmse": rmse, "preds": preds}

    return results