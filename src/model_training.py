from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score
from joblib import Parallel, delayed
import numpy as np
import pandas as pd

def preprocess_data(df):
    """Handle missing values and check data integrity"""
    df = df.dropna()  # Remove rows with missing values
    if 'Tumor' not in df.columns:
        raise ValueError("Target column 'Tumor' not found in dataframe!")
    
    X = df.drop('Tumor', axis=1)
    y = df['Tumor']
    return X, y

def train_model(model, X_train, X_test, y_train, y_test):
    """Train a model and return its performance metrics"""
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:,1]

    return {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_proba),
        'confusion_matrix': confusion_matrix(y_test, y_pred)
    }

def train_and_evaluate(df):
    """Train models using optimized hyperparameters and parallel processing"""
    X, y = preprocess_data(df)
    
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    models = {
        'RandomForest': RandomForestClassifier(n_estimators=300, max_depth=12, n_jobs=-1, random_state=42),
        'XGBoost': XGBClassifier(n_estimators=200, max_depth=6, learning_rate=0.05, colsample_bytree=0.8, n_jobs=-1, random_state=42)
    }

    results = {}
    for train_idx, test_idx in skf.split(X, y):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        # Parallel training
        model_results = Parallel(n_jobs=1)(
            delayed(train_model)(models[name], X_train, X_test, y_train, y_test)
            for name in models
        )

        for name, metrics in zip(models.keys(), model_results):
            if name not in results:
                results[name] = {k: [] for k in metrics.keys()}
            for k, v in metrics.items():
                results[name][k].append(v)

    # Averaging metrics across folds
    for model in results:
        for metric in results[model]:
            results[model][metric] = np.mean(results[model][metric])

    return results
