import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from scipy.stats import f_oneway
import sys
sys.path.append(r'C:\Users\matan\OneDrive\שולחן העבודה\python\project\src')
sys.path.append(r'C:\Users\matan\OneDrive\שולחן העבודה\python\project\src\functions')
sys.path.append(r'C:\Users\matan\OneDrive\שולחן העבודה\python\project\src\objects')

def plot_difference_of_cortisol_chi2(data: pd.DataFrame, chi2: float, p: float, threshold: float=0.055) ->None:
    """
    Creates a bar plot comparing the number of cortisol responders and non-responders in two groups 
    (Naturally Cycling (NC) and Hormonal Contraceptive (HC) women). The function includes annotations, 
    a trend line, and statistical information.

    Parameters:
        data (df.DataFrame): The DataFrame we perform the analysis on.
        chi2 (float): The Chi-square statistic value.
        p (float): The p-value associated with the Chi-square test.
        threshold (float, optional): The threshold for defining responders in μg/dL. Default is 0.055.

    Returns:
        None: This function generates and displays a plot but does not return any value.
    """

     # Create figure and axis
    plt.figure(figsize=(8, 6))
    
    # Plot bars
    bar_width = 0.35
    x = range(len(data['Group']))
    
    # Plot Responders and Non-Responders bars
    plt.bar(x, data['Responders'], bar_width, color='#E6E6FA', label='Responders')
    plt.bar([i + bar_width for i in x], data['Non-Responders'], bar_width, 
            color='#87CEFA', label='Non-Responders')
    
    # Customize the plot
    plt.title('Number of CPS Cortisol Responders and Non-Responders in\n'
              'Naturally Cycling (NC) and Hormonal Contraceptive (HC) Women')
    plt.xlabel('Contraceptive Group')
    plt.ylabel('Number of Participants')
    
    # Set x-axis ticks
    plt.xticks([i + bar_width/2 for i in x], data['Group'])
    
    # Add trend line
    plt.plot([0 + bar_width/2, 1 + bar_width/2], 
             [data['Responders'].iloc[0], data['Responders'].iloc[1]],
             'k--', label='Trend Line')
    
    # Add 'Higher Responders in NC' annotation
    plt.annotate('Higher Responders in NC',
                xy=(1 + bar_width/2, data['Responders'].iloc[1]),
                xytext=(0.5 + bar_width/2, data['Responders'].max() + 2),
                arrowprops=dict(facecolor='black', arrowstyle='->'),
                ha='center')
    
    # Set y-axis limit to match reference
    plt.ylim(0, 30)
    
    # Add legend
    plt.legend(loc='upper right')
    
    # Add statistical information
    plt.figtext(0.15, 0.02,
                f"Threshold used for defining responders: {threshold:.3f} μg/dL\n"
                f"Chi-square statistic: {chi2:.2f}\n"
                f"p-value: {p:.4f}\n"
                "No statistically significant difference (p ≥ 0.05)",
                fontsize=8)
    
    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)
    plt.show()

def plot_difference_sAA_responses(data: pd.DataFrame) -> None: 

    """
    Plots the difference in salivary alpha-amylase (sAA) responses between women in HC (Hormonal Contraceptive) 
    and NC (Natural Cycle) groups based on the provided data.

    Parameters:
        data (pd.DataFrame): The DataFrame we perform the analysis on

    Returns:
        None: The function generates a bar plot but does not return any value
    
    Raises:
        KeyError: If required columns are missing from the data
    """

    # Extract groups from the DataFrame. 
    try:
        groups = {
            'NC': data['change_image_sAA_level'][:42],
            'HC': data['change_image_sAA_level'][42:],
        }
    except KeyError as e:
        # Handle missing or incorrect group data
        print(f"Error accessing group data: {e}")
        raise  # Re-raise the exception

    plt.figure(figsize=(8, 6))
    # Create a bar plot with labels and formatting, calculate the mean for each group as the Y axis.
    plt.bar(['HC Women', 'NC Women'], [np.mean(groups['HC']),np.mean(groups['NC'])], capsize=5, color=['#4A6D7C', '#475657'], alpha=0.8)
    plt.title('difference sAA responses: between women in the HC group and the NC group', fontsize=10, weight='bold')
    plt.ylabel('sAA Change (U/mL)\nSEM', fontsize=12)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def statistics_of_sAA_responses(results: dict) -> None:
    """
    Display sAA response Anova analysis results as a visual table
   
    Parameters:
    results (dict): Dictionary containing ANOVA, effect size, and summary statistics

    Returns:
        None: The function generates a table plot but does not return any value
    """
    # Prepare the data for visualization
    table_data = []
    table_data.append(["F-statistic", f"{results['anova_results']['f_statistic']:.4f}"])
    table_data.append(["P-value", f"{results['anova_results']['p_value']:.4f}"])
    table_data.append(["Effect Size (Cohen's d)", f"{results['effect_size']['cohens_d']:.4f}"])

    for group in ['HC', 'NC']:
        for stat, value in results['summary_statistics'][group].items():
            table_data.append([f"{group} {stat.capitalize()}", f"{value:.4f}"])

    # Plot the table
    plt.figure(figsize=(10, 5))
    plt.axis('off')
    plt.title("sAA Response Analysis Results", fontsize=14, weight='bold')

    # Create the table
    table = plt.table(
        cellText=table_data,
        colLabels=["Metric", "Value"],
        cellLoc='center',
        loc='center',
        bbox=[0, 0, 1, 1]
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=[0, 1])

    plt.show()


