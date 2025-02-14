from src.data_loader import load_data
from src.preprocessing import split_data

def test_split_data():
    """
    Tests whether the data is split into training and validation sets properly.
    """
    data = load_data()
    X_train, X_val, y_train, y_val = split_data(data)

    assert X_train is not None and len(X_train) > 0, "X_train should not be empty"
    assert X_val is not None and len(X_val) > 0, "X_val should not be empty"
    assert y_train is not None and len(y_train) > 0, "y_train should not be empty"
    assert y_val is not None and len(y_val) > 0, "y_val should not be empty"