import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from scipy.stats import f_oneway
import statsmodels.api as sm
from statsmodels.formula.api import ols
import sys

sys.path.append(r'C:\Users\matan\OneDrive\שולחן העבודה\python\project\src')
sys.path.append(r'C:\Users\matan\OneDrive\שולחן העבודה\python\project\src\functions')
sys.path.append(r'C:\Users\matan\OneDrive\שולחן העבודה\python\project\src\objects')


def analyze_saa_response(data: pd.DataFrame ) -> dict: 
    """
    Analyze sAA response differences between HC and NC groups
    
    Parameters:
    data (pd.DataFrame): The DataFrame we perform the analysis on
    
    Returns:
    dict: Dictionary containing all statistical results and summary statistics

    Raises:
        KeyError: If the columns are missing
     """    
    required_columns = [
        'change_image_sAA_level', 'cortisol_level_baseline',
        'change_CPS_cortisol_level', 'sAA_level_baseline'
    ]
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        raise KeyError(f"Missing required columns: {', '.join(missing_columns)}")
    # Rest of the function logic...

    # Create separate groups for HC and NC
    hc_group = data['change_image_sAA_level'][42:].dropna()
    nc_group = data['change_image_sAA_level'][:42].dropna()
    
    # Perform one-way ANOVA
    f_statistic, p_value = f_oneway(hc_group,nc_group)
    
    # Calculate descriptive statistics
    summary_stats = {
        'HC': {
            'count': len(hc_group),
            'mean': float(hc_group.mean()),
            'std': float(hc_group.std()),
            'min': float(hc_group.min()),
            'max': float(hc_group.max())
        },
        'NC': {
            'count': len(nc_group),
            'mean': float(nc_group.mean()),
            'std': float(nc_group.std()),
            'min': float(nc_group.min()),
            'max': float(nc_group.max())
        }
    }
    
    # Calculate effect size
    effect_size = calculate_effect_size(hc_group, nc_group)
    
    # Organize all results in a dictionary
    results = {
        'anova_results': {
            'f_statistic': float(f_statistic),
            'p_value': float(p_value)
        },
        'effect_size': {
            'cohens_d': float(effect_size)
        },
        'summary_statistics': summary_stats,
        'group_data': {
            'HC': list(hc_group),
            'NC': list(nc_group)
        }
    }    
    return results

def calculate_effect_size(group1: pd.Series, group2: pd.Series) -> float:
    """
    Calculate Cohen's d effect size.
    
    Parameters:
    group1 (pd.DataFrame): HC group data
    group2 (pd.DataFrame): NC group data
    
    Returns:
    float: Cohen's d effect size
    
    Raises:
    ZeroDivisionError: If there is a division by zero during calculation
    """
    n1, n2 = len(group1), len(group2)
    var1, var2 = group1.var(), group2.var()
    
    # Pooled standard deviation
    
    if (n1 + n2 - 2) == 0:
        raise ZeroDivisionError("Deviation is zero. Cannot calculate pooled standard.")
    pooled_sd = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_sd == 0:
        raise ZeroDivisionError("Pooled standard deviation is zero. Cannot calculate Cohen's d.")
    # Cohen's d calculation
    d = (group1.mean() - group2.mean()) / pooled_sd
    
    return d


def chi_square(data: pd.DataFrame) -> tuple:
    """
    Perform chi-square test on the data.
    
    Parameters:
    data (pd.DataFrame): The DataFrame for chi-square analysis
    
    Returns:
    tuple:
        - float: chi-square test statistic (chi2)
        - float: p-value for the chi-square test
        - np.ndarray: Contingency table used for the chi-square test
    
    Raises:
        KeyError: If the columns for 'Responders' and 'Non-Responders' are missing
    """
    try:
        contingency_table = data[["Responders", "Non-Responders"]].values
        chi2, p, _, _ = chi2_contingency(contingency_table)
    except KeyError as e:
        # Handle missing columns error
        print(f"Error accessing contingency table columns: {e}")
        raise  # Re-raise the exception

    return chi2, p, contingency_table

def calculate_two_way_anova_with_viz_positive(data: pd.DataFrame) -> tuple:
    """
    Calculates a Two-Way ANOVA with interaction effects for positive image ratings.
    
    Parameters:
    data (pd.DataFrame): The DataFrame for analysis
    
    Returns:
    tuple:
        - pd.DataFrame: Group means for positive image ratings
        - pd.DataFrame: ANOVA table containing F-statistics and p-values
    
    Raises:
    KeyError: If required columns are missing or not categorized properly
    """
    try:
        # Categorize into responders and non-responders
        data['saa_responders'] = np.where(data['responsive_state_SAA'] == 'responders', 'SAA Responders', 'SAA Nonresponders')
        data['cortisol_responders'] = np.where(data['responsive_state_cortisol'] == 'responders', 'Cortisol Responders', 'Cortisol Nonresponders')
        # Calculate means for each group (by status and responder type)
        group_means = data.groupby(['status', 'saa_responders', 'cortisol_responders']).agg({'positive_image': 'mean'}).reset_index()
    except KeyError as e:
        # Handle missing categorization columns
        print(f"Error categorizing responder states: {e}")
        raise  # Re-raise the exception

    # Perform the Two-Way ANOVA
    model = ols('positive_image ~ C(status) * C(saa_responders) * C(cortisol_responders)', data=data).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)

    return group_means, anova_table


