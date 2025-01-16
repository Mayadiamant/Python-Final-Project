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

    # Rest of the function logic...

def analyze_saa_response(data) -> dict:
    """
    Analyze sAA response differences between HC and NC groups
    
    Parameters:
    data (pd.DataFrame): Input data containing status and sAA measurements
    
    Returns:
    dict: Dictionary containing all statistical results and summary statistics
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
    Calculate Cohen's d effect size
    """
    n1, n2 = len(group1), len(group2)
    var1, var2 = group1.var(), group2.var()
    
    # Pooled standard deviation
    pooled_sd = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    
    # Cohen's d
    d = (group1.mean() - group2.mean()) / pooled_sd
    return d


def chi_square(df):
    """
    Performs chi-square test on the data.
    """
    contingency_table = df[["Responders", "Non-Responders"]].values
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    return chi2, p, contingency_table

def calculate_two_way_anova_with_viz_positive(data):
    # Categorize into responders and non-responders
    data['saa_responders'] = np.where(data['responsive_state_SAA'] == 'responders', 'SAA Responders', 'SAA Nonresponders')
    data['cortisol_responders'] = np.where(data['responsive_state_cortisol'] == 'responders', 'Cortisol Responders', 'Cortisol Nonresponders')

    # Calculate means for each group (by status and responder type)
    group_means = data.groupby(['status', 'saa_responders', 'cortisol_responders']).agg({'positive_image': 'mean'}).reset_index()

    # Perform the Two-Way ANOVA
    model = ols('positive_image ~ C(status) * C(saa_responders) * C(cortisol_responders)', data=data).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)

    return group_means, anova_table

def calculate_two_way_anova_with_viz_negative(data):
    # Categorize into responders and non-responders
    data['saa_responders'] = np.where(data['responsive_state_SAA'] == 'responders', 'SAA Responders', 'SAA Nonresponders')
    data['cortisol_responders'] = np.where(data['responsive_state_cortisol'] == 'responders', 'Cortisol Responders', 'Cortisol Nonresponders')

    # Calculate means for each group (by status and responder type)
    group_means = data.groupby(['status', 'saa_responders', 'cortisol_responders']).agg({'negative_image': 'mean'}).reset_index()

    # Perform the Two-Way ANOVA
    model = ols('negative_image ~ C(status) * C(saa_responders) * C(cortisol_responders)', data=data).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)

    return group_means, anova_table

# Function to perform analysis and visualization
def analyze_cortisol_data(data):
    # Ensure the cortisol_change column is created
    if 'cortisol_change' not in data.columns:
        if 'change_CPS_cortisol_level' in data.columns:
            data['cortisol_change'] = data['change_CPS_cortisol_level']
        else:
            raise KeyError("Missing required column: 'change_CPS_cortisol_level'. Please ensure it exists in the dataset.")

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

