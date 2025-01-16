import unittest
import pandas as pd
import sys
sys.path.append(r'C:\Users\matan\OneDrive\שולחן העבודה\python\project\src')
sys.path.append(r"C:\Users\matan\OneDrive\שולחן העבודה\python\project\src\functions")
from objects.initializeFile import InitializeFile
from functions.calculate import chi_square, analyze_saa_response
from functions.visualization import (
    plot_difference_sAA_responses,
    statistics_of_sAA_responses,
    plot_positive_images_responses,
    plot_negative_images_responses,
    plot_cortisol_phase_pill_effects,
)

class TestProjectFunctionsAdvanced(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize the file once for all tests
        cls.file = InitializeFile().file

    def test_initialize_file_columns_and_data(self):
        """
        Test that InitializeFile creates the required DataFrame with correct columns and data.
        """
        self.assertFalse(self.file.empty, "DataFrame is empty")
        required_columns = [
            'age', 'BMI', 'sAA_level_baseline', 'change_image_sAA_level',
            'cortisol_level_baseline', 'change_CPS_cortisol_level',
            'positive_image', 'negative_image'
        ]
        for column in required_columns:
            self.assertIn(column, self.file.columns, f"Missing column: {column}")

        # Verify data types for specific columns
        self.assertTrue(pd.api.types.is_numeric_dtype(self.file['age']), "Age column should be numeric")
        self.assertTrue(pd.api.types.is_numeric_dtype(self.file['BMI']), "BMI column should be numeric")

    def test_chi_square_results(self):
        """
        Test the chi_square function with mock data.
        """
        prepared_data = pd.DataFrame({
            'Group': ['NC', 'HC'],
            'Responders': [20, 18],
            'Non-Responders': [10, 12]
        })
        chi2, p, _ = chi_square(prepared_data)

        # Verify chi-square results
        self.assertGreater(chi2, 0, "Chi-square value should be positive")
        self.assertGreaterEqual(p, 0, "p-value should be >= 0")
        self.assertLessEqual(p, 1, "p-value should be <= 1")

    def test_analyze_saa_response_accuracy(self):
        """
        Test analyze_saa_response for valid output structure and meaningful results.
        """
        results = analyze_saa_response(self.file)

        # Check the structure of the results
        self.assertIn('anova_results', results, "Missing 'anova_results' in output")
        self.assertIn('effect_size', results, "Missing 'effect_size' in output")
        self.assertIn('summary_statistics', results, "Missing 'summary_statistics' in output")

        # Verify numerical correctness
        self.assertIsInstance(results['anova_results']['f_statistic'], float, "F-statistic should be a float")
        self.assertIsInstance(results['anova_results']['p_value'], float, "p-value should be a float")
        self.assertGreater(results['anova_results']['f_statistic'], 0, "F-statistic should be positive")
        self.assertGreaterEqual(results['anova_results']['p_value'], 0, "p-value should be >= 0")
        self.assertLessEqual(results['anova_results']['p_value'], 1, "p-value should be <= 1")

    def test_plot_difference_sAA_responses_no_exceptions(self):
        """
        Test that plot_difference_sAA_responses runs without exceptions.
        """
        try:
            plot_difference_sAA_responses(self.file)
        except Exception as e:
            self.fail(f"plot_difference_sAA_responses raised an exception: {e}")

    def test_statistics_of_sAA_responses_structure(self):
        """
        Test that statistics_of_sAA_responses produces a valid output without errors.
        """
        results = analyze_saa_response(self.file)

        try:
            statistics_of_sAA_responses(results)
        except Exception as e:
            self.fail(f"statistics_of_sAA_responses raised an exception: {e}")

    def test_visualization_functions(self):
        """
        Test that visualization functions run without errors and plot correctly.
        """
        try:
            plot_positive_images_responses(self.file)
            plot_negative_images_responses(self.file)
        except Exception as e:
            self.fail(f"Visualization function raised an exception: {e}")

    def test_missing_columns_error_handling(self):
        """
        Test that functions handle missing columns gracefully.
        """
        modified_file = self.file.copy()
        modified_file.drop(columns=['sAA_level_baseline'], inplace=True)

        with self.assertRaises(KeyError) as context:
            analyze_saa_response(modified_file)
        self.assertIn('sAA_level_baseline', str(context.exception))

    def test_edge_cases(self):
        """
        Test edge cases such as empty DataFrame or extreme values.
        """
        empty_file = pd.DataFrame()

        # Test empty DataFrame for missing columns
        with self.assertRaises(KeyError) as context:
            analyze_saa_response(empty_file)
        self.assertIn('change_image_sAA_level', str(context.exception))
        self.assertIn('change_CPS_cortisol_level', str(context.exception))
        self.assertIn('sAA_level_baseline', str(context.exception))

        # Test extreme values
        extreme_file = self.file.copy()
        extreme_file['sAA_level_baseline'] = extreme_file['sAA_level_baseline'] * 1e6  # Inflate values

        try:
            analyze_saa_response(extreme_file)
        except Exception as e:
            self.fail(f"analyze_saa_response failed with extreme values: {e}")


class MockAnovaResult:
    """
    Mock class to simulate ANOVA result objects for testing.
    """
    def __init__(self, pvalue):
        self.pvalue = pvalue

class TestProjectFunctionsAdvanced(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file = InitializeFile().file

    def test_initialize_file_columns_and_data(self):
        self.assertFalse(self.file.empty, "DataFrame is empty")
        required_columns = [
            'age', 'BMI', 'sAA_level_baseline', 'change_image_sAA_level',
            'cortisol_level_baseline', 'change_CPS_cortisol_level',
            'positive_image', 'negative_image'
        ]
        for column in required_columns:
            self.assertIn(column, self.file.columns, f"Missing column: {column}")

    def test_chi_square_results(self):
        prepared_data = pd.DataFrame({
            'Group': ['NC', 'HC'],
            'Responders': [20, 18],
            'Non-Responders': [10, 12]
        })
        chi2, p, _ = chi_square(prepared_data)
        self.assertGreater(chi2, 0)
        self.assertGreaterEqual(p, 0)
        self.assertLessEqual(p, 1)

class TestPlotCortisolPhasePillEffects(unittest.TestCase):

    def test_valid_data(self):
        nc_data = pd.DataFrame({
            'phase': ['follicular', 'luteal'],
            'cortisol_level_baseline': [0.2, 0.1],
            'cortisol_change': [0.05, 0.02]
        })
        hc_data = pd.DataFrame({
            'pill_type': ['monophasic', 'triphasic'],
            'cortisol_level_baseline': [0.15, 0.25],
            'cortisol_change': [0.03, 0.04]
        })
        anova_nc_baseline = MockAnovaResult(pvalue=0.05)
        anova_nc_change = MockAnovaResult(pvalue=0.01)
        anova_hc_baseline = MockAnovaResult(pvalue=0.03)
        anova_hc_change = MockAnovaResult(pvalue=0.02)
        try:
            plot_cortisol_phase_pill_effects(
                anova_nc_baseline, anova_nc_change,
                anova_hc_baseline, anova_hc_change,
                nc_data, hc_data
            )
        except Exception as e:
            self.fail(f"plot_cortisol_phase_pill_effects raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()

