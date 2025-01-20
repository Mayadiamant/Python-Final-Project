import numpy as np
import pandas as pd

def generate_numbers_with_stats(n: int, target_mean: float, target_std: float, min_val: float, max_val: float) -> list:
    """
    Generate a list of numbers with specified statistics.

    Args:
        n (int): Number of values to generate.
        target_mean (float): Target mean of the generated numbers.
        target_std (float): Target standard deviation of the generated numbers.
        min_val (float): Minimum value allowed in the generated list.
        max_val (float): Maximum value allowed in the generated list.

    Returns:
        list: A sorted list of numbers satisfying the given statistics.
    """
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

def split_list(lst: list, size: int) -> tuple:
    """
    Split a list into two parts based on a specified size.

    Args:
        lst (list): The list to split.
        size (int): Number of elements in the first part of the split.

    Returns:
        tuple: Two lists, the first containing 'size' elements, the second containing the rest.
    """
    list1 = lst[:size]
    list2 = lst[size:]
    return list1, list2

def prepare_data_from_csv(data: pd.DataFrame) -> pd.DataFrame:
    """
    Create a new DataFrame summarizing Responders and Non-Responders for each group.

    Args:
        csv_data (pd.DataFrame): The input DataFrame containing the original data.

    Returns:
        pd.DataFrame: A DataFrame summarizing the counts of Responders and Non-Responders for each group.
    """
    # Create a copy of the data to avoid modifying the original
    working_data = data.copy()

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
