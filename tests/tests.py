"""Unit tests for project functions, including data initialization, statistical analysis and visualization.

Modules:
    - unittest: Framework for writing and running tests.
    - pandas (pd): Data manipulation and analysis library.
    - sys: Provides access to system-specific parameters and functions.

Custom Modules:
    - InitializeFile: Initializes project-related data files.
    - chi_square: Performs chi-square analysis.
    - analyze_saa_response: Analyzes sAA response data.
    - Visualization functions: Provides plotting capabilities for various analyses.

Notes:
    - All tests validate function behavior, data integrity, and visualization output.
    - The script expects specific data structures and column names.
"""

import sys
import unittest

import pandas as pd

# Adding paths for importing custom modules
sys.path.append(r"C:\Users\matan\OneDrive\שולחן העבודה\python\project")
sys.path.append(r"C:\Users\matan\OneDrive\שולחן העבודה\python\project\src")
sys.path.append(r"C:\Users\matan\OneDrive\שולחן העבודה\python\project\src\functions")

# Importing custom modules
import pytest

from src.functions.calculate import analyze_saa_response, chi_square
from src.functions.visualization import (
    plot_cortisol_phase_pill_effects,
    plot_difference_saa_responses,
    plot_negative_images_responses,
    plot_positive_images_responses,
    statistics_of_saa_responses,
)
from src.objects.initialize_file import InitializeFile


class TestProjectFunctionsAdvanced(unittest.TestCase):
    """Unit tests for advanced project functions, including data initialization,

    statistical analysis, and visualization.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Set up class-level resources, including initializing the data file.

        This method runs once before all tests in this class.
        """
        cls.file = InitializeFile().file

    def test_initialize_file_columns_and_data(self) -> None:
        """Test that InitializeFile creates the required DataFrame with correct columns and data.

        Verifies:
        - DataFrame is not empty
        - Required columns exist
        - Specific columns have numeric data types
        """
        assert not self.file.empty, "DataFrame is empty"
        required_columns = [
            "age", "BMI", "sAA_level_baseline", "change_image_sAA_level",
            "cortisol_level_baseline", "change_CPS_cortisol_level",
            "positive_image", "negative_image"
        ]
        for column in required_columns:
            assert column in self.file.columns, f"Missing column: {column}"

        # Verify data types for specific columns
        assert pd.api.types.is_numeric_dtype(self.file["age"]), "Age column should be numeric"
        assert pd.api.types.is_numeric_dtype(self.file["BMI"]), "BMI column should be numeric"

    def test_chi_square_results(self) -> None:
        """Test the chi_square function with mock data to ensure correct output values.

        Verifies:
        - Chi-square statistic is positive
        - p-value is within the range [0, 1]
        """
        prepared_data = pd.DataFrame({
            "Group": ["NC", "HC"],
            "Responders": [20, 18],
            "Non-Responders": [10, 12]
        })
        chi2, p, _ = chi_square(prepared_data)

        # Verify chi-square results
        assert chi2 > 0, "Chi-square value should be positive"
        assert p >= 0, "p-value should be >= 0"
        assert p <= 1, "p-value should be <= 1"

    def test_analyze_saa_response_accuracy(self) -> None:
        """Test analyze_saa_response for valid output structure and meaningful results.

        Verifies:
        - Output structure contains expected keys
        - Numerical results are valid
        """
        results = analyze_saa_response(self.file)

        # Check the structure of the results
        assert "anova_results" in results, "Missing 'anova_results' in output"
        assert "effect_size" in results, "Missing 'effect_size' in output"
        assert "summary_statistics" in results, "Missing 'summary_statistics' in output"

        # Verify numerical correctness
        assert isinstance(results["anova_results"]["f_statistic"], float), "F-statistic should be a float"
        assert isinstance(results["anova_results"]["p_value"], float), "p-value should be a float"
        assert results["anova_results"]["p_value"] >= 0, "p-value should be >= 0"
        assert results["anova_results"]["p_value"] <= 1, "p-value should be <= 1"

    def test_plot_difference_saa_responses_no_exceptions(self) -> None:
        """Test that plot_difference_saa_responses runs without exceptions."""
        try:
            plot_difference_saa_responses(self.file)
        except Exception as e:
            self.fail(f"plot_difference_saa_responses raised an exception: {e}")

    def test_statistics_of_saa_responses_structure(self) -> None:
        """Test that statistics_of_saa_responses produces a valid output without errors."""
        results = analyze_saa_response(self.file)

        try:
            statistics_of_saa_responses(results)
        except Exception as e:
            self.fail(f"statistics_of_saa_responses raised an exception: {e}")

    def test_visualization_functions(self) -> None:
        """Test that visualization functions run without errors and produce expected results.

        Includes:
        - plot_positive_images_responses
        - plot_negative_images_responses
        """
        try:
            plot_positive_images_responses(self.file)
            plot_negative_images_responses(self.file)
        except Exception as e:
            self.fail(f"Visualization function raised an exception: {e}")

    def test_missing_columns_error_handling(self) -> None:
        """Test that functions handle missing columns gracefully.

        Verifies:
        - analyze_saa_response raises KeyError when required columns are missing
        """
        modified_file = self.file.copy()
        modified_file = modified_file.drop(columns=["change_image_sAA_level"])

        with pytest.raises(KeyError) as context:
            analyze_saa_response(modified_file)
        assert "change_image_sAA_level" in str(context.value)

    def test_edge_cases(self) -> None:
        """Test edge cases such as empty DataFrame or extreme values."""
        empty_file = pd.DataFrame()

        # Test empty DataFrame for missing columns
        with pytest.raises(KeyError) as context:
            analyze_saa_response(empty_file)
        assert "change_image_sAA_level" in str(context.value)

        # Test extreme values
        extreme_file = self.file.copy()
        extreme_file["change_image_sAA_level"] = extreme_file["change_image_sAA_level"] * 1e6  # Inflate values

        try:
            analyze_saa_response(extreme_file)
        except Exception as e:
            self.fail(f"analyze_saa_response failed with extreme values: {e}")

class MockAnovaResult:
    """Mock class to simulate ANOVA result objects for testing."""
    def __init__(self, pvalue: float) -> None:
        self.pvalue = pvalue

class TestPlotCortisolPhasePillEffects(unittest.TestCase):
    """Unit tests for the plot_cortisol_phase_pill_effects function."""

    def test_valid_data(self) -> None:
        """Test plot_cortisol_phase_pill_effects with valid data to ensure no exceptions occur."""
        nc_data = pd.DataFrame({
            "phase": ["follicular", "luteal"],
            "cortisol_level_baseline": [0.2, 0.1],
            "cortisol_change": [0.05, 0.02]
        })
        hc_data = pd.DataFrame({
            "pill_type": ["monophasic", "triphasic"],
            "cortisol_level_baseline": [0.15, 0.25],
            "cortisol_change": [0.03, 0.04]
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
