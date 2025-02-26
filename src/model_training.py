# model_training.py
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

def split_data(dataframe):
    """
    Splits the DataFrame into features (X) and target (y) and further splits into training and testing sets.

    Parameters:
        - dataframe: A pandas DataFrame containing the GLCM features and target.

    Returns:
        - X_train, X_test, y_train, y_test: Training and testing sets.
    """
    X = dataframe.drop(columns=['Tumor'])
    y = dataframe['Tumor']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    return X_train, X_test, y_train, y_test

def train_and_evaluate_model(model_name, model, X_train, X_test, y_train, y_test):
    """
    Trains and evaluates a single machine learning model.

    Parameters:
        - model_name: Name of the model.
        - model: The machine learning model.
        - X_train, X_test, y_train, y_test: Training and testing sets.

    Returns:
        - model_name: Name of the model.
        - metrics: A dictionary containing the evaluation metrics.
    """
    # Train the model
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    conf_matrix = confusion_matrix(y_test, y_pred)

    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'confusion_matrix': conf_matrix
    }
    return model_name, metrics

def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    """
    Trains and evaluates multiple machine learning models in parallel.

    Parameters:
        - X_train, X_test, y_train, y_test: Training and testing sets.

    Returns:
        - results: A dictionary containing the evaluation metrics for each model.
    """
    # Define the models
    models = {
        'Random Forest': RandomForestClassifier(random_state=42),
        'SVM': SVC(random_state=42),
        # Add a third model if needed
    }

    results = {}
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(train_and_evaluate_model, model_name, model, X_train, X_test, y_train, y_test)
            for model_name, model in models.items()
        ]
        for future in as_completed(futures):
            model_name, metrics = future.result()
            results[model_name] = metrics

    return results