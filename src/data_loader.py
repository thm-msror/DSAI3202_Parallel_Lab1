import pandas as pd

def load_data():
    # Load the train_dataset
    file_path = 'data/housing_prices_data/train.csv'
    train_data = pd.read_csv(file_path, index_col="Id")

    # Columns to be deleted
    columns_to_delete = ['MoSold', 'YrSold', 'SaleType', 'SaleCondition', 'Alley', 'FireplaceQu', 'PoolQC', 'Fence', 'MiscFeature']

    # Delete the specified columns
    train_data_cleaned = train_data.drop(columns=columns_to_delete, axis=1)

    return train_data_cleaned