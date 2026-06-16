import pandas as pd
import matplotlib.pyplot as plt
import os
import joblib

from preprocessing import clean_data, feature_engineering
from train import train_models, evaluate_models

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_data():
    train = pd.read_csv(os.path.join(BASE_DIR, "data", "df_train.csv"))
    test = pd.read_csv(os.path.join(BASE_DIR, "data", "df_test.csv"))
    return train, test


def prepare_data(train, test):

    train = clean_data(train)
    test = clean_data(test)

    train = feature_engineering(train)
    test = feature_engineering(test)

    # Align columns
    test = test.reindex(columns=train.columns, fill_value=0)

    X_train = train.drop(columns=["power_consumption", "date"])
    y_train = train["power_consumption"]

    X_test = test.drop(columns=["power_consumption", "date"])
    y_test = test["power_consumption"]

    return X_train, y_train, X_test, y_test, test


def plot_results(test, preds, model_name):

    plt.figure(figsize=(10,5))

    plt.plot(test["date"], test["power_consumption"], label="Actual", color="green")
    plt.plot(test["date"], preds, label="Predicted", color="brown")

    plt.title(f"Power Consumption - {model_name}")
    plt.xlabel("Date")
    plt.ylabel("Power Consumption")

    plt.legend()
    plt.tight_layout()
    plt.show()


def main():

    train, test = load_data()

    X_train, y_train, X_test, y_test, test_df = prepare_data(train, test)

    models = train_models(X_train, y_train)

    results = evaluate_models(models, X_test, y_test)

    summary = {
        name: results[name]["rmse"]
        for name in results
    }

    print("\nMODEL PERFORMANCE")
    for k, v in summary.items():
        print(k, ":", round(v, 3))

    best_model_name = min(results, key=lambda x: results[x]["rmse"])
    best_preds = results[best_model_name]["preds"]

    print("\nBEST MODEL:", best_model_name)
    
    # Save the best model to trained_model.pkl
    model_dir = os.path.join(BASE_DIR, "models")
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "trained_model.pkl")
    joblib.dump(models[best_model_name], model_path)
    print(f"Saved the best model to {model_path}")

    plot_results(test_df, best_preds, best_model_name)

    print("\nFINAL INSIGHT:")
    print("Energy consumption shows strong time-based patterns.")
    print("Tree-based models perform best for forecasting.")


if __name__ == "__main__":
    main()