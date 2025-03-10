import os
import pandas as pd
import pingouin as pg
import seaborn as sns
import matplotlib.pyplot as plt

# Load the merged CSV file
file_path = "merged_llm_scores.csv"  # Change this to your actual file name
df = pd.read_csv(file_path)

# Ensure output folder exists for heatmaps
HEATMAPS_FOLDER = "icc_heatmaps/"
os.makedirs(HEATMAPS_FOLDER, exist_ok=True)

# Ensure output folder exists for ICC matrices
ICC_MATRICES_FOLDER = "icc_matrices/"
os.makedirs(ICC_MATRICES_FOLDER, exist_ok=True)

# Step 1: Keep only necessary columns
df = df.iloc[:, :11]  # Keep Assessor, Respondent, and 9 Criterion Scores

# Step 2: Reshape the data into long format for ICC computation
melted_df = df.melt(id_vars=["assessor", "respondent"], var_name="Criterion", value_name="Score")

# Save melted dataset
melted_df.to_csv("melted_df.csv", index=False)
print("\n✅ Melted dataset saved as `melted_df.csv`")

# Step 3: Compute ICC for each Assessor pair
assessors = df["assessor"].unique()
icc_matrix_types = {icc_type: pd.DataFrame(index=assessors, columns=assessors, dtype=float) for icc_type in ["ICC1", "ICC2", "ICC3"]}

for assessor1 in assessors:
    for assessor2 in assessors:
        if assessor1 != assessor2:
            # Filter scores for both assessors
            subset = melted_df[melted_df["assessor"].isin([assessor1, assessor2])]

            # Ensure at least 5 respondents for valid ICC computation
            if subset["respondent"].nunique() >= 5:
                icc_results = pg.intraclass_corr(
                    data=subset, targets="respondent", raters="assessor", ratings="Score"
                ).round(3)

                for icc_type in ["ICC1", "ICC2", "ICC3"]:
                    icc_matrix_types[icc_type].loc[assessor1, assessor2] = icc_results.set_index("Type").loc[icc_type]["ICC"]



# Ensure output folder exists for ICC matrices
ICC_MATRICES_FOLDER = "icc_matrices/"
os.makedirs(ICC_MATRICES_FOLDER, exist_ok=True)

# Step 4: Save ICC Matrices & Extended Results
for icc_type, icc_matrix in icc_matrix_types.items():
    icc_matrix_file = os.path.join(ICC_MATRICES_FOLDER, f"icc_matrix_{icc_type}.csv")
    icc_matrix.to_csv(icc_matrix_file, index=True)
    print(f"✅ ICC matrix ({icc_type}) saved as `{icc_matrix_file}`")

    # Generate Heatmap for each ICC Type
    plt.figure(figsize=(10, 8))
    sns.heatmap(icc_matrix.astype(float), annot=True, cmap="coolwarm", linewidths=0.5, fmt=".2f")
    plt.title(f"Assessor ICC Matrix ({icc_type})")
    plt.xlabel("Assessor (LLM)")
    plt.ylabel("Assessor (LLM)")
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    heatmap_file = os.path.join(HEATMAPS_FOLDER, f"icc_matrix_{icc_type}.png")
    plt.savefig(heatmap_file)
    plt.close()
    print(f"✅ ICC heatmap ({icc_type}) saved as `{heatmap_file}`")


# Step 5: Save Extended ICC Results
full_icc_results = pg.intraclass_corr(data=melted_df, targets="respondent", raters="assessor", ratings="Score").round(3)
full_icc_results.to_csv("icc_full_results.csv", index=False)
print("\n✅ Full ICC results saved as `icc_full_results.csv`")
