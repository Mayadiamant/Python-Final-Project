"""This module initializes and processes data for visualization.

It includes:
- Data manipulation using NumPy
- Plotting functionalities with Matplotlib
- File handling using InitializeFile
"""
import matplotlib.pyplot as plt
import numpy as np
import panda as pd

from src.objects.initialize_file import InitializeFile


def article_test(data: pd.DataFrame) -> None:
    """Generate bar plots to visualize the sAA responses for different groups of women.

    Parameters:
        data (pd.DataFrame): The DataFrame containing the required data with a column "change_image_sAA_level".

    Returns:
        None: The function generates plots and does not return a value.

    The function creates two bar plots:
    1. sAA Responders: Comparing the mean sAA change for HC and NC women who are responders.
    2. sAA Non-Responders: Comparing the mean sAA change for HC and NC women who are non-responders.
    """
    # Define groups for responders and non-responders
    groups = {
        "Responders NC": data["change_image_sAA_level"][:22],
        "Non-Responders NC": data["change_image_sAA_level"][22:42],
        "Responders HC": data["change_image_sAA_level"][42:59],
        "Non-Responders HC": data["change_image_sAA_level"][59:],
    }

    # Plot for sAA Responders
    plt.figure(figsize=(8, 6))
    plt.bar(
        ["HC Women", "NC Women"],
        [
            np.mean(groups["Responders HC"]),
            np.mean(groups["Responders NC"])
        ],
        capsize=5, color=["gray", "lightgray"], alpha=0.8
    )
    plt.title("sAA Responders: sAA Response to Slide Show", fontsize=14, weight="bold")
    plt.ylabel("sAA Change (U/mL)\nSEM", fontsize=12)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

    # Plot for sAA Non-Responders
    plt.figure(figsize=(8, 6))
    plt.bar(
        ["HC Women", "NC Women"],
        [
            np.mean(groups["Non-Responders HC"]),
            np.mean(groups["Non-Responders NC"])
        ],
        capsize=5, color=["gray", "lightgray"], alpha=0.8
    )
    plt.title("sAA Non-Responders: sAA Response to Slide Show", fontsize=14, weight="bold")
    plt.ylabel("sAA Change (U/mL)\nSEM", fontsize=12)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.axhline(0, color="black", linewidth=0.8, linestyle="-")  # Add a horizontal line at y=0
    plt.show()

# Initialize the data file
file = InitializeFile().file

# Run the test function
article_test(file)
