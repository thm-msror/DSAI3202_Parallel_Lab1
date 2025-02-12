from src.data_loader import load_data
from src.preprocessing import split_data
from src.model import train_model
from src.evaluate import evaluate_model
from src.serial_bestParameters import serial_search

# Load data
train_data_cleaned = load_data()

# Preprocess and split data
X_train, X_val, y_train, y_val = split_data(train_data_cleaned)

# Train the model
rf_model = train_model(X_train, y_train)

# Evaluate the model
rmse = evaluate_model(rf_model, X_val, y_val)
print(f'RMSE on the validation data: {rmse:.4f}')

# Run parameter tuning
sequential_time = serial_search(X_train, X_val, y_train, y_val)
