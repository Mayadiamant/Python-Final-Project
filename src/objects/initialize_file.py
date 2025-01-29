"""Module for demonstrating how to handle system-level operations."""
import sys

import numpy as np
import pandas as pd

sys.path.append(r"C:/Users/matan/OneDrive/שולחן העבודה/python/project/src")
sys.path.append(r"C:/Users/matan/OneDrive/שולחן העבודה/python/project/src/objects")
sys.path.append(r"C:/Users/matan/OneDrive/שולחן העבודה/python/project/src/functions")
from functions.general import generate_numbers_with_stats, split_list


class InitializeFile:
    """This class initializes and processes a dataset by loading data from a CSV file,

    generating synthetic data, and creating new columns in the dataset.

    Attributes:
        file (pd.DataFrame): The processed dataset.
    """

    def __init__(self) -> None:
        """Initializes the class by loading a dataset and augmenting it with synthetic data.

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
        except FileNotFoundError as err:
            msg = "Error: File not found. Check the path."
            raise FileNotFoundError(msg) from err
        except pd.errors.EmptyDataError as err:
            msg = "Error: The file is empty."
            raise ValueError(msg) from err
        except pd.errors.ParserError as err:
            msg = "Error: There was a problem with the file format."
            raise ValueError(msg) from err
        except PermissionError as err:
            msg = "Error: Permission to read file denied."
            raise PermissionError(msg) from err
        except Exception as e:
            msg = f"General error: {e}"
            raise RuntimeError(msg) from e

        # Generate numbers
        # Partially based on means and standard deviation based on data extraction from graphs
        np.random.seed(42)  # In order to get the same data every run
        age = generate_numbers_with_stats(78, 20.37, 2.37, 18, 35)
        bmi_hc = generate_numbers_with_stats(36, 22.15, 3.98, 13, 33)
        bmi_nc = generate_numbers_with_stats(42, 21.78, 2.71, 13, 33)
        responders_images_saa_level_hc = generate_numbers_with_stats(17, 33.5, 10, 10, 50)
        responders_images_saa_level_nc = generate_numbers_with_stats(22, 55, 15, 30, 68)
        nonresponders_images_saa_level_hc = generate_numbers_with_stats(19, -45, 8, -50, -40)
        nonresponders_images_saa_level_nc = generate_numbers_with_stats(20, -17, 4, -22, -15)
        responders_images_saa_level_hc_baseline = generate_numbers_with_stats(17, 70, 10, 60, 80)
        responders_images_saa_level_nc_baseline = generate_numbers_with_stats(22, 135, 10, 125, 145)
        nonresponders_images_saa_level_hc_baseline = generate_numbers_with_stats(19, 175, 10, 165, 185)
        nonresponders_images_saa_level_nc_baseline = generate_numbers_with_stats(20, 120, 10, 110, 130)
        responders_cps_corisol_level_hc = generate_numbers_with_stats(9 , 0.2, 0.1, 0, 0.4)
        responders_cps_cortisol_level_nc = generate_numbers_with_stats(17, 0.25, 0.15, 0, 0.4)
        nonresponders_cps_cortisol_level_hc = generate_numbers_with_stats(14 , -0.03, 0.05, -0.08, 0)
        nonresponders_cps_cortisol_level_nc = generate_numbers_with_stats(7 , -0.007, 0.005, -0.08, 0)
        responders_cps_corisol_level_hc_baseline = generate_numbers_with_stats(9 , 0.075, 0.05, 0, 0.3)
        responders_cps_cortisol_level_nc_baseline = generate_numbers_with_stats(17 , 0.135, 0.08, 0, 0.3)
        nonresponders_cps_cortisol_level_hc_baseline = generate_numbers_with_stats(14 , 0.23, 0.2, 0, 0.3)
        nonresponders_cps_cortisol_level_nc_baseline = generate_numbers_with_stats(7 , 0.123, 0.105, 0, 0.3)
        control_nonresponders_cortisol_nc_baseline = generate_numbers_with_stats(18, 0.123, 0.05, 0, 0.3)
        control_nonresponders_cortisol_hc_baseline = generate_numbers_with_stats(13, 0.23, 0.15, 0, 0.3)
        control_nonresponders_cortisol_nc = generate_numbers_with_stats(18, -0.007, 0.1, -0.08, 0)
        control_nonresponders_cortisol_hc = generate_numbers_with_stats(13, -0.03,0.1,-0.08, 0)
        responders_positive_image_cps_hc = generate_numbers_with_stats(10 , 2.8, 0.1, 2.7, 2.8)
        responders_positive_image_cps_nc = generate_numbers_with_stats(12 , 2.6, 0.1, 2.5, 2.7)
        responders_positive_image_control_hc = generate_numbers_with_stats(7 , 1.2, 0.05, 1.15, 1.25)
        responders_positive_image_control_nc = generate_numbers_with_stats(10 , 2.2, 0.1, 2.1, 2.3)
        nonresponders_positive_image_cps_hc = generate_numbers_with_stats(13 , 3.4, 0.03, 3.37, 3.43)
        nonresponders_positive_image_cps_nc = generate_numbers_with_stats(12 , 2.7, 0.15, 2.55, 2.85)
        nonresponders_positive_image_control_hc = generate_numbers_with_stats(6 , 1.05, 0.1, 0.95, 1.15)
        nonresponders_positive_image_control_nc = generate_numbers_with_stats(8 , 2.9, 0.1, 2.8, 3)
        responders_negative_image_cps_hc = generate_numbers_with_stats(10 , 2.9, 0.15, 2.75, 3.05)
        responders_negative_image_cps_nc = generate_numbers_with_stats(12 , 3.4, 0.08, 3.32, 3.48)
        responders_negative_image_control_hc = generate_numbers_with_stats(7, 4.7, 0.02, 4.68, 4.72)
        responders_negative_image_control_nc = generate_numbers_with_stats(10, 3.2, 0.1, 3.1, 3.3)
        nonresponders_negative_image_cps_hc = generate_numbers_with_stats(13 , 4, 0.3, 3.7, 4.3)
        nonresponders_negative_image_cps_nc = generate_numbers_with_stats(12 , 3.2, 0.15, 3.05, 3.35)
        nonresponders_negative_image_control_hc = generate_numbers_with_stats(6 , 3, 0.2, 2.8, 3.2)
        nonresponders_negative_image_control_nc = generate_numbers_with_stats(8 , 2.9, 0.1, 2.8, 3)

        # Split lists
        part_one_responders_cps_cortisol_level_nc_baseline , part_two_responders_cps_cortisol_level_nc_baseline = split_list(responders_cps_cortisol_level_nc_baseline, 12)
        part_one_nonresponders_cps_cortisol_level_hc_baseline , part_two_nonresponders_cps_cortisol_level_hc_baseline = split_list(nonresponders_cps_cortisol_level_hc_baseline, 1)
        part_one_responders_cps_cortisol_level_nc , part_two_responders_cps_cortisol_level_nc = split_list(responders_cps_cortisol_level_nc, 12)
        part_one_nonresponders_cps_cortisol_level_hc , part_two_nonresponders_cps_cortisol_level_hc = split_list(nonresponders_cps_cortisol_level_hc, 1)
        part_one_control_nonresponders_cortisol_level_hc, part_two_control_nonresponders_cortisol_level_hc = split_list(control_nonresponders_cortisol_hc, 7)
        part_one_control_nonresponders_cortisol_level_nc, part_two_control_nonresponders_cortisol_level_nc = split_list(control_nonresponders_cortisol_nc, 10)
        part_one_control_nonresponders_cortisol_level_hc_baseline, part_two_control_nonresponders_cortisol_level_hc_baseline = split_list(control_nonresponders_cortisol_hc_baseline, 7)
        part_one_control_nonresponders_cortisol_level_nc_baseline, part_two_control_nonresponders_cortisol_level_nc_baseline = split_list(control_nonresponders_cortisol_nc_baseline, 10)

        try:
            # Augment the dataset
            file["age"] = age
            file["BMI"] = bmi_nc + bmi_hc
            file["sAA_level_baseline"] = responders_images_saa_level_nc_baseline + nonresponders_images_saa_level_nc_baseline + responders_images_saa_level_hc_baseline + nonresponders_images_saa_level_hc_baseline
            file["change_image_sAA_level"] = responders_images_saa_level_nc + nonresponders_images_saa_level_nc + responders_images_saa_level_hc + nonresponders_images_saa_level_hc
            file["cortisol_level_baseline"] = part_one_responders_cps_cortisol_level_nc_baseline+ part_one_control_nonresponders_cortisol_level_nc_baseline+ part_two_responders_cps_cortisol_level_nc_baseline + nonresponders_cps_cortisol_level_nc_baseline + part_two_control_nonresponders_cortisol_level_nc_baseline + responders_cps_corisol_level_hc_baseline + part_one_nonresponders_cps_cortisol_level_hc_baseline + part_one_control_nonresponders_cortisol_level_hc_baseline + part_two_nonresponders_cps_cortisol_level_hc_baseline + part_two_control_nonresponders_cortisol_level_hc_baseline
            file["change_CPS_cortisol_level"] =  part_one_responders_cps_cortisol_level_nc+ part_one_control_nonresponders_cortisol_level_nc+ part_two_responders_cps_cortisol_level_nc + nonresponders_cps_cortisol_level_nc + part_two_control_nonresponders_cortisol_level_nc + responders_cps_corisol_level_hc + part_one_nonresponders_cps_cortisol_level_hc + part_one_control_nonresponders_cortisol_level_hc + part_two_nonresponders_cps_cortisol_level_hc + part_two_control_nonresponders_cortisol_level_hc
            file["positive_image"] = responders_positive_image_cps_nc + responders_positive_image_control_nc + nonresponders_positive_image_cps_nc + nonresponders_positive_image_control_nc + responders_positive_image_cps_hc + responders_positive_image_control_hc + nonresponders_positive_image_cps_hc + nonresponders_positive_image_control_hc
            file["negative_image"] = responders_negative_image_cps_nc + responders_negative_image_control_nc + nonresponders_negative_image_cps_nc + nonresponders_negative_image_control_nc + responders_negative_image_cps_hc + responders_negative_image_control_hc + nonresponders_negative_image_cps_hc + nonresponders_negative_image_control_hc
            self.file = file
            print("Columns added successfully!")
        except PermissionError as err:
            msg = "Error: Permission to write into the file denied."
            raise PermissionError(msg) from err
        except Exception as e:
            msg = f"Error while adding columns: {e}"
            raise RuntimeError(msg) from e
