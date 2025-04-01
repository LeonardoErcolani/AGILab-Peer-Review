import streamlit as st
import pandas as pd
import icc  # Importing ICC computation functions

# Set up Streamlit page layout (Full Width)
st.set_page_config(layout="wide", page_title="LLM's Scores Evaluation: ICC Computation", page_icon="📊")

# Title and instructions
st.title("📊 LLM's Scores Evaluation: ICC Computation")
st.markdown("Upload a **CSV file** containing LLM evaluation scores and compute **Intraclass Correlation Coefficients (ICC)**.")

# **Two Side-by-Side Containers**
container_left, container_right = st.columns([1, 2])  # Left (Filters) | Right (ICC Results + Heatmaps)

# **LEFT: File Upload & Selection Filters**
with container_left:
    st.header("📂 Upload & Selection")

    # File uploader
    uploaded_file = st.file_uploader("Upload Your CSV", type=["csv"])
    st.markdown("""
    **File Requirements:**
    - The file must be in **CSV format**.
    - It should contain the following columns:
    - **assessor**: Identifier for the assessor (e.g., evaluator name or ID).
    - **respondent**: Identifier for the respondent (e.g., participant name or ID).
    - **criterion_X**: Columns starting with "criterion" representing evaluation criteria (e.g., criterion_1, criterion_2, etc.).""")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, delimiter=",", dtype=str)  # Read as string first

        required_columns = ["assessor", "respondent"]
        criterion_columns = [col for col in df.columns if col.startswith("criterion")]

        if not all(col in df.columns for col in required_columns) or len(criterion_columns) < 1:
            st.error("❌ Invalid CSV format.")
        else:
            st.success("✅ CSV format is valid!")

            # Sidebar filters
            st.subheader("🔍 Select Filters")

            # Extract Unique Options
            all_assessors = sorted(df["assessor"].unique())
            all_respondents = sorted(df["respondent"].unique())
            all_criteria = criterion_columns

            # **Assessors Selection with 'Select All'**
            select_all_assessors = st.checkbox("Select All Assessors", value=True)
            selected_assessors = st.multiselect(
                "Select Assessors", all_assessors, default=all_assessors if select_all_assessors else []
            )

            # **Respondents Selection with 'Select All'**
            select_all_respondents = st.checkbox("Select All Respondents", value=True)
            selected_respondents = st.multiselect(
                "Select Respondents", all_respondents, default=all_respondents if select_all_respondents else []
            )

            # **Criteria Selection with 'Select All'**
            select_all_criteria = st.checkbox("Select All Criteria", value=True)
            selected_criteria = st.multiselect(
                "Select Criteria", all_criteria, default=all_criteria if select_all_criteria else []
            )

            # Filter data based on user selection
            df = icc.preprocess_data(df, selected_assessors, selected_respondents, selected_criteria)

            if df.empty:
                st.error("⚠️ No data available with selected filters.")

# **RIGHT: Display ICC Results + Heatmaps**
with container_right:
    st.header("📊 ICC Results & Heatmaps")

    if uploaded_file is not None and not df.empty:
        with st.spinner("⏳ Computing ICC... Please wait."):
            icc_results = icc.compute_icc(df)

        if icc_results is not None:
            st.subheader("📈 Overall ICC Results")
            st.dataframe(icc_results, use_container_width=True)  # Display ICC table
        else:
            st.warning("⚠️ Not enough respondents to compute ICC.")

        # **HEATMAPS: Display Below in 3 Columns**
        st.subheader("🔥 ICC Heatmaps (Assessor Agreement)")
        heatmap_cols = st.columns(3)  # 3-column layout for heatmaps

        # Compute assessor ICC
        icc_matrix_types = icc.compute_assessor_icc(df)

        # Generate heatmaps and display
        heatmap_files = icc.generate_heatmaps(icc_matrix_types)

        for i, (icc_type, heatmap_file) in enumerate(heatmap_files.items()):
            heatmap_cols[i].image(heatmap_file, caption=f"ICC Heatmap ({icc_type})", use_container_width=True)

