from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score
from joblib import Parallel, delayed
import numpy as np
import pandas as pd

def preprocess_data(df):
    """
    Preprocess the dataframe by handling missing values and extracting features and target.
    
    Parameters:
        df (DataFrame): Input DataFrame.
    Returns:
        X (DataFrame): Feature data.
        y (Series): Target labels.
    """
    df = df.dropna()  # Remove rows with missing values
    if 'Tumor' not in df.columns:
        raise ValueError("Target column 'Tumor' not found in dataframe!")
    X = df.drop('Tumor', axis=1)
    y = df['Tumor']
    return X, y

def train_model(name, model, X_train, X_test, y_train, y_test):
    """
    Trains a model and computes performance metrics.
    
    Parameters:
        name (str): Model name.
        model: The machine learning model.
        X_train, X_test, y_train, y_test: Training and testing data.
    Returns:
        Tuple (name, metrics dictionary)
    """
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_test)[:, 1]
    else:
        y_proba = np.zeros_like(y_pred)
    
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred),
        'roc_auc': roc_auc_score(y_test, y_proba),
        'confusion_matrix': confusion_matrix(y_test, y_pred)
    }
    return name, metrics

def train_and_evaluate(df):
    """
    Trains multiple models using stratified k-fold cross-validation and parallel processing.
    
    Parameters:
        df (DataFrame): Normalized and cleaned DataFrame.
    Returns:
        results (dict): Averaged performance metrics for each model.
    """
    X, y = preprocess_data(df)
    
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    # Define models with pipelines and hyperparameter tuning for SVM.
    models = {
        'RandomForest': make_pipeline(StandardScaler(), 
                                     RandomForestClassifier(n_estimators=300, max_depth=12, n_jobs=-1, random_state=42)),
        'GradientBoosting': make_pipeline(StandardScaler(),
                                          GradientBoostingClassifier(n_estimators=200, max_depth=6, learning_rate=0.05, 
                                                                    subsample=0.8, random_state=42)),
        'SVM': make_pipeline(StandardScaler(), SVC(kernel='rbf', probability=True, random_state=42))
    }
    
    # Hyperparameter tuning for SVM using GridSearchCV
    param_grid = {'svc__C': [0.1, 1, 10], 'svc__gamma': ['scale', 'auto']}
    grid_search = GridSearchCV(models['SVM'], param_grid, cv=3, n_jobs=-1)
    grid_search.fit(X, y)
    models['SVM'] = grid_search.best_estimator_
    
    results = {}
    for train_idx, test_idx in skf.split(X, y):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        
        fold_results = Parallel(n_jobs=3)(
            delayed(train_model)(name, model, X_train, X_test, y_train, y_test)
            for name, model in models.items()
        )
        for name, metrics in fold_results:
            if name not in results:
                results[name] = {k: [] for k in metrics.keys()}
            for k, v in metrics.items():
                results[name][k].append(v)
    
    # Average the metrics across folds
    for model in results:
        for metric in results[model]:
            results[model][metric] = np.mean(results[model][metric])
    
    return results