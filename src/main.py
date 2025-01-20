import sys

# Add custom module paths for importing project-specific functions and objects
sys.path.append(r'C:/Users/matan/OneDrive/שולחן העבודה/python/project/src/objects')
sys.path.append(r'C:/Users/matan/OneDrive/שולחן העבודה/python/project/src/functions')

# Import project-specific modules
from objects.initializeFile import InitializeFile
from functions.general import prepare_data_from_csv
from functions.visualization import (
    plot_difference_sAA_responses,
    statistics_of_sAA_responses,
    plot_positive_images_responses,
    plot_negative_images_responses,
    plot_difference_of_cortisol_chi2,
    plot_affect_basleline_cortisol_sAA_linear_regressions,
    heatMap,
    vizualizations_two_way_anova,
    plot_cortisol_phase_pill_effects
)
from functions.calculate import (
    analyze_saa_response,
    calculate_two_way_anova_with_viz_positive,
    calculate_two_way_anova_with_viz_negative,
    chi_square,
    analyze_cortisol_data
)

# Initialize file object and save its content to a CSV file
data = InitializeFile().file
data.to_csv(r'C:\Users\matan\OneDrive\מסמכים\new_output.csv', index=False)

'''
Is there a difference in the cortisol response to a stress test (Cold Pressor Stress - CPS)
between HC womnen and NC women?
'''
# Prepare data for chi-square analysis and visualization
prepared_data = prepare_data_from_csv(data)
chi2, p, contingency_table = chi_square(prepared_data)
plot_difference_of_cortisol_chi2(prepared_data, chi2, p)

'''
Is there a difference in the noradrenaline (sAA)
response to emotional stimuli between women in the HC group and the NC group?
'''
# Plot differences in sAA responses
plot_difference_sAA_responses(data)
# Analyze sAA responses and display statistics (one way ANOVA) 
results = analyze_saa_response(data)
statistics_of_sAA_responses(results)

'''
Do baseline levels of cortisol and sAA affect stress test response
in women from the HC group differently than in women from the NC group?
'''
# Plot linear regressions for cortisol and sAA responses
plot_affect_basleline_cortisol_sAA_linear_regressions(data)

'''
Is there a relationship between the phase of the cycle in the NC
group and the type of pills in the HC group and the initial cortisol and the change in cortisol?
'''
# Analyze cortisol data and visualize phase and pill effects
anova_nc_baseline, anova_nc_change, anova_hc_baseline, anova_hc_change, nc_data, hc_data = analyze_cortisol_data(data)
plot_cortisol_phase_pill_effects(anova_nc_baseline, anova_nc_change, anova_hc_baseline, anova_hc_change, nc_data, hc_data)

'''
Is there a difference in memory for negative stimuli between
women in the HC group and women in the NC group, according to the cortisol response and the sAA response?
'''
# Analyze and visualize responses to negative images
plot_negative_images_responses(data)
group_means_negative, anova_table_negative = calculate_two_way_anova_with_viz_negative(data)
heatMap(group_means_negative, 'negative_image')
vizualizations_two_way_anova(anova_table_negative)

'''
Is there a difference in memory for positive stimuli between women in the HC group
and women in the NC group, according to the cortisol response and the sAA response?
'''
# Analyze and visualize responses to positive images
plot_positive_images_responses(data)
group_means_positive, anova_table_positive = calculate_two_way_anova_with_viz_positive(data)
heatMap(group_means_positive, 'positive_image')
vizualizations_two_way_anova(anova_table_positive)

