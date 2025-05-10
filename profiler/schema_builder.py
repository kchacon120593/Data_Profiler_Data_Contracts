import pandas as pd
from typing import Dict, List
import pandera as pa
from pandera import Column, DataFrameSchema, Check
from datetime import datetime

    
type_mapping = {
          'int': pa.Int
        , 'float': pa.Float
        , 'string': pa.String
        , 'bool': pa.Bool
        , 'datetime': pa.DateTime
        , 'date': pa.Date
        }


def build_schema(contract: dict):
    """
    Build a Pandera DataFrameSchema based on field definitions in a contract.
    This includes type and nullability checks only.

    Args:
        contract (dict): The parsed YAML contract.

    Returns:
        DataFrameSchema: The built schema object.
    """
    # Initialize an empty list to hold the column definitions
    field_definitions = contract.get('fields', [])
    
    schema_columns = {}

    
    # Iterate over each field definition in the contract
    
    for field in field_definitions:
        field_name =  field['name']
        field_type = type_mapping.get(field['type'], pa.String)  # default to string
        nullable = field.get('nullable', True)

        
        schema_columns[field_name] = Column(
             dtype= field_type
           , nullable=nullable
           , required= True  # assumes all defined fields are required in the schema
           )
       
    return DataFrameSchema(schema_columns)   
   
def validate_schema(df: pd.DataFrame, contract: Dict):

    """
    Validate the dataframe using a schema based on the data contract.
    Captures schema violations and enriches them with 'schema_check' rule metadata.

    Args:
        df (pd.DataFrame): The dataset to validate.
        contract (dict): The full parsed data contract.

    Returns:
        List[Dict]: List of schema violations with severity details.
    """
    # Build the schema from the contract
    schema = build_schema(contract)
    
    # Get schema_check rules from the contract
    rules = contract.get('rules', [])
    
    schema_rule = next((rule for rule in rules if rule.get("type") == "schema_check"), {})
    
    severity = schema_rule.get("severity", "high")
    severity_points = schema_rule.get("severity_points", 5)
    
    try:
        schema.validate(df, lazy=True)
        return []  # ✅ Schema passed
    
    except pa.errors.SchemaErrors as e:
        violations = []

        # Loop over the rows in the failure_cases DataFrame
        for _, row in e.failure_cases.iterrows():
            violations.append({
                "rule": "schema_check",
                "column": row.get("column"),
                "check": row.get("check"),
                "failed_value": row.get("failure_case"),
                "error": row.get("error"),
                "severity": severity,
                "severity_points": severity_points,
                "message": f"{row.get('check')} failed on column {row.get('column')}: {row.get('failure_case')}",
                "timestamp": datetime.now().isoformat()
            })

        return violations
    