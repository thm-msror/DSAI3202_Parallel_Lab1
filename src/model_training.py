from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def split_data(dataframe):
    """
    Splits the DataFrame into features (X) and target (y) and further splits into training and testing sets.

    Parameters:
        - dataframe: A pandas DataFrame containing the GLCM features and target.

    Returns:
        - X_train, X_test, y_train, y_test: Training and testing sets.
    """
    X = dataframe.drop(columns=['Tumor'])  # Use 'Tumor' instead of 'target'
    y = dataframe['Tumor']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    return X_train, X_test, y_train, y_test

def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    """Trains and evaluates multiple machine learning models."""
    models = {
        'RandomForest': RandomForestClassifier(n_estimators=200, max_depth=10, n_jobs=-1),
        'SVM': SVC(kernel='rbf', C=10, gamma='scale', probability=True)
    }
    
    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        results[name] = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred),
            'recall': recall_score(y_test, y_pred),
            'f1': f1_score(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred)
        }
    
    return results