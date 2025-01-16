import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import sys
sys.path.append(r'C:\Users\matan\OneDrive\שולחן העבודה\python\project\src')
sys.path.append(r'C:\Users\matan\OneDrive\שולחן העבודה\python\project\src\functions')
sys.path.append(r'C:\Users\matan\OneDrive\שולחן העבודה\python\project\src\objects')

def plot_difference_sAA_responses(data): 

    groups = {
         'NC': data['change_image_sAA_level'][:42],
         'HC': data['change_image_sAA_level'][42:],
     }

    plt.figure(figsize=(8, 6))
    plt.bar(['HC Women', 'NC Women'], [np.mean(groups['HC']),np.mean(groups['NC'])], capsize=5, color=['#4A6D7C', '#475657'], alpha=0.8)
    plt.title('difference sAA responses: between women in the HC group and the NC group', fontsize=10, weight='bold')
    plt.ylabel('sAA Change (U/mL)\nSEM', fontsize=12)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def statistics_of_sAA_responses(results):
    """
    Display sAA response analysis results as a visual table
   
    Parameters:
    results (dict): Dictionary containing ANOVA, effect size, and summary statistics
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

def plot_difference_of_cortisol_chi2(df, chi2, p, threshold=0.055):
    """
    Creates the final visualization matching the reference image.
    """
    # Create figure and axis
    plt.figure(figsize=(8, 6))
    
    # Plot bars
    bar_width = 0.35
    x = range(len(df['Group']))
    
    # Plot Responders and Non-Responders bars
    plt.bar(x, df['Responders'], bar_width, color='gray', label='Responders')
    plt.bar([i + bar_width for i in x], df['Non-Responders'], bar_width, 
            color='lightgray', label='Non-Responders')
    
    # Customize the plot
    plt.title('Number of CPS Cortisol Responders and Non-Responders in\n'
              'Naturally Cycling (NC) and Hormonal Contraceptive (HC) Women')
    plt.xlabel('Contraceptive Group')
    plt.ylabel('Number of Participants')
    
    # Set x-axis ticks
    plt.xticks([i + bar_width/2 for i in x], df['Group'])
    
    # Add trend line
    plt.plot([0 + bar_width/2, 1 + bar_width/2], 
             [df['Responders'].iloc[0], df['Responders'].iloc[1]],
             'k--', label='Trend Line')
    
    # Add 'Higher Responders in NC' annotation
    plt.annotate('Higher Responders in NC',
                xy=(1 + bar_width/2, df['Responders'].iloc[1]),
                xytext=(0.5 + bar_width/2, df['Responders'].max() + 2),
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

def plot_positive_images_responses(data):
    # Split data based on group (HC vs NC)
    hc_data = data[data['status'] == 'HC'].copy()
    nc_data = data[data['status'] == 'NC'].copy()

    # Define responders and non-responders for both HC and NC
    hc_data['saa_responders'] = np.where(hc_data['responsive_state_SAA'] == 'responders', 'SAA Responders', 'SAA Nonresponders')
    hc_data['cortisol_responders'] = np.where(hc_data['responsive_state_cortisol'] == 'responders', 'Cortisol Responders', 'Cortisol Nonresponders')

    nc_data['saa_responders'] = np.where(nc_data['responsive_state_SAA'] == 'responders', 'SAA Responders', 'SAA Nonresponders')
    nc_data['cortisol_responders'] = np.where(nc_data['responsive_state_cortisol'] == 'responders', 'Cortisol Responders', 'Cortisol Nonresponders')

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

def heatMap(group_means, val):
    
    # Extract relevant data
    means = group_means.pivot(index=['saa_responders', 'cortisol_responders'], columns='status', values= val)

    # Visualization of group means
    plt.figure(figsize=(10, 6))
    sns.heatmap(means, annot=True, fmt=".2f", cmap="coolwarm", cbar_kws={'label': 'Mean Memory Score'})
    plt.title("Heatmap of Group Means")
    plt.xlabel("Status")
    plt.ylabel("SAA and Cortisol Responders")
    plt.tight_layout()
    plt.show()

def vizualizations_two_way_anova(anova_table):
    # Visualization of ANOVA F-Values and p-Values (filtering for 'status' effects only)
    anova_viz = anova_table.reset_index().rename(columns={'index': 'Effect'})
    anova_viz = anova_viz[anova_viz['Effect'].str.contains('status')]

    plt.figure(figsize=(12, 6))
    sns.barplot(data=anova_viz, x='Effect', y='F', palette='muted', legend=False, hue='Effect')
    plt.title('ANOVA F-Values for Status(NC/HC) Effects')
    plt.ylabel('F-Value')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.barplot(data=anova_viz, x='Effect', y='PR(>F)', palette='muted', legend=False, hue='Effect')
    plt.title('ANOVA p-Values for Status(NC/HC) Effects')
    plt.ylabel('p-Value')
    plt.xticks(rotation=45)
    plt.axhline(0.05, color='red', linestyle='--', label='Significance Threshold (p=0.05)')
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_negative_images_responses(data):
    # Split data based on group (HC vs NC)
    hc_data = data[data['status'] == 'HC'].copy()
    nc_data = data[data['status'] == 'NC'].copy()

    # Define responders and non-responders for both HC and NC
    hc_data['saa_responders'] = np.where(hc_data['responsive_state_SAA'] == 'responders', 'SAA Responders', 'SAA Nonresponders')
    hc_data['cortisol_responders'] = np.where(hc_data['responsive_state_cortisol'] == 'responders', 'Cortisol Responders', 'Cortisol Nonresponders')

    nc_data['saa_responders'] = np.where(nc_data['responsive_state_SAA'] == 'responders', 'SAA Responders', 'SAA Nonresponders')
    nc_data['cortisol_responders'] = np.where(nc_data['responsive_state_cortisol'] == 'responders', 'Cortisol Responders', 'Cortisol Nonresponders')

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

def plot_affect_basleline_cortisol_sAA_linear_regressions(data):
    # Separate data by groups
    group_nc = data[data['status'] == 'NC'].copy()
    group_hc = data[data['status'] == 'HC'].copy()

    # Plot SAA Level Baseline vs Change in Cortisol Level
    plt.figure(figsize=(10, 8))

    # Group NC
    x_nc_saa = group_nc['sAA_level_baseline']
    y_nc_cortisol = group_nc['change_CPS_cortisol_level']
    x_nc_saa_const = sm.add_constant(x_nc_saa)
    model_nc_saa = sm.OLS(y_nc_cortisol, x_nc_saa_const).fit()
    y_nc_pred_saa = model_nc_saa.predict(x_nc_saa_const)
    plt.scatter(x_nc_saa, y_nc_cortisol, alpha=0.7, label='NC (Data)', color='blue')
    plt.plot(x_nc_saa, y_nc_pred_saa, label='NC (Regression)', color='blue', linestyle='--')

    # Group HC
    x_hc_saa = group_hc['sAA_level_baseline']
    y_hc_cortisol = group_hc['change_CPS_cortisol_level']
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
    x_nc_cortisol = group_nc['cortisol_level_baseline']
    y_nc_cortisol_change = group_nc['change_CPS_cortisol_level']
    x_nc_cortisol_const = sm.add_constant(x_nc_cortisol)
    model_nc_cortisol = sm.OLS(y_nc_cortisol_change, x_nc_cortisol_const).fit()
    y_nc_pred_cortisol = model_nc_cortisol.predict(x_nc_cortisol_const)
    plt.scatter(x_nc_cortisol, y_nc_cortisol_change, alpha=0.7, label='NC (Data)', color='blue')
    plt.plot(x_nc_cortisol, y_nc_pred_cortisol, label='NC (Regression)', color='blue', linestyle='--')

    # Group HC
    x_hc_cortisol = group_hc['cortisol_level_baseline']
    y_hc_cortisol_change = group_hc['change_CPS_cortisol_level']
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

def plot_cortisol_phase_pill_effects(anova_nc_baseline, anova_nc_change, anova_hc_baseline, anova_hc_change, nc_data, hc_data):
     # Create plots
    plt.figure(figsize=(10, 8))  # Adjusted size to make each subplot smaller

    # NC baseline cortisol levels
    plt.subplot(2, 2, 1)
    sns.barplot(data=nc_data, x='phase', y='cortisol_level_baseline', palette='muted', errorbar=None, hue= 'phase', legend=False)
    plt.title(f'NC Baseline Cortisol Levels (p = {anova_nc_baseline.pvalue:.3f})', fontsize=10)
    plt.xlabel('phase', fontsize=10, labelpad=-7)
    plt.ylabel('Baseline Cortisol Level', fontsize=8)
    plt.xticks(rotation=45, fontsize=8, ha='right')
    plt.yticks(fontsize=8)
    plt.ylim(0, nc_data['cortisol_level_baseline'].max() * 1.1)

    # NC cortisol change
    plt.subplot(2, 2, 2)
    sns.barplot(data=nc_data, x='phase', y='cortisol_change', palette='muted', errorbar=None,  hue= 'phase', legend=False)
    plt.title(f'NC Cortisol Change (p = {anova_nc_change.pvalue:.3f})', fontsize=10)
    plt.xlabel('phase', fontsize=10, labelpad=-7)
    plt.ylabel('Cortisol Change', fontsize=8)
    plt.xticks(rotation=45, fontsize=8, ha='right')
    plt.yticks(fontsize=8)
    plt.ylim(0, nc_data['cortisol_change'].max() * 1.1)

    # HC baseline cortisol levels
    plt.subplot(2, 2, 3)
    sns.barplot(data=hc_data, x='pill_type', y='cortisol_level_baseline', palette='pastel', errorbar=None, hue= 'pill_type', legend=False)
    plt.title(f'HC Baseline Cortisol Levels (p = {anova_hc_baseline.pvalue:.3f})', fontsize=10)
    plt.ylabel('Baseline Cortisol Level', fontsize=8)
    plt.xlabel('Pill Type', fontsize=10, labelpad=-7)
    plt.xticks(rotation=45, fontsize=8, ha='right')
    plt.yticks(fontsize=8)
    plt.ylim(0, hc_data['cortisol_level_baseline'].max() * 1.1)

    # HC cortisol change
    plt.subplot(2, 2, 4)
    sns.barplot(data=hc_data, x='pill_type', y='cortisol_change', palette='pastel', errorbar=None, hue= 'pill_type', legend=False)
    plt.title(f'HC Cortisol Change (p = {anova_hc_change.pvalue:.3f})', fontsize=10)
    plt.ylabel('Cortisol Change', fontsize=8)
    plt.xlabel('Pill Type', fontsize=10, labelpad=-7)
    plt.xticks(rotation=45, fontsize=8, ha='right')
    plt.yticks(fontsize=8)
    plt.ylim(0, hc_data['cortisol_change'].max() * 1.1)

    plt.tight_layout()
    plt.show()


