from src.model import train_model
from src.data_loader import load_data
from src.preprocessing import split_data

def test_train_model():
    """
    Tests whether the RandomForestRegressor is trained correctly.
    """
    data = load_data()
    X_train, X_val, y_train, y_val = split_data(data)

    model = train_model(X_train, y_train, n_estimators=10, max_depth=5, max_features='sqrt')

    assert model is not None, "Model should not be None"
    assert hasattr(model, "predict"), "Model should have a predict method"

    # Ensure the model can make predictions
    predictions = model.predict(X_val)
    assert predictions is not None, "Predictions should not be None"
    assert len(predictions) == len(y_val), "Number of predictions should match number of validation samples"