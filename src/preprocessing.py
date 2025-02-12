from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def split_data(train_data_cleaned, test_size=0.30, random_state=42):
    """
    Prepares the dataset by encoding categorical features, 
    splitting into train and validation sets, and handling missing values.
    
    Args:
    train_data_cleaned (pandas.DataFrame): The cleaned dataset.
    test_size (float): The proportion of the dataset to include in the test split.
    random_state (int): Controls the shuffling applied to the data before splitting.
    
    Returns:
    tuple: X_train_filled, X_val_filled, y_train, y_val
    """
    
    # Define the input features (X) and the output (y)
    X = train_data_cleaned.drop('SalePrice', axis=1)
    y = train_data_cleaned['SalePrice']

    # Identify categorical columns
    categorical_columns = X.select_dtypes(include=['object']).columns

    # Encode categorical columns
    label_encoders = {col: LabelEncoder() for col in categorical_columns}
    for col in categorical_columns:
        X[col] = label_encoders[col].fit_transform(X[col])

    # Split the data
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Handle missing values
    X_train_filled = X_train.fillna(X_train.median())
    X_val_filled = X_val.fillna(X_val.median())

    return X_train_filled, X_val_filled, y_train, y_val
