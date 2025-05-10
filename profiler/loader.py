import yaml
import os
import pandas as pd

def load_dataset(filepath):
    """
    Load a dataset from a CSV file and return it as a pandas DataFrame. 
    The function checks if the file exists before attempting to load it.
    
    Args:
        filepath (str): The path to the CSV file.
    Returns:
        pd.DataFrame: The loaded dataset.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f'The file {filepath} does not exist')
    
    return pd.read_csv(filepath)

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