# AGILab-Peer-Review

We implement the peer review for a LLM panel at choice.
Technical details are @
### Link Arxiv
https://arxiv.org/abs/2412.09385

<img width="612" alt="image" src="https://github.com/user-attachments/assets/cde5b587-a923-4dd9-98c9-ebb69d94abb6" />

## ICC Analysis

The project includes an Intraclass Correlation Coefficient (ICC) analysis to evaluate the agreement between different LLM assessors. The analysis performs the following:

### Features
- Computes ICC scores (ICC1, ICC2, ICC3) between all assessors
- Generates heatmaps visualizing the ICC matrices
- Processes assessor scores across 9 different criteria
- Outputs detailed ICC analysis results

### Generated Files
- `melted_df.csv`: Long-format dataset for ICC computation
- `icc_matrices/*.csv`: ICC matrices for different ICC types
- `icc_heatmaps/*.png`: Heatmap visualizations of ICC scores
- `icc_full_results.csv`: Complete ICC analysis results

### Requirements
- Python packages: pandas, pingouin, seaborn, matplotlib
- Input file: `merged_llm_scores.csv` containing assessor scores

### Input Data Structure
The code expects an input CSV file (`merged_llm_scores.csv`) with the following structure:

1. **Required Columns:**
   - `assessor`: Column containing the identifiers for the LLMs/raters
   - `respondent`: Column containing the identifiers for the items being rated
   - Nine additional columns containing the criterion scores

2. **Data Format:**
   - Each row represents one assessment
   - Multiple assessors rate the same respondents
   - Scores should be numerical values

Example format of `merged_llm_scores.csv`:
```csv
assessor,respondent,criterion1,criterion2,...,criterion9
LLM1,item1,4,5,...,3
LLM1,item2,3,4,...,5
LLM2,item1,5,4,...,4
...
```

The script will automatically:
1. Transform this wide-format data into the required long format
2. Process it using the pingouin.intraclass_corr() function with:
   - targets = "respondent" (items being rated)
   - raters = "assessor" (LLMs doing the rating)
   - ratings = "Score" (the actual scores)

## Installation and Running Instructions

1. **Setup Environment:**
   ```bash
   # Clone the repository
   git clone [repository-url]
   cd AGILab-Peer-Review

   # Create and activate a virtual environment (optional but recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate

   # Install requirements
   pip install -r requirements.txt
   ```

2. **Prepare Data:**
   - Place your `merged_llm_scores.csv` file in the root directory
   - Ensure it follows the input data structure described above

3. **Run ICC Analysis:**
   ```bash
   # Run the analysis from the root directory
   python ICC/icc.py
   ```

4. **Check Results:**
   After running the script, you'll find:
   - ICC matrices in the `icc_matrices/` folder
   - Heatmap visualizations in the `icc_heatmaps/` folder
   - `melted_df.csv` and `icc_full_results.csv` in the root directory
