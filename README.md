# AGILab-Peer-Review

We implement the peer review for a LLM panel at choice.
Technical details are at:
#### Link Arxiv
https://arxiv.org/abs/2412.09385


The following chart illustrates the concet behind an Automated LLM's Peer Review System:

<img width="612" alt="image" src="https://github.com/user-attachments/assets/cde5b587-a923-4dd9-98c9-ebb69d94abb6" />


## LLM's Scores Evaluation: ICC Computation

This project provides a **Streamlit-based web application** for evaluating LLM (Large Language Model) scores using **Intraclass Correlation Coefficients (ICC)**. The application allows users to upload a CSV file containing evaluation scores, filter the data, compute ICC values, and visualize the results through heatmaps.

### Features

1. **File Upload**:
   - Upload a CSV file containing evaluation scores.
   - The file must follow a specific structure (see [File Requirements](#file-requirements)).

2. **Data Filtering**:
   - Filter the data by assessors, respondents, and evaluation criteria.
   - Options to "Select All" or choose specific subsets.

3. **ICC Computation**:
   - Compute overall ICC values for the dataset.
   - Generate ICC matrices for assessor agreement.

4. **Heatmap Visualization**:
   - Visualize ICC matrices as heatmaps for better interpretability.

5. **Results Export**:
   - Save the melted dataset, ICC results, ICC matrices, and heatmaps in a structured `results/` folder.


### File Requirements

The uploaded CSV file must adhere to the following structure:

- **Columns**:
  - `assessor`: Identifier for the assessor (e.g., evaluator name or ID).
  - `respondent`: Identifier for the respondent (e.g., participant name or ID).
  - `criterion_X`: Columns starting with `criterion` representing evaluation criteria (e.g., `criterion_1`, `criterion_2`, etc.).

- **Example Data**:
  ```csv
  assessor,respondent,criterion_1,criterion_2,criterion_3
  Assessor1,Respondent1,4,3,...5
  Assessor2,Respondent1,4,3,...4
  Assessor1,Respondent2,5,4,...4
  ...
  ```

### Installation and Running Instructions

The app is available as a Hugging Face Space at https://huggingface.co/spaces/AGILab/ICC-Automation

Otherwise, if needed locally:

1. **Setup Environment:**
   ```bash
   # Clone the repository
   git clone <repository-url>
   cd <repository-folder>

   # Create and activate a virtual environment (optional but recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate

   # Install requirements
   pip install -r requirements.txt
   ```

2. **Run the Streamlit App:**
   ```bash
   streamlit run app.py
   ```