def plot_affect_basleline_cortisol_sAA_linear_regressions(data: pd.DataFrame) -> None:
    """
    Creates scatter plots with linear regression lines for:
    1. SAA Level Baseline vs Change in Cortisol Level
    2. Cortisol Level Baseline vs Change in Cortisol Level
    for two groups: Naturally Cycling (NC) and Hormonal Contraceptive (HC).

    Parameters:
        data (pd.DataFrame): The DataFrame we perform the analysis on

    Returns:
        None: The function generates and displays scatter plots with regression lines.
    
    Raises:
        KeyError: If required columns are missing from the data
    """

    # Separate data by groups
    try:
        group_nc = data[data['status'] == 'NC'].copy()
        group_hc = data[data['status'] == 'HC'].copy()
    except KeyError as e:
        # Handle missing contingency table columns
        print(f"Error accessing contingency table columns: {e}")
        raise  # Re-raise the exception

    # Plot SAA Level Baseline vs Change in Cortisol Level
    plt.figure(figsize=(10, 8))

    # Group NC
    try:
        x_nc_saa = group_nc['sAA_level_baseline']
        y_nc_cortisol = group_nc['change_CPS_cortisol_level']
    except KeyError as e:
        # Handle missing contingency table columns
        print(f"Error accessing contingency table columns: {e}")
        raise  # Re-raise the exception
    x_nc_saa_const = sm.add_constant(x_nc_saa)
    model_nc_saa = sm.OLS(y_nc_cortisol, x_nc_saa_const).fit()
    y_nc_pred_saa = model_nc_saa.predict(x_nc_saa_const)
    plt.scatter(x_nc_saa, y_nc_cortisol, alpha=0.7, label='NC (Data)', color='blue')
    plt.plot(x_nc_saa, y_nc_pred_saa, label='NC (Regression)', color='blue', linestyle='--')

    # Group HC
    try:
        x_hc_saa = group_hc['sAA_level_baseline']
        y_hc_cortisol = group_hc['change_CPS_cortisol_level']
    except KeyError as e:
        # Handle missing contingency table columns
        print(f"Error accessing contingency table columns: {e}")
        raise  # Re-raise the exception
    x_hc_saa_const = sm.add_constant(x_hc_saa)
    model_hc_saa = sm.OLS(y_hc_cortisol, x_hc_saa_const).fit()
    y_hc_pred_saa = model_hc_saa.predict(x_hc_saa_const)
    plt.scatter(x_hc_saa, y_hc_cortisol, alpha=0.7, label='HC (Data)', color='orange')
    plt.plot(x_hc_saa, y_hc_pred_saa, label='HC (Regression)', color='orange', linestyle='--')

    plt.xlabel('SAA Level Baseline')
    plt.ylabel('Change in Cortisol Level')
    plt.title('SAA Level Baseline vs Change in Cortisol Level (NC vs HC)')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Plot Cortisol Level Baseline vs Change in Cortisol Level
    plt.figure(figsize=(10, 8))

    # Group NC
    try:
        x_nc_cortisol = group_nc['cortisol_level_baseline']
        y_nc_cortisol_change = group_nc['change_CPS_cortisol_level']
    except KeyError as e:
        # Handle missing contingency table columns
        print(f"Error accessing contingency table columns: {e}")
        raise  # Re-raise the exception
    x_nc_cortisol_const = sm.add_constant(x_nc_cortisol)
    model_nc_cortisol = sm.OLS(y_nc_cortisol_change, x_nc_cortisol_const).fit()
    y_nc_pred_cortisol = model_nc_cortisol.predict(x_nc_cortisol_const)
    plt.scatter(x_nc_cortisol, y_nc_cortisol_change, alpha=0.7, label='NC (Data)', color='blue')
    plt.plot(x_nc_cortisol, y_nc_pred_cortisol, label='NC (Regression)', color='blue', linestyle='--')

    # Group HC
    try:
        x_hc_cortisol = group_hc['cortisol_level_baseline']
        y_hc_cortisol_change = group_hc['change_CPS_cortisol_level']
    except KeyError as e:
        # Handle missing contingency table columns
        print(f"Error accessing contingency table columns: {e}")
        raise  # Re-raise the exception
    x_hc_cortisol_const = sm.add_constant(x_hc_cortisol)
    model_hc_cortisol = sm.OLS(y_hc_cortisol_change, x_hc_cortisol_const).fit()
    y_hc_pred_cortisol = model_hc_cortisol.predict(x_hc_cortisol_const)
    plt.scatter(x_hc_cortisol, y_hc_cortisol_change, alpha=0.7, label='HC (Data)', color='orange')
    plt.plot(x_hc_cortisol, y_hc_pred_cortisol, label='HC (Regression)', color='orange', linestyle='--')

    plt.xlabel('Cortisol Level Baseline')
    plt.ylabel('Change in Cortisol Level')
    plt.title('Cortisol Level Baseline vs Change in Cortisol Level (NC vs HC)')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_cortisol_phase_pill_effects(anova_nc_baseline: f_oneway, anova_nc_change: f_oneway, 
                                     anova_hc_baseline: f_oneway, anova_hc_change: f_oneway, 
                                     nc_data: pd.DataFrame, hc_data: pd.DataFrame) -> None:
    """
    Creates a 2x2 grid of bar plots to visualize the effects of menstrual phase and pill type on cortisol levels 
    (baseline and change) for Naturally Cycling (NC) and Hormonal Contraceptive (HC) groups.

    Parameters:
        anova_nc_baseline (f_oneway): ANOVA result for baseline cortisol levels in the NC group.
        anova_nc_change (f_oneway): ANOVA result for cortisol change in the NC group.
        anova_hc_baseline (f_oneway): ANOVA result for baseline cortisol levels in the HC group.
        anova_hc_change (f_oneway): ANOVA result for cortisol change in the HC group.
        nc_data (pd.DataFrame): DataFrame of the NC group 
        hc_data (pd.DataFrame): DataFrame of the HC group

    Returns:
        None: The function generates and displays a grid of bar plots.
    """

    plt.figure(figsize=(10, 8))  # Adjusted size to make each subplot smaller

    # NC baseline cortisol levels
    plt.subplot(2, 2, 1)
    sns.barplot(data=nc_data, x='phase', y='cortisol_level_baseline', palette='muted', errorbar=None, hue= 'phase', legend=False)
    plt.title('NC Baseline Cortisol Levels', fontsize=10)
    plt.xlabel('phase', fontsize=10, labelpad=-7)
    plt.ylabel('Baseline Cortisol Level', fontsize=8)
    plt.xticks(rotation=45, fontsize=8, ha='right')
    plt.yticks(fontsize=8)
    plt.ylim(0, nc_data['cortisol_level_baseline'].max() * 1.1)

    # NC cortisol change
    plt.subplot(2, 2, 2)
    sns.barplot(data=nc_data, x='phase', y='cortisol_change', palette='muted', errorbar=None,  hue= 'phase', legend=False)
    plt.title('NC Cortisol Change', fontsize=10)
    plt.xlabel('phase', fontsize=10, labelpad=-7)
    plt.ylabel('Cortisol Change', fontsize=8)
    plt.xticks(rotation=45, fontsize=8, ha='right')
    plt.yticks(fontsize=8)
    plt.ylim(0, nc_data['cortisol_change'].max() * 1.1)

    # HC baseline cortisol levels
    plt.subplot(2, 2, 3)
    sns.barplot(data=hc_data, x='pill_type', y='cortisol_level_baseline', palette='pastel', errorbar=None, hue= 'pill_type', legend=False)
    plt.title('HC Baseline Cortisol Levels', fontsize=10)
    plt.ylabel('Baseline Cortisol Level', fontsize=8)
    plt.xlabel('Pill Type', fontsize=10, labelpad=-7)
    plt.xticks(rotation=45, fontsize=8, ha='right')
    plt.yticks(fontsize=8)
    plt.ylim(0, hc_data['cortisol_level_baseline'].max() * 1.1)

    # HC cortisol change
    plt.subplot(2, 2, 4)
    sns.barplot(data=hc_data, x='pill_type', y='cortisol_change', palette='pastel', errorbar=None, hue= 'pill_type', legend=False)
    plt.title('HC Cortisol Change', fontsize=10)
    plt.ylabel('Cortisol Change', fontsize=8)
    plt.xlabel('Pill Type', fontsize=10, labelpad=-7)
    plt.xticks(rotation=45, fontsize=8, ha='right')
    plt.yticks(fontsize=8)
    plt.ylim(0, hc_data['cortisol_change'].max() * 1.1)

    plt.tight_layout()
    plt.show()

