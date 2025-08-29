import pandas as pd 
blocks_number = [1, 2, 3, 4, 5]

def average_HR(xlsx_path, blocks=blocks_number, HR_col="HR", block_col="block"):
    # ------------------------------------------------------------
    # Function: average_HR
    # ------------------------------------------------------------
    # 1) Load all sheets (participants) from a given Excel file.
    # 2) For each participant:
    #      - Compute mean and standard deviation of HR for each block (1–5).
    #      - Compute overall mean and standard deviation across all blocks.
    # 3) Return a DataFrame where each row = one participant,
    #    with columns for block-wise and overall statistics.
    # ------------------------------------------------------------
    
    sheets = pd.read_excel(xlsx_path, sheet_name=None)

    rows = []
    for sheet_name, data in sheets.items():
        data = data[data["block"].isin(blocks)]
        data_grouped = data.groupby("block")["HR"].agg(["mean", "std"]).reindex(blocks)
        row = {"participant": str(sheet_name)}
        for b in blocks:
            row[f"mean_b{b}"] = data_grouped.loc[b, "mean"]
            row[f"sd_b{b}"]   = data_grouped.loc[b, "std"]

        # Overall mean and std across all blocks
        row["mean_all"] = data["HR"].mean()
        row["sd_all"]   = data["HR"].std()

        rows.append(row)

    return pd.DataFrame(rows)

# ============================================================
# LOAD AND SUMMARIZE DATA FOR EACH CONDITION
# ============================================================

cool_data = average_HR("/Users/margheritabisaglia/Library/CloudStorage/OneDrive-ScientificNetworkSouthTyrol/PhD/Courses/Python 2025/HR_cool_all.xlsx")
cold_data = average_HR("/Users/margheritabisaglia/Library/CloudStorage/OneDrive-ScientificNetworkSouthTyrol/PhD/Courses/Python 2025/HR_cold_all.xlsx")
warm_data = average_HR("/Users/margheritabisaglia/Library/CloudStorage/OneDrive-ScientificNetworkSouthTyrol/PhD/Courses/Python 2025/HR_warm_all.xlsx")
hot_data  = average_HR("/Users/margheritabisaglia/Library/CloudStorage/OneDrive-ScientificNetworkSouthTyrol/PhD/Courses/Python 2025/HR_hot_all.xlsx")

summary = {
    "cool": cool_data,
    "warm": warm_data,
    "cold": cold_data,
    "hot":  hot_data,
}

import matplotlib.pyplot as plt

# ============================================================
# STATISTICAL TESTS: One-way ANOVA across conditions
# - For each block (mean_b1 ... mean_b5)
# - For the overall mean (mean_all)
# ============================================================

# Define condition 
conditions = ["cool", "warm", "cold", "hot"]

from scipy import stats

def anova_across_conditions(summary_dict, measure_column, conditions_order):
    """Runs one-way ANOVA across conditions for a given measure column."""
    groups = []
    number_participant = {}
    for cond in conditions_order:
        values = summary_dict[cond][measure_column].dropna().values
        groups.append(values)
        number_participant[cond] = len(values)
        
    F, p = stats.f_oneway(*groups)
    print(f"{measure_column}: ANOVA F={F:.3f}, p={p:.4g} | Number participant: { number_participant}")

# Run ANOVA for each block
for b in [1, 2, 3, 4, 5]:
    anova_across_conditions(summary, f"mean_b{b}", conditions)

# Run ANOVA for overall mean
anova_across_conditions(summary, "mean_all", conditions)

# ============================================================
# HISTOGRAMS
# ============================================================
# For each block (1–5):
#   - Compute the mean HR across participants per condition.
#   - Plot results as a bar chart (one per block).
# ============================================================

colors     = ["lightblue", "orange", "navy", "red"]  # same order as conditions
blocks = [1, 2, 3, 4, 5]

for b in blocks:
    measure = f"mean_b{b}"      # e.g., "mean_b1"
    means = []                  # collect means across conditions

    # Calculate condition-wise participant means
    for i in range(len(conditions)):
        cond_name = conditions[i]
        cond_df = summary[cond_name]          # DataFrame for this condition
        mean_val = cond_df[measure].mean(skipna=True)
        means.append(mean_val)

    # Plot histogram for this block
    plt.figure()
    plt.bar(conditions, means, color=colors)
    plt.title(f"HR mean — block {b}")
    plt.ylabel("HR")
    plt.xlabel("Condition")
    plt.tight_layout()
    plt.show()

# ============================================================
# HISTOGRAM OVERALL DATA
# ============================================================
# Compute the grand mean HR across all blocks (1–5) for each condition,
# then plot as a bar chart.
# ============================================================

overall_means = []
for i in range(len(conditions)):
    cond_name = conditions[i]
    cond_df = summary[cond_name]
    mean_val = cond_df["mean_all"].mean(skipna=True)
    overall_means.append(mean_val)

plt.figure()
plt.bar(conditions, overall_means, color=colors)
plt.title("HR mean — overall (blocks 1–5)")
plt.ylabel("HR")
plt.xlabel("Condition")
plt.tight_layout()
plt.show()
