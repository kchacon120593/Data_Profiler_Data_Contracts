import yaml
import os
import pandas as pd

def load_dataset(filepath, datetime_columns=None):
    """
    Load a dataset from a CSV file and return it as a pandas DataFrame. 
    The function checks if the file exists before attempting to load it.
    
    Args:
        filepath (str): The path to the CSV file.
        datetime_columns (list, optional): List of columns to convert to datetime. 
                                            If None, no conversion is done.
    Returns:
        pd.DataFrame: The loaded dataset.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'The file {filepath} does not exist')
    
    df = pd.read_csv(filepath)
    # Check for datetime columns in the dataset
    if datetime_columns:
        for col in datetime_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
    
    return df

def load_contract(filepath):
    """
    Load a contract from a YAML file and return it as a dictionary. 
    The function checks if the file exists before attempting to load it.
    
    Args:
        filepath (str): The path to the YAML file.
    Returns:
        dict: The loaded contract.
    """   
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'The file {filepath} does not exist')
    
    with open(filepath, 'r') as file:
        return yaml.safe_load(file)