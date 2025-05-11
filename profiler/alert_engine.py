def get_contract_alerts(contract: dict):
    """
    Extract alerts from the contract and return them as a list of dictionaries.
    
    Args:
        contract (dict): The parsed YAML contract.
    
    Returns:
        List[Dict]: A list of alerts extracted from the contract.
    """
    # Extract alerts from the contract
    alerts = contract.get('alerts', [])
    
    # Filter out alerts that are not relevant
    relevant_alerts = [alert for alert in alerts]
    
    return relevant_alerts

def validate_alerts(df,contract, relevant_alerts):
    """
    Validate the dataset against the alerts defined in the contract.
    
    Args:
        df (pd.DataFrame): The dataset to validate.
        relevant_alerts (List[Dict]): A list of alerts extracted from the contract.   
    
    Returns:
        List[Dict]: A list of alerts found in the dataset. 
    """
    
    alerts = []
    
    # Iterate over each alert and validate it    
    for alert in relevant_alerts:
        alert_type = alert.get("type")
        severity = alert.get("severity", "high")
        
        
        if alert_type == "completeness_check":
            fields = alert.get("fields", [])
            
            threshold = alert.get("threshold")
            
            # Check if the fields are complete
            for field in fields:      
                
                # Check if the field null ratio is above the threshold
                null_ratio = df[field].isnull().mean()
                if null_ratio > threshold:
                    # Add the alert to the list
                    alerts.append({
                        "field": field,
                        "alert": alert_type,
                        "severity": severity,
                        "column": field,
                        "threshold": threshold,
                        "null_ratio": null_ratio,
                    })              
                
        
        elif alert_type == "tag_check":
            fields = alert.get("fields", [])
            tags = alert.get("tags", [])
            # Check if the fields have the specified tags
            
            for field in fields:      
                # Check if the field has the specified tags
                field_meta = next((f for f in contract.get('fields', []) if f['name'] == field), None)
                if field_meta:
                    for tag in tags:
                        if tag == 'pii' and not field_meta.get('pii', False):
                            # Add the alert to the list
                            alerts.append({
                                "field": field,
                                "alert": alert_type,
                                "severity": severity,
                                "column": field,
                                "tags": tags,
                    })
            

    
    return alerts