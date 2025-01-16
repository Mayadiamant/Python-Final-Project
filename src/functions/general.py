import numpy as np
import pandas as pd

def generate_numbers_with_stats(n, target_mean, target_std, min_val, max_val):
    # Start with normal distribution
    numbers = np.random.normal(target_mean, target_std, n-2)
    
    # Clip to range and add endpoints
    numbers = np.clip(numbers, min_val, max_val)
    numbers = np.append(numbers, [min_val, max_val])
    
    # Adjust to get target mean
    current_mean = np.mean(numbers)
    adjustment = target_mean - current_mean
    numbers = numbers + adjustment
    
    # Adjust to get target std
    current_std = np.std(numbers)
    scale_factor = target_std / current_std
    numbers = (numbers - target_mean) * scale_factor + target_mean
    
    # Final clip and round
    numbers = np.clip(numbers, min_val, max_val)
    numbers = np.round(numbers, 2)
    
    return sorted(numbers)

def split_list(lst, size):
    list1 = lst[:size]
    list2 = lst[size:]
    return list1, list2

def prepare_data_from_csv(csv_data: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a new DataFrame summarizing Responders and Non-Responders for each group,
    including control-non-responders in the Non-Responders count.
    """
    # Create a copy of the data to avoid modifying the original
    working_data = csv_data.copy()
    
    # Create empty DataFrame for results
    result = pd.DataFrame()
    
    # Process each group (HC, NC)
    for status in working_data['status'].unique():
        group_data = working_data[working_data['status'] == status]
        
        # Count responders (only CPS condition)
        responders = len(group_data[
            (group_data['stress_test_condition'] == 'cps') & 
            (group_data['responsive_state_cortisol'] == 'responders')
        ])
        
        # Count non-responders (including both CPS and control conditions)
        non_responders = len(group_data[
            ((group_data['stress_test_condition'] == 'cps') & 
             (group_data['responsive_state_cortisol'] == 'non-responders')) |
            (group_data['responsive_state_cortisol'] == 'control-non-responders')
        ])
        
        # Add new row to result DataFrame
        new_row = pd.DataFrame({
            'Group': [status],
            'Responders': [responders],
            'Non-Responders': [non_responders]
        })
        result = pd.concat([result, new_row], ignore_index=True)
    
    # Sort to ensure HC comes before NC
    result = result.sort_values('Group', ascending=True).reset_index(drop=True)
    return result
