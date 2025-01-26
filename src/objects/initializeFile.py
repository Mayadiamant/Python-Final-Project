import numpy as np
import pandas as pd
import sys
sys.path.append(r'C:/Users/matan/OneDrive/שולחן העבודה/python/project/src/objects')
sys.path.append(r'C:/Users/matan/OneDrive/שולחן העבודה/python/project/src/functions')
from functions.general import (
    generate_numbers_with_stats,
    split_list
)

class InitializeFile():
    """
    This class initializes and processes a dataset by loading data from a CSV file,
    generating synthetic data, and creating new columns in the dataset.

    Attributes:
        file (pd.DataFrame): The processed dataset.
    """

    def __init__(self):
        """
        Initializes the class by loading a dataset and augmenting it with synthetic data.

        Steps:
            1. Load the dataset from a CSV file.
            2. Generate synthetic data based on specified parameters.
            3. Add new columns to the dataset.

        Raises:
            FileNotFoundError: If the CSV file is not found.
            pd.errors.EmptyDataError: If the CSV file is empty.
            pd.errors.ParserError: If the file format is invalid.
            Exception: For other general errors while loading the file.
            ValueError: If the generated synthetic data lengths do not match the dataset.
            Exception: For general errors during column addition.
        """
        try:
            file = pd.read_csv(r"C:\Users\matan\OneDrive\מסמכים\data set.csv")
            print("File uploaded successfully!")
        except FileNotFoundError:
            print("Error: File not found. Check the path.")
            sys.exit(1)
        except pd.errors.EmptyDataError:
            print("Error: The file is empty.")
            sys.exit(1)
        except pd.errors.ParserError:
            print("Error: There was a problem with the file format.")
            sys.exit(1)
        except PermissionError:
            print("Error: Permission to read file denied")
            sys.exit(1)
        except Exception as e:
            print(f"General error: {e}")
            sys.exit(1)
        # Generate numbers 
        # Partially based on means and standard deviation based on data extraction from graphs
        np.random.seed(42)  # In order to get the same data every run
        age = generate_numbers_with_stats(78, 20.37, 2.37, 18, 35)
        BMI_HC = generate_numbers_with_stats(36, 22.15, 3.98, 13, 33)
        BMI_NC = generate_numbers_with_stats(42, 21.78, 2.71, 13, 33)
        responders_images_sAA_level_HC = generate_numbers_with_stats(17, 33.5, 10, 10, 50)
        responders_images_sAA_level_NC = generate_numbers_with_stats(22, 55, 15, 30, 68)
        nonresponders_images_sAA_level_HC = generate_numbers_with_stats(19, -45, 8, -50, -40)
        nonresponders_images_sAA_level_NC = generate_numbers_with_stats(20, -17, 4, -22, -15)
        responders_images_sAA_level_HC_baseline = generate_numbers_with_stats(17, 70, 10, 60, 80)
        responders_images_sAA_level_NC_baseline = generate_numbers_with_stats(22, 135, 10, 125, 145)
        nonresponders_images_sAA_level_HC_baseline = generate_numbers_with_stats(19, 175, 10, 165, 185)
        nonresponders_images_sAA_level_NC_baseline = generate_numbers_with_stats(20, 120, 10, 110, 130)
        responders_CPS_corisol_level_HC = generate_numbers_with_stats(9 , 0.2, 0.1, 0, 0.4)
        responders_CPS_cortisol_level_NC = generate_numbers_with_stats(17, 0.25, 0.15, 0, 0.4)
        nonresponders_CPS_cortisol_level_HC = generate_numbers_with_stats(14 , -0.03, 0.05, -0.08, 0)
        nonresponders_CPS_cortisol_level_NC = generate_numbers_with_stats(7 , -0.007, 0.005, -0.08, 0)
        responders_CPS_corisol_level_HC_baseline = generate_numbers_with_stats(9 , 0.075, 0.05, 0, 0.3)
        responders_CPS_cortisol_level_NC_baseline = generate_numbers_with_stats(17 , 0.135, 0.08, 0, 0.3)
        nonresponders_CPS_cortisol_level_HC_baseline = generate_numbers_with_stats(14 , 0.23, 0.2, 0, 0.3)
        nonresponders_CPS_cortisol_level_NC_baseline = generate_numbers_with_stats(7 , 0.123, 0.105, 0, 0.3)
        control_nonresponders_cortisol_NC_baseline = generate_numbers_with_stats(18, 0.123, 0.05, 0, 0.3)
        control_nonresponders_cortisol_HC_baseline = generate_numbers_with_stats(13, 0.23, 0.15, 0, 0.3)
        control_nonresponders_cortisol_NC = generate_numbers_with_stats(18, -0.007, 0.1, -0.08, 0)
        control_nonresponders_cortisol_HC = generate_numbers_with_stats(13, -0.03,0.1,-0.08, 0)
        responders_positive_image_CPS_HC = generate_numbers_with_stats(10 , 2.8, 0.1, 2.7, 2.8)
        responders_positive_image_CPS_NC = generate_numbers_with_stats(12 , 2.6, 0.1, 2.5, 2.7)
        responders_positive_image_control_HC = generate_numbers_with_stats(7 , 1.2, 0.05, 1.15, 1.25)
        responders_positive_image_control_NC = generate_numbers_with_stats(10 , 2.2, 0.1, 2.1, 2.3)
        nonresponders_positive_image_CPS_HC = generate_numbers_with_stats(13 , 3.4, 0.03, 3.37, 3.43)
        nonresponders_positive_image_CPS_NC = generate_numbers_with_stats(12 , 2.7, 0.15, 2.55, 2.85)
        nonresponders_positive_image_control_HC = generate_numbers_with_stats(6 , 1.05, 0.1, 0.95, 1.15)
        nonresponders_positive_image_control_NC = generate_numbers_with_stats(8 , 2.9, 0.1, 2.8, 3)
        responders_negative_image_CPS_HC = generate_numbers_with_stats(10 , 2.9, 0.15, 2.75, 3.05)
        responders_negative_image_CPS_NC = generate_numbers_with_stats(12 , 3.4, 0.08, 3.32, 3.48)
        responders_negative_image_control_HC = generate_numbers_with_stats(7, 4.7, 0.02, 4.68, 4.72)
        responders_negative_image_control_NC = generate_numbers_with_stats(10, 3.2, 0.1, 3.1, 3.3)
        nonresponders_negative_image_CPS_HC = generate_numbers_with_stats(13 , 4, 0.3, 3.7, 4.3)
        nonresponders_negative_image_CPS_NC = generate_numbers_with_stats(12 , 3.2, 0.15, 3.05, 3.35)
        nonresponders_negative_image_control_HC = generate_numbers_with_stats(6 , 3, 0.2, 2.8, 3.2)
        nonresponders_negative_image_control_NC = generate_numbers_with_stats(8 , 2.9, 0.1, 2.8, 3)

        # Split lists
        part_one_responders_CPS_cortisol_level_NC_baseline , part_two_responders_CPS_cortisol_level_NC_baseline = split_list(responders_CPS_cortisol_level_NC_baseline, 12)
        part_one_nonresponders_CPS_cortisol_level_HC_baseline , part_two_nonresponders_CPS_cortisol_level_HC_baseline = split_list(nonresponders_CPS_cortisol_level_HC_baseline, 1)
        part_one_responders_CPS_cortisol_level_NC , part_two_responders_CPS_cortisol_level_NC = split_list(responders_CPS_cortisol_level_NC, 12)
        part_one_nonresponders_CPS_cortisol_level_HC , part_two_nonresponders_CPS_cortisol_level_HC = split_list(nonresponders_CPS_cortisol_level_HC, 1)
        part_one_control_nonresponders_cortisol_level_HC, part_two_control_nonresponders_cortisol_level_HC = split_list(control_nonresponders_cortisol_HC, 7)
        part_one_control_nonresponders_cortisol_level_NC, part_two_control_nonresponders_cortisol_level_NC = split_list(control_nonresponders_cortisol_NC, 10)
        part_one_control_nonresponders_cortisol_level_HC_baseline, part_two_control_nonresponders_cortisol_level_HC_baseline = split_list(control_nonresponders_cortisol_HC_baseline, 7)
        part_one_control_nonresponders_cortisol_level_NC_baseline, part_two_control_nonresponders_cortisol_level_NC_baseline = split_list(control_nonresponders_cortisol_NC_baseline, 10)
        
        try:
            # Augment the dataset
            file['age'] = age
            file['BMI'] = BMI_NC + BMI_HC 
            file['sAA_level_baseline'] = responders_images_sAA_level_NC_baseline + nonresponders_images_sAA_level_NC_baseline + responders_images_sAA_level_HC_baseline + nonresponders_images_sAA_level_HC_baseline
            file['change_image_sAA_level'] = responders_images_sAA_level_NC + nonresponders_images_sAA_level_NC + responders_images_sAA_level_HC + nonresponders_images_sAA_level_HC
            file['cortisol_level_baseline'] = part_one_responders_CPS_cortisol_level_NC_baseline+ part_one_control_nonresponders_cortisol_level_NC_baseline+ part_two_responders_CPS_cortisol_level_NC_baseline + nonresponders_CPS_cortisol_level_NC_baseline + part_two_control_nonresponders_cortisol_level_NC_baseline + responders_CPS_corisol_level_HC_baseline + part_one_nonresponders_CPS_cortisol_level_HC_baseline + part_one_control_nonresponders_cortisol_level_HC_baseline + part_two_nonresponders_CPS_cortisol_level_HC_baseline + part_two_control_nonresponders_cortisol_level_HC_baseline
            file['change_CPS_cortisol_level'] =  part_one_responders_CPS_cortisol_level_NC+ part_one_control_nonresponders_cortisol_level_NC+ part_two_responders_CPS_cortisol_level_NC + nonresponders_CPS_cortisol_level_NC + part_two_control_nonresponders_cortisol_level_NC + responders_CPS_corisol_level_HC + part_one_nonresponders_CPS_cortisol_level_HC + part_one_control_nonresponders_cortisol_level_HC + part_two_nonresponders_CPS_cortisol_level_HC + part_two_control_nonresponders_cortisol_level_HC
            file['positive_image'] = responders_positive_image_CPS_NC + responders_positive_image_control_NC + nonresponders_positive_image_CPS_NC + nonresponders_positive_image_control_NC + responders_positive_image_CPS_HC + responders_positive_image_control_HC + nonresponders_positive_image_CPS_HC + nonresponders_positive_image_control_HC
            file['negative_image'] = responders_negative_image_CPS_NC + responders_negative_image_control_NC + nonresponders_negative_image_CPS_NC + nonresponders_negative_image_control_NC + responders_negative_image_CPS_HC + responders_negative_image_control_HC + nonresponders_negative_image_CPS_HC + nonresponders_negative_image_control_HC
            self.file = file
            print("Columns added successfully!")
        except PermissionError:
            print("Error: Permission to write into the file denied")
            sys.exit(1) 
        except Exception as e:
            print(f"Error while adding columns: {e}")
            sys.exit(1)
       
       
        