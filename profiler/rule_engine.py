""" Rule Engine for Data Validation """



def get_contract_rules(contract: dict):
    """
    Extract rules from the contract and return them as a list of dictionaries.
    
    Args:
        contract (dict): The parsed YAML contract.
    
    Returns:
        List[Dict]: A list of rules extracted from the contract.
    """
    # Extract rules from the contract
    rules = contract.get('rules', [])
    
    # Filter out rules that are not relevant
    relevant_rules = [rule for rule in rules if rule.get("type") != "schema_check"]
    
    return relevant_rules

def validate_rules(df, relevant_rules):
    """
    validate the dataset against the rules defined in the contract.
    Args:
        df (pd.DataFrame): The dataset to validate.
        relevant_rules (List[Dict]): A list of rules extracted from the contract.   
    Returns:
        List[Dict]: A list of violations found in the dataset. 
    
    """
    
    violations = []
    
    # Iterate over each rule and validate it    
    for rule in relevant_rules:
        rule_type = rule.get("type")
        severity = rule.get("severity", "high")
        severity_points = rule.get("severity_points", 5)
        fields = rule.get("fields", [])
        

        # Add additional validation logic here if needed
        
        if rule_type == "range_check":

            min_value = rule.get("min_value")
            max_value = rule.get("max_value")
                        
            for field in fields:      
                # Check if the values are within the specified range
                if min_value is not None and df[field].min() < min_value:
                    # Add the violation to the list
                    violations.append({
                        "field": field,
                        "rule": rule_type,
                        "severity": severity,
                        "severity_points": severity_points,
                        "min_value": min_value,
                        "max_value": max_value,
                        "actual_value": df[field].min()
                    })
                    
                # Check if the values are within the specified range
                if max_value is not None and df[field].max() > max_value:
                    # Add the violation to the list
                    violations.append({
                        "field": field,
                        "rule": rule_type,
                        "severity": severity,
                        "severity_points": severity_points,
                        "min_value": min_value,
                        "max_value": max_value,
                        "actual_value": df[field].max()
                    })
        elif rule_type == "regex_check":
            regex = rule.get("regex")
            
            for field in fields:
                # Check if the values match the specified regex
                if not df[field].str.match(regex).all():
                    # Add the violation to the list
                    violations.append({
                        "field": field,
                        "rule": rule_type,
                        "severity": severity,
                        "severity_points": severity_points,
                        "regex": regex,
                        "actual_value": df[field][~df[field].str.match(regex)]
                    })
                    
        elif rule_type == "null_check":
            for field in fields:
                # Check if the values are null
                if df[field].isnull().any():
                    # Add the violation to the list
                    violations.append({
                        "field": field,
                        "rule": rule_type,
                        "severity": severity,
                        "severity_points": severity_points,
                        "actual_value": df[field][df[field].isnull()]
                    })
                    
    return violations