def plot_negative_images_responses(data: pd.DataFrame) -> None:
    """
    Plots the average memory for negative stimuli based on SAA and Cortisol responses in two groups 
    (Hormonal Contraceptive (HC) and Naturally Cycling (NC)).

    Parameters:
        data (pd.DataFrame): The DataFrame we perform the analysis on

    Returns:
        None: This function generates and displays a bar plot but does not return any value.
    
    Raises:
        KeyError: If required columns are missing from the data
    """
    # Split data based on group (HC vs NC)
    try:
        hc_data = data[data['status'] == 'HC'].copy()
        nc_data = data[data['status'] == 'NC'].copy()

        # Define responders and non-responders for both HC and NC
        hc_data['saa_responders'] = np.where(hc_data['responsive_state_SAA'] == 'responders', 'SAA Responders', 'SAA Nonresponders')
        hc_data['cortisol_responders'] = np.where(hc_data['responsive_state_cortisol'] == 'responders', 'Cortisol Responders', 'Cortisol Nonresponders')

        nc_data['saa_responders'] = np.where(nc_data['responsive_state_SAA'] == 'responders', 'SAA Responders', 'SAA Nonresponders')
        nc_data['cortisol_responders'] = np.where(nc_data['responsive_state_cortisol'] == 'responders', 'Cortisol Responders', 'Cortisol Nonresponders')
    except KeyError as e:
        # Handle missing contingency table columns
        print(f"Error accessing contingency table columns: {e}")
        raise  # Re-raise the exception
    
    # Combine data for plotting
    combined_data_saa = pd.concat([hc_data[['status', 'saa_responders', 'negative_image']],
                                   nc_data[['status', 'saa_responders', 'negative_image']]])
    combined_data_cortisol = pd.concat([hc_data[['status', 'cortisol_responders', 'negative_image']],
                                        nc_data[['status', 'cortisol_responders', 'negative_image']]])

    # Merge the two datasets for unified x-axis
    combined_data_saa['response_type'] = 'SAA'
    combined_data_saa.rename(columns={'saa_responders': 'responders'}, inplace=True)
    combined_data_cortisol['response_type'] = 'Cortisol'
    combined_data_cortisol.rename(columns={'cortisol_responders': 'responders'}, inplace=True)

    merged_data = pd.concat([combined_data_saa, combined_data_cortisol])

    # Create a combined bar plot
    plt.figure(figsize=(12, 8))
    sns.barplot(data=merged_data, x='responders', y='negative_image', hue='status', errorbar=None, palette="pastel", dodge=True)
    plt.title('Memory for Negative Stimuli Based on SAA and Cortisol Responses (Combined)')
    plt.ylabel('Average Memory for Negative Stimuli')
    plt.xlabel('Responders vs Nonresponders')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def heatMap(group_means: pd.DataFrame, val: str):
    """
    Creates a heatmap visualization of group means based on the specified value column.

    Parameters:
        group_means (pd.DataFrame): The DataFrame we perform the analysis on.
        val (str): The name of the column in `group_means` to be used for the heatmap values.

    Returns:
        None: The function generates and displays a heatmap but does not return any value.

    Raises:
        KeyError: If required columns are missing from the data
    """

    # Extract relevant data
    try:
        means = group_means.pivot(index=['saa_responders', 'cortisol_responders'], columns='status', values= val)
    except KeyError as e:
        # Handle missing contingency table columns
        print(f"Error accessing contingency table columns: {e}")
        raise  # Re-raise the exception
    # Visualization of group means
    plt.figure(figsize=(10, 6))
    sns.heatmap(means, annot=True, fmt=".2f", cmap="coolwarm", cbar_kws={'label': 'Mean Memory Score'})
    plt.title("Heatmap of Group Means")
    plt.xlabel("Status")
    plt.ylabel("SAA and Cortisol Responders")
    plt.tight_layout()
    plt.show()


