from sklearn.ensemble import RandomForestRegressor

def train_model(X_train, y_train):
    """
    Trains a RandomForestRegressor on the given training data.

    Args:
    X_train (pandas.DataFrame): The training features.
    y_train (pandas.Series): The training labels.

    Returns:
    RandomForestRegressor: The trained model.
    """
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)
    return model