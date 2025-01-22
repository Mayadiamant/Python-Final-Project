import numpy as np
import pandas as pd
import sys

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

    Raises:
        ValueError: If 'n' is less than or equal to 0, 'min_val' is greater than or equal to 'max_val', or 'target_std' is 0.
    """
    if n <= 0:
        raise ValueError("Error: 'n' must be a positive integer.")
    if min_val >= max_val:
        raise ValueError("Error: 'min_val' must be less than 'max_val'.")
    if target_std == 0:
        raise ValueError("Error: 'target_std' cannot be zero.")
        
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
    
    Raises:
        TypeError: If 'lst' is not a list.
        ValueError: If 'size' is less than 0 or greater than the length of the list.
        Exception: If an unexpected error occurs during the list splitting process.
    """
    try:
        if not isinstance(lst, list):
            raise TypeError("Error: 'lst' must be a list.")
        if size < 0 or size > len(lst):
            raise ValueError("Error: 'size' must be between 0 and the length of the list.")
        
        list1 = lst[:size]
        list2 = lst[size:]
        return list1, list2
    
    except TypeError as e:
        print(f"TypeError: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"ValueError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

    

def prepare_data_from_csv(data: pd.DataFrame) -> pd.DataFrame:
    """
    Create a new DataFrame summarizing Responders and Non-Responders for each group.

    Args:
        csv_data (pd.DataFrame): The input DataFrame containing the original data.

    Returns:
        pd.DataFrame: A DataFrame summarizing the counts of Responders and Non-Responders for each group.

    Raises:
        TypeError: If 'data' is not a pandas DataFrame.
        KeyError: If 'status' column is missing in the input data.
        ValueError: If 'status' column is empty.
        Exception: If an unexpected error occurs during data processing.
    """
    try:
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Error: 'data' must be a pandas DataFrame.")
        if 'status' not in data.columns:
            raise KeyError("Error: 'status' column is missing in the input data.")
        if data['status'].empty:
            raise ValueError("Error: 'status' column is empty.")
        
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
    
    except TypeError as e:
        print(f"TypeError: {e}")
        sys.exit(1)
    except KeyError as e:
        print(f"KeyError: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"ValueError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