def vizualizations_two_way_anova(anova_table: pd.DataFrame) -> None:
    """
    Creates visualizations for a two-way ANOVA table, displaying F-values and p-values for effects related to status.

    Parameters:
        anova_table (pd.DataFrame): A pandas DataFrame containing the ANOVA results.
                                    Must include the following columns:
                                    - 'Effect': The effect names.
                                    - 'F': The F-values for each effect.
                                    - 'PR(>F)': The p-values for each effect.

    Returns:
        None: The function generates and displays bar plots but does not return any value.
    """

    # Visualization of ANOVA F-Values and p-Values (filtering for 'status' effects only)
    anova_viz = anova_table.reset_index().rename(columns={'index': 'Effect'})
    anova_viz = anova_viz[anova_viz['Effect'].str.contains('status')]


    # Plot F-Values for status effects
    plt.figure(figsize=(12, 6))
    sns.barplot(data=anova_viz, x='Effect', y='F', palette='muted', legend=False, hue='Effect')
    plt.title('ANOVA F-Values for Status(NC/HC) Effects')
    plt.ylabel('F-Value')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Plot p-Values for status effects
    plt.figure(figsize=(12, 6))
    sns.barplot(data=anova_viz, x='Effect', y='PR(>F)', palette='muted', legend=False, hue='Effect')
    plt.title('ANOVA p-Values for Status(NC/HC) Effects')
    plt.ylabel('p-Value')
    plt.xticks(rotation=45)
    plt.axhline(0.05, color='red', linestyle='--', label='Significance Threshold (p=0.05)')
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_positive_images_responses(data: pd.DataFrame) -> None:
    """
    Plots the average memory for positive stimuli based on SAA and Cortisol responses in two groups 
    (Hormonal Contraceptive (HC) and Naturally Cycling (NC)).

    Args:
        data (pd.DataFrame): The DataFrame we perform the analysis on.

    Returns:
        None: This function generates and displays a bar plot but does not return any value.

    Raises:
        KeyError: If required columns are missing from the data
    """
    # Split data based on group (HC vs NC)
    try:
        hc_data = data[data['status'] == 'HC'].copy()
        nc_data = data[data['status'] == 'NC'].copy()
    
        # Define responders and non-responders for both HC and NC
        hc_data['saa_responders'] = np.where(hc_data['responsive_state_SAA'] == 'responders', 'SAA Responders', 'SAA Nonresponders')
        hc_data['cortisol_responders'] = np.where(hc_data['responsive_state_cortisol'] == 'responders', 'Cortisol Responders', 'Cortisol Nonresponders')

        nc_data['saa_responders'] = np.where(nc_data['responsive_state_SAA'] == 'responders', 'SAA Responders', 'SAA Nonresponders')
        nc_data['cortisol_responders'] = np.where(nc_data['responsive_state_cortisol'] == 'responders', 'Cortisol Responders', 'Cortisol Nonresponders')
    except KeyError as e:
        # Handle missing contingency table columns
        print(f"Error accessing contingency table columns: {e}")
        raise  # Re-raise the exception
    
    # Combine data for plotting
    combined_data_saa = pd.concat([hc_data[['status', 'saa_responders', 'positive_image']],
                                   nc_data[['status', 'saa_responders', 'positive_image']]])
    combined_data_cortisol = pd.concat([hc_data[['status', 'cortisol_responders', 'positive_image']],
                                        nc_data[['status', 'cortisol_responders', 'positive_image']]])

    # Merge the two datasets for unified x-axis
    combined_data_saa['response_type'] = 'SAA'
    combined_data_saa.rename(columns={'saa_responders': 'responders'}, inplace=True)
    combined_data_cortisol['response_type'] = 'Cortisol'
    combined_data_cortisol.rename(columns={'cortisol_responders': 'responders'}, inplace=True)

    merged_data = pd.concat([combined_data_saa, combined_data_cortisol])

    # Create a combined bar plot
    plt.figure(figsize=(12, 8))
    sns.barplot(data=merged_data, x='responders', y='positive_image', hue='status', errorbar=None, palette="muted", dodge=True)
    plt.title('Memory for Positive Stimuli Based on SAA and Cortisol Responses (Combined)')
    plt.ylabel('Average Memory for Positive Stimuli')
    plt.xlabel('Responders vs Nonresponders')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
