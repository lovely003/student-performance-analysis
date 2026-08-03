"""
generate_dataset.py
--------------------
Generates a synthetic "Students Performance" dataset that mirrors the
well-known Kaggle "Students Performance in Exams" dataset structure.

Why synthetic? So the project is fully self-contained and reproducible
without depending on an internet download. Distributions were chosen to
resemble realistic exam-score patterns (mild correlation between the three
scores, small effect of test-prep completion and parental education).
"""

import numpy as np
import pandas as pd

np.random.seed(42)

N = 1000

genders = np.random.choice(["male", "female"], size=N, p=[0.48, 0.52])

race_groups = np.random.choice(
    ["group A", "group B", "group C", "group D", "group E"],
    size=N, p=[0.10, 0.20, 0.32, 0.24, 0.14]
)

parent_education = np.random.choice(
    ["some high school", "high school", "some college",
     "associate's degree", "bachelor's degree", "master's degree"],
    size=N, p=[0.14, 0.20, 0.24, 0.22, 0.14, 0.06]
)

lunch = np.random.choice(["standard", "free/reduced"], size=N, p=[0.65, 0.35])

test_prep = np.random.choice(["none", "completed"], size=N, p=[0.64, 0.36])

study_hours_per_week = np.round(np.random.gamma(shape=3.0, scale=2.2, size=N), 1)
study_hours_per_week = np.clip(study_hours_per_week, 0, 25)

attendance_rate = np.clip(np.random.normal(88, 8, size=N), 45, 100).round(1)

# Base ability per student (latent factor) drives correlated scores
base_ability = np.random.normal(65, 12, size=N)

edu_bonus = pd.Series(parent_education).map({
    "some high school": -4, "high school": -2, "some college": 1,
    "associate's degree": 3, "bachelor's degree": 6, "master's degree": 9
}).values

prep_bonus = np.where(test_prep == "completed", 6, 0)
lunch_bonus = np.where(lunch == "standard", 3, -3)
study_bonus = study_hours_per_week * 0.6
attendance_bonus = (attendance_rate - 88) * 0.15

math_score = base_ability + edu_bonus + prep_bonus + lunch_bonus + study_bonus \
             + attendance_bonus + np.random.normal(0, 6, size=N)
reading_score = base_ability + edu_bonus * 0.8 + prep_bonus * 1.3 + lunch_bonus * 0.6 \
                + study_bonus * 0.8 + attendance_bonus + np.random.normal(0, 6, size=N)
writing_score = reading_score * 0.9 + np.random.normal(0, 5, size=N) + prep_bonus * 0.7

def clip_score(s):
    return np.clip(np.round(s), 0, 100).astype(int)

math_score = clip_score(math_score)
reading_score = clip_score(reading_score)
writing_score = clip_score(writing_score)

df = pd.DataFrame({
    "student_id": [f"STU{1000+i}" for i in range(N)],
    "gender": genders,
    "race/ethnicity": race_groups,
    "parental_level_of_education": parent_education,
    "lunch": lunch,
    "test_preparation_course": test_prep,
    "study_hours_per_week": study_hours_per_week,
    "attendance_rate": attendance_rate,
    "math_score": math_score,
    "reading_score": reading_score,
    "writing_score": writing_score,
})

# --- Introduce realistic messiness for the cleaning step ---
rng = np.random.default_rng(7)

# 1) Missing values scattered across a few columns
for col, frac in [("attendance_rate", 0.03), ("parental_level_of_education", 0.02),
                   ("writing_score", 0.015), ("study_hours_per_week", 0.02)]:
    idx = rng.choice(df.index, size=int(N * frac), replace=False)
    df.loc[idx, col] = np.nan

# 2) A handful of exact duplicate rows (common in raw exports)
dup_rows = df.sample(12, random_state=3)
df = pd.concat([df, dup_rows], ignore_index=True)

# 3) Shuffle row order so it doesn't look artificially generated
df = df.sample(frac=1, random_state=11).reset_index(drop=True)

df.to_csv("/home/claude/student-performance-analysis/data/StudentsPerformance.csv", index=False)
print("Dataset saved:", df.shape)
print(df.head())
