import matplotlib.pyplot as plt
import sys
import seaborn as sns
from scipy.stats import f_oneway, linregress
sys.path.append(r'C:/Users/matan/OneDrive/שולחן העבודה/python/project/src/objects')
sys.path.append(r'C:/Users/matan/OneDrive/שולחן העבודה/python/project/src/functions')
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

file = InitializeFile().file
file.to_csv(r'C:\Users\matan\OneDrive\מסמכים\new_output.csv', index=False)

plot_difference_sAA_responses(file)
results = analyze_saa_response(file)
statistics_of_sAA_responses(results)

prepared_data = prepare_data_from_csv(file)
chi2, p, contingency_table = chi_square(prepared_data)
plot_difference_of_cortisol_chi2(prepared_data, chi2, p)

plot_positive_images_responses(file)
group_means_positive, anova_table_positive = calculate_two_way_anova_with_viz_positive(file)
heatMap(group_means_positive, 'positive_image')
vizualizations_two_way_anova(anova_table_positive)

plot_negative_images_responses(file)
group_means_negative, anova_table_negative = calculate_two_way_anova_with_viz_negative(file)
heatMap(group_means_negative, 'negative_image')
vizualizations_two_way_anova(anova_table_negative)

plot_affect_basleline_cortisol_sAA_linear_regressions(file)

anova_nc_baseline, anova_nc_change, anova_hc_baseline, anova_hc_change, nc_data, hc_data = analyze_cortisol_data(file)
plot_cortisol_phase_pill_effects(anova_nc_baseline, anova_nc_change, anova_hc_baseline, anova_hc_change, nc_data, hc_data)









