import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 110

DATA_PATH = "data/StudentsPerformance.csv"
OUT = "visualizations/"

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("SHAPE:", df.shape)
print("=" * 60)
print("\nHEAD:\n", df.head())
print("\nTAIL:\n", df.tail())
print("\nINFO:")
df.info()
print("\nDESCRIBE:\n", df.describe())

print("\nMISSING VALUES:\n", df.isnull().sum())
print("\nDUPLICATE ROWS:", df.duplicated().sum())

# --- Cleaning ---
df_clean = df.drop_duplicates().copy()

# numeric columns -> fill with median
for col in ["attendance_rate", "study_hours_per_week", "writing_score"]:
    df_clean[col] = df_clean[col].fillna(df_clean[col].median())

# categorical -> fill with mode
df_clean["parental_level_of_education"] = df_clean["parental_level_of_education"].fillna(
    df_clean["parental_level_of_education"].mode()[0]
)

df_clean["average_score"] = df_clean[["math_score", "reading_score", "writing_score"]].mean(axis=1).round(1)

print("\nAFTER CLEANING shape:", df_clean.shape)
print("Missing after cleaning:\n", df_clean.isnull().sum().sum())

df_clean.to_csv("data/StudentsPerformance_clean.csv", index=False)

# ---------------------------------------------------------------
# 1. Distribution of scores
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
for ax, col, color in zip(axes, ["math_score", "reading_score", "writing_score"],
                           ["#4C72B0", "#DD8452", "#55A868"]):
    sns.histplot(df_clean[col], kde=True, ax=ax, color=color, bins=20)
    ax.set_title(f"{col.replace('_', ' ').title()} Distribution")
plt.tight_layout()
plt.savefig(OUT + "01_score_distributions.png")
plt.close()

# 2. Gender vs average score
fig, ax = plt.subplots(figsize=(6, 4.5))
sns.boxplot(data=df_clean, x="gender", y="average_score", hue="gender",
            palette="Set2", ax=ax, legend=False)
ax.set_title("Average Score by Gender")
plt.tight_layout()
plt.savefig(OUT + "02_gender_vs_score.png")
plt.close()

# 3. Test preparation course effect
fig, ax = plt.subplots(figsize=(6, 4.5))
sns.boxplot(data=df_clean, x="test_preparation_course", y="average_score",
            hue="test_preparation_course", palette="Set3", ax=ax, legend=False)
ax.set_title("Average Score vs Test Preparation Course")
plt.tight_layout()
plt.savefig(OUT + "03_testprep_vs_score.png")
plt.close()

# 4. Parental education vs average score
fig, ax = plt.subplots(figsize=(8, 5))
order = ["some high school", "high school", "some college",
         "associate's degree", "bachelor's degree", "master's degree"]
sns.barplot(data=df_clean, x="parental_level_of_education", y="average_score",
            order=order, hue="parental_level_of_education", palette="viridis", ax=ax, legend=False)
ax.set_title("Average Score by Parental Education Level")
ax.tick_params(axis="x", rotation=30)
plt.tight_layout()
plt.savefig(OUT + "04_parentedu_vs_score.png")
plt.close()

# 5. Correlation heatmap
fig, ax = plt.subplots(figsize=(6, 5))
corr = df_clean[["math_score", "reading_score", "writing_score",
                  "study_hours_per_week", "attendance_rate", "average_score"]].corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
ax.set_title("Correlation Heatmap")
plt.tight_layout()
plt.savefig(OUT + "05_correlation_heatmap.png")
plt.close()

# 6. Study hours vs average score scatter
fig, ax = plt.subplots(figsize=(6.5, 4.5))
sns.scatterplot(data=df_clean, x="study_hours_per_week", y="average_score",
                 hue="test_preparation_course", palette="deep", alpha=0.6, ax=ax)
ax.set_title("Study Hours per Week vs Average Score")
plt.tight_layout()
plt.savefig(OUT + "06_studyhours_vs_score.png")
plt.close()

# 7. Lunch type vs average score
fig, ax = plt.subplots(figsize=(6, 4.5))
sns.violinplot(data=df_clean, x="lunch", y="average_score", hue="lunch",
               palette="pastel", ax=ax, legend=False)
ax.set_title("Average Score by Lunch Type")
plt.tight_layout()
plt.savefig(OUT + "07_lunch_vs_score.png")
plt.close()

print("\nAll charts saved to /visualizations")

# summary stats used in the report
print("\nGROUPBY gender mean scores:\n", df_clean.groupby("gender")[["math_score","reading_score","writing_score","average_score"]].mean().round(2))
print("\nGROUPBY test prep mean scores:\n", df_clean.groupby("test_preparation_course")["average_score"].mean().round(2))
print("\nGROUPBY parental edu mean scores:\n", df_clean.groupby("parental_level_of_education")["average_score"].mean().round(2).sort_values())
print("\nCorrelation study_hours vs average_score:", df_clean["study_hours_per_week"].corr(df_clean["average_score"]).round(3))
print("\nCorrelation attendance vs average_score:", df_clean["attendance_rate"].corr(df_clean["average_score"]).round(3))
