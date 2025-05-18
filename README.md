:nerd_face:
# README: Hormonal Contraceptives - Stress and Memory Responses Analysis

## Project Overview:
This project focuses on analyzing the effects of hormonal contraceptives (HC) versus natural cycling (NC) on physiological and cognitive responses.
In this project we created the dataset based on the article stated below.  

The primary objectives are:

1. Investigating differences in Cortisol and sAA responses to stress and emotional stimuli between HC and NC groups.
2. Analyzing memory performance for positive and negative emotional stimuli in both groups.
3. Conducting statistical analyses such as ANOVA and Chi-square tests to uncover significant patterns.

Link to the project summary: 
https://docs.google.com/document/d/1vFIpdaZ4GAX_lcSuaWWK1TUJAWx6nYx-bnnnrVglgs8/edit?usp=sharing

The article this project is based on: 
https://www.sciencedirect.com/science/article/pii/S030105111200227X?casa_token=6mF9uyf9pG0AAAAA:NttZLVmGWyY23ebrkeIKdyGmkCVWjnhCh-rrX68G-_GRPDRo_ByrC6Va1VWrBhtVsOIwUMflkA 


## Project Structure:
The project includes:

1. **Data Generation and Initialization**:
   - Synthetic data generation based on means and standard deviations from extracted graphs.
   - Data includes variables such as cortisol levels, sAA levels, BMI, and memory performance.

2. **Statistical Analysis**:
   - One-way ANOVA for group-level comparisons.
   - Two-way ANOVA for interaction effects between responders and non-responders.
   - Chi-square test for independence between groups.
   - Linear regression for trends.
   

3. **Visualization**:
   - Bar plots for group comparisons.
   - Heatmaps for interaction effects.
   - Custom annotations to highlight trends and statistical results.
   - Scatter plotts to highlight the difference between different subjects.

## Requirements to Run the Project: 

### Libraries
The project relies on the following Python libraries:
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `statsmodels`
- `scipy`

Install the required libraries using:
```bash
pip install pandas numpy matplotlib seaborn statsmodels scipy
```
### Input Data
Link to the dataset before adding the runtime simulated data:
https://drive.google.com/file/d/1nVZVmDqx3acpP1rcA6QXBXQwCeW2M7yt/view?usp=sharing

Link to the dataset after adding the runtime simulated data: 
This is the full dataset: 
https://drive.google.com/file/d/111uVm2qm3GnVWHJ4HI5ofEM6yOwBp8MN/view?usp=sharing

In InitializeFile(): 
Line 14:  file = pd.read_csv() 
put: 
```bash
C:-PATH-TO-DATA-IN-YOUR-COMPUTER
```
In Main(): 
Line 31:  data.to_csv()
put: 
```bash
C:-PATH-TO-OUTPUT-DATA-IN-YOUR-COMPUTER
```
### Folder Structure
Ensure the following directory structure:
```
project/
|-- main.py
|-- src/
    |-- objects/
        |-- initialize_file.py
        |-- __init__.py
    |-- functions/
        |-- visualization.py
        |-- calculate.py
        |-- general.py
        |-- __init__.py
    |-- __init__.py
|-- tests/
    |-- article_test.py
    |-- tests.py
    |-- __init__.py
```


## How to Run

1. **Initialization**:
   - `InitializeFile` creates the dataset with generated values.
   - Download the dataset 

3. **Key Functions**:
   - `plot_difference_sAA_responses`: Compares sAA changes between HC and NC groups.
   - `statistics_of_sAA_responses`: Visualizes ANOVA results and summary statistics for sAA responses.
   - `plot_positive_images_responses`: Analyzes memory performance for positive images.
   - `visualizions_two_way_anova`: Performs two-way ANOVA and visualizes results for stimuli.
   - `plot_negative_images_responses`: Analyzes memory performance for negative images.
   - `plot_effect_baseline_cortisol_sAA_linear_regression`: Calculates the Linear Regression of the effects of baseline cortisol and sAA on the results of the CPS tests.
   - `plot_cortisol_phase_pill_effect`: Analyzes the effects of pill type in HC women and cycle phase in NC women on baseline cortisol.
   - `plot_difference_of_cortisol_chi2`: Visualizes Chi-square test results.

4. **Execution**:
Run the script from the root directory using:
```bash
python main.py
```

## Outputs
- **Plots**:
  - Bar plots comparing HC and NC groups for various metrics.
  - Heatmaps showing interaction effects of responders/non-responders, NC/HC based on memory performance.
  - Scatter plots showing the effcts of baseline SAA and Cortisol levels on the reaction to the CPS test HC and NC.
    
- **Statistical Tables**:
  - ANOVA tables visualized as bar plots.
  - Summary tables for sAA and cortisol responses.
  - Linear Regression graphs.
  - ChiSquare represented as bar plot.

## Health check (Lint/Tests/Tests-Coverage):
#### Lint Project:
Check formatting, type hinting, lint code & docstrings
```bash
tox run -e lint
```
#### Test Project: 
Run all tests on diffrent python versions and produce tests-coverage and tests-results reports (make sure tested versions installed before run):
```bash
tox run -f test
```
#### Lint and Test project (on diffrent python versions):
```bash
tox run
```

## Build/pack the project (should run on every version change)
```bash
python -m build
```

#### Package documentation:
```bash
tox run -e docs
```

## Example Workflow
```python
# Initialize dataset
file = InitializeFile().file

# Plot differences in sAA responses
plot_difference_sAA_responses(file)

# Analyze and visualize sAA response statistics
results = analyze_saa_response(file)
statistics_of_sAA_responses(results)

# Analyze positive and negative image memory performance
plot_positive_images_responses(file)
calculate_two_way_anova_with_viz_positive(file)
plot_negative_images_responses(file)
calculate_two_way_anova_with_viz_negative(file)
```

## Notes
- Ensure all paths are correctly specified for importing modules and accessing datasets.
- Use `np.random.seed()` to reproduce synthetic data consistently.
