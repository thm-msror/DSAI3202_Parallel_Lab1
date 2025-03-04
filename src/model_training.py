# Import necessary libraries
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score
from joblib import Parallel, delayed  # For parallel processing
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
    # Remove rows with missing values
    df = df.dropna()
    
    # Check if the target column 'Tumor' exists in the dataframe
    if 'Tumor' not in df.columns:
        raise ValueError("Target column 'Tumor' not found in dataframe!")
    
    # Split the dataframe into features (X) and target (y)
    X = df.drop('Tumor', axis=1)  # Features (all columns except 'Tumor')
    y = df['Tumor']  # Target (only the 'Tumor' column)
    
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
    # Train the model on the training data
    model.fit(X_train, y_train)
    
    # Predict labels for the test data
    y_pred = model.predict(X_test)
    
    # If the model supports probability estimates, compute ROC-AUC
    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_test)[:, 1]  # Probability of the positive class
    else:
        y_proba = np.zeros_like(y_pred)  # Default to zeros if probability is not supported
    
    # Compute performance metrics
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),  # Accuracy
        'precision': precision_score(y_test, y_pred),  # Precision
        'recall': recall_score(y_test, y_pred),  # Recall
        'f1': f1_score(y_test, y_pred),  # F1-Score
        'roc_auc': roc_auc_score(y_test, y_proba),  # ROC-AUC
        'confusion_matrix': confusion_matrix(y_test, y_pred)  # Confusion matrix
    }
    
    # Return the model name and computed metrics
    return name, metrics

def train_and_evaluate(df):
    """
    Trains multiple models using stratified k-fold cross-validation and parallel processing.
    
    Parameters:
        df (DataFrame): Normalized and cleaned DataFrame.
    Returns:
        results (dict): Averaged performance metrics for each model.
    """
    # Preprocess the data: split into features (X) and target (y)
    X, y = preprocess_data(df)
    
    # Initialize StratifiedKFold for cross-validation
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    # Define models with pipelines and hyperparameter tuning for SVM
    models = {
        'RandomForest': make_pipeline(
            StandardScaler(),  # Standardize features
            RandomForestClassifier(n_estimators=300, max_depth=12, n_jobs=-1, random_state=42)
        ),
        'GradientBoosting': make_pipeline(
            StandardScaler(),  # Standardize features
            GradientBoostingClassifier(n_estimators=200, max_depth=6, learning_rate=0.05, 
                                      subsample=0.8, random_state=42)
        ),
        'SVM': make_pipeline(
            StandardScaler(),  # Standardize features
            SVC(kernel='rbf', probability=True, random_state=42)
        )
    }
    
    # Hyperparameter tuning for SVM using GridSearchCV
    param_grid = {'svc__C': [0.1, 1, 10], 'svc__gamma': ['scale', 'auto']}  # Parameters to tune
    grid_search = GridSearchCV(models['SVM'], param_grid, cv=3, n_jobs=-1)  # 3-fold cross-validation
    grid_search.fit(X, y)  # Fit the GridSearchCV to find the best parameters
    models['SVM'] = grid_search.best_estimator_  # Update the SVM model with the best estimator
    
    # Initialize a dictionary to store results
    results = {}
    
    # Perform cross-validation
    for train_idx, test_idx in skf.split(X, y):
        # Split the data into training and testing sets for this fold
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        
        # Train models in parallel using joblib
        fold_results = Parallel(n_jobs=2)(  # Use 2 parallel jobs
            delayed(train_model)(name, model, X_train, X_test, y_train, y_test)  # Train each model
            for name, model in models.items()
        )
        
        # Aggregate results for this fold
        for name, metrics in fold_results:
            if name not in results:
                results[name] = {k: [] for k in metrics.keys()}  # Initialize metrics dictionary
            for k, v in metrics.items():
                results[name][k].append(v)  # Append metrics for this fold
    
    # Average the metrics across folds, except for the confusion matrix
    for model in results:
        for metric in results[model]:
            if metric == 'confusion_matrix':
                # Sum the confusion matrices across folds
                results[model][metric] = np.sum(results[model][metric], axis=0)
            else:
                # Average other metrics (accuracy, precision, recall, etc.)
                results[model][metric] = np.mean(results[model][metric])
    
    # Return the final results
    return results