def calculate_two_way_anova_with_viz_negative(data: pd.DataFrame) -> tuple:
    """
    Calculates a Two-Way ANOVA with interaction effects for negative image ratings.
    
    Parameters:
    data (pd.DataFrame): The DataFrame for analysis
    
    Returns:
    tuple:
        - pd.DataFrame: Group means for negative image ratings
        - pd.DataFrame: ANOVA table containing F-statistics and p-values
    
    Raises:
    KeyError: If required columns are missing or not categorized properly
    """
    try:
        # Categorize into responders and non-responders
        data['saa_responders'] = np.where(data['responsive_state_SAA'] == 'responders', 'SAA Responders', 'SAA Nonresponders')
        data['cortisol_responders'] = np.where(data['responsive_state_cortisol'] == 'responders', 'Cortisol Responders', 'Cortisol Nonresponders')
        # Calculate means for each group (by status and responder type)
        group_means = data.groupby(['status', 'saa_responders', 'cortisol_responders']).agg({'negative_image': 'mean'}).reset_index()

    except KeyError as e:
        # Handle missing categorization columns
        print(f"Error categorizing responder states: {e}")
        raise  # Re-raise the exception

    # Perform the Two-Way ANOVA
    model = ols('negative_image ~ C(status) * C(saa_responders) * C(cortisol_responders)', data=data).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)

    return group_means, anova_table

def analyze_cortisol_data(data: pd.DataFrame) -> tuple:
    """
    Analyzes cortisol data by performing MANOVA tests.
    
    Parameters:
    data (pd.DataFrame): The DataFrame for cortisol analysis
    
    Returns:
    tuple:
        - scipy.stats._stats_py.F_onewayResult: ANOVA results for NC group (cortisol baseline by phase)
        - scipy.stats._stats_py.F_onewayResult: ANOVA results for NC group (cortisol change by phase)
        - scipy.stats._stats_py.F_onewayResult: ANOVA results for HC group (cortisol baseline by pill type)
        - scipy.stats._stats_py.F_onewayResult: ANOVA results for HC group (cortisol change by pill type)
        - pd.DataFrame: Filtered data for NC group
        - pd.DataFrame: Filtered data for HC group
    
    Raises:
    KeyError: If the required columns are missing
    """
    # Ensure the cortisol_change column is created
    if 'cortisol_change' not in data.columns:
        if 'change_CPS_cortisol_level' in data.columns:
            data['cortisol_change'] = data['change_CPS_cortisol_level']
        else:
            raise KeyError("Missing required column: 'change_CPS_cortisol_level'. Please ensure it exists in the dataset.")

    
    try:
        # Filter NC and HC groups
        nc_data = data[data['status'] == 'NC']
        hc_data = data[data['status'] == 'HC']

        # One-way ANOVA for NC group (cortisol baseline by phase)
        follicular_nc = nc_data[nc_data['phase'] == 'follicular']['cortisol_level_baseline']
        luteal_nc = nc_data[nc_data['phase'] == 'luteal']['cortisol_level_baseline']
        anova_nc_baseline = f_oneway(follicular_nc, luteal_nc)

        # One-way ANOVA for NC group (cortisol change by phase)
        follicular_nc_change = nc_data[nc_data['phase'] == 'follicular']['cortisol_change']
        luteal_nc_change = nc_data[nc_data['phase'] == 'luteal']['cortisol_change']
        anova_nc_change = f_oneway(follicular_nc_change, luteal_nc_change)

        # One-way ANOVA for HC group (cortisol baseline by pill type)
        monophasic_hc = hc_data[hc_data['pill_type'] == 'monophasic']['cortisol_level_baseline']
        triphasic_hc = hc_data[hc_data['pill_type'] == 'triphasic']['cortisol_level_baseline']
        anova_hc_baseline = f_oneway(monophasic_hc, triphasic_hc)

        # One-way ANOVA for HC group (cortisol change by pill type)
        monophasic_hc_change = hc_data[hc_data['pill_type'] == 'monophasic']['cortisol_change']
        triphasic_hc_change = hc_data[hc_data['pill_type'] == 'triphasic']['cortisol_change']
        anova_hc_change = f_oneway(monophasic_hc_change, triphasic_hc_change)

        return anova_nc_baseline, anova_nc_change, anova_hc_baseline, anova_hc_change, nc_data, hc_data
    except KeyError as e:
        # Handle missing contingency table columns
        print(f"Error accessing contingency table columns: {e}")
        raise  # Re-raise the exception

