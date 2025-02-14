from sklearn.ensemble import RandomForestRegressor

def train_model(X_train, y_train, n_estimators=100, max_features=None, max_depth=None):
    """
    Trains a RandomForestRegressor on the given training data.

    Args:
    X_train (pandas.DataFrame): The training features.
    y_train (pandas.Series): The training labels.
    n_estimators (int): The number of trees in the forest.
    max_features (str or int or None): The number of features to consider when looking for the best split.
    max_depth (int or None): The maximum depth of the trees.

    Returns:
    RandomForestRegressor: The trained model.
    """
    model = RandomForestRegressor(n_estimators=n_estimators, 
                                  max_features=max_features, 
                                  max_depth=max_depth, 
                                  random_state=42)
    model.fit(X_train, y_train)
    return model
