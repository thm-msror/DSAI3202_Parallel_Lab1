# model_training.py
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

def split_data(dataframe):
    """Splits data into training and testing sets."""
    X = dataframe.drop(columns=['target'])  # Adjust 'target' based on your dataset
    y = dataframe['target']
    return train_test_split(X, y, test_size=0.2, random_state=42)

def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    """Optimized models with hyperparameter tuning and parallel training"""
    models = {
        'RandomForest': make_pipeline(
            StandardScaler(),
            RandomForestClassifier(n_estimators=200, max_depth=10, n_jobs=-1)
        ),
        'SVM': make_pipeline(
            StandardScaler(),
            SVC(kernel='rbf', C=10, gamma='scale', probability=True)
        )
    }
    
    # Parallel grid search for SVM
    param_grid = {
        'svc__C': [0.1, 1, 10],
        'svc__gamma': ['scale', 'auto']
    }
    grid_search = GridSearchCV(models['SVM'], param_grid, cv=3, n_jobs=-1)
    grid_search.fit(X_train, y_train)
    models['SVM'] = grid_search.best_estimator_
    
    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        results[name] = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1': f1_score(y_test, y_pred)
        }
    
    return results