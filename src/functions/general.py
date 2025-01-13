import numpy as np

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
    numbers = np.round(numbers, 1)
    
    return sorted(numbers)

def split_list(lst, size):
    list1 = lst[:size]
    list2 = lst[size:]
    return list1, list2