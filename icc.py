import os
import pandas as pd
import pingouin as pg
import seaborn as sns
import matplotlib.pyplot as plt

# Set up output directories
RESULTS_FOLDER = "results/"
HEATMAPS_FOLDER = os.path.join(RESULTS_FOLDER, "icc_heatmaps/")
MATRICES_FOLDER = os.path.join(RESULTS_FOLDER, "icc_matrices/")
os.makedirs(HEATMAPS_FOLDER, exist_ok=True)
os.makedirs(MATRICES_FOLDER, exist_ok=True)


def preprocess_data(df, selected_assessors, selected_respondents, selected_criteria):
    """
    Filters the dataset based on user-selected assessors, respondents, and criteria.
    Ensures data is properly formatted for ICC computation.
    """
    df = df[df["assessor"].isin(selected_assessors) & df["respondent"].isin(selected_respondents)]
    df = df[["assessor", "respondent"] + selected_criteria]

    # Convert all columns to numeric (handling comma decimals)
    for col in selected_criteria:
        df[col] = df[col].str.replace(",", ".").astype(float)

    # Ensure 'assessor' and 'respondent' are treated as categorical
    df["assessor"] = df["assessor"].astype(str)
    df["respondent"] = df["respondent"].astype(str)

    return df


def compute_icc(df):
    """
    Computes the overall ICC (Intraclass Correlation Coefficient).
    Saves the melted DataFrame and ICC results to the results folder.
    """
    melted_df = df.melt(id_vars=["assessor", "respondent"], var_name="Criterion", value_name="Score")
    melted_df_path = os.path.join(RESULTS_FOLDER, "melted_dataframe.csv")
    melted_df.to_csv(melted_df_path, index=False)

    if melted_df["respondent"].nunique() >= 5:
        icc_results = pg.intraclass_corr(data=melted_df, targets="respondent", raters="assessor", ratings="Score").round(3)
        icc_results_path = os.path.join(RESULTS_FOLDER, "icc_results.csv")
        icc_results.to_csv(icc_results_path, index=False)
        return icc_results
    else:
        return None


def compute_assessor_icc(df):
    """
    Computes ICC matrices between assessors and saves them to the matrices folder.
    """
    melted_df = df.melt(id_vars=["assessor", "respondent"], var_name="Criterion", value_name="Score")
    assessors = df["assessor"].unique()
    icc_matrix_types = {icc_type: pd.DataFrame(index=assessors, columns=assessors, dtype=float) for icc_type in ["ICC1", "ICC2", "ICC3"]}

    for assessor1 in assessors:
        for assessor2 in assessors:
            if assessor1 != assessor2:
                subset = melted_df[melted_df["assessor"].isin([assessor1, assessor2])]

                if subset["respondent"].nunique() >= 5:
                    icc_results = pg.intraclass_corr(
                        data=subset, targets="respondent", raters="assessor", ratings="Score"
                    ).round(3)

                    for icc_type in ["ICC1", "ICC2", "ICC3"]:
                        icc_matrix_types[icc_type].loc[assessor1, assessor2] = icc_results.set_index("Type").loc[icc_type]["ICC"]

    # Save ICC matrices to the matrices folder
    for icc_type, icc_matrix in icc_matrix_types.items():
        matrix_file = os.path.join(MATRICES_FOLDER, f"icc_matrix_{icc_type}.csv")
        icc_matrix.to_csv(matrix_file)

    return icc_matrix_types


def generate_heatmaps(icc_matrix_types):
    """
    Generates and saves heatmaps for ICC matrices in the heatmaps folder.
    """
    heatmap_files = {}
    for icc_type, icc_matrix in icc_matrix_types.items():
        plt.figure(figsize=(8, 6))
        sns.heatmap(icc_matrix.astype(float), annot=True, cmap="coolwarm", linewidths=0.5, fmt=".2f")
        plt.title(f"Assessor ICC Matrix ({icc_type})")
        plt.xlabel("Assessor (LLM)")
        plt.ylabel("Assessor (LLM)")
        plt.xticks(rotation=45)
        plt.yticks(rotation=0)
        heatmap_file = os.path.join(HEATMAPS_FOLDER, f"icc_matrix_{icc_type}.png")
        plt.savefig(heatmap_file)
        plt.close()
        heatmap_files[icc_type] = heatmap_file

    return heatmap_files
