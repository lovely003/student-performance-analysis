# Data Analysis Report — Student Performance Dataset

**Task:** Data Analysis Using Python (Task 1)
**Tools used:** Python, Pandas, NumPy, Matplotlib, Seaborn, Jupyter Notebook

---

## 1. Objective

Load, inspect, clean, and analyze a student performance dataset, then pull out meaningful
insights using statistical summaries and visualizations.

## 2. Dataset Overview

- **Rows:** 1,012 (before cleaning) → 1,000 (after removing duplicates)
- **Columns:** 11 — a mix of categorical (gender, race/ethnicity, parental education, lunch,
  test prep) and numeric (study hours, attendance rate, math/reading/writing scores) features.

## 3. Data Cleaning

| Issue | Found | Action |
|---|---|---|
| Duplicate rows | 12 | Dropped with `drop_duplicates()` |
| Missing `parental_level_of_education` | 21 | Filled with mode |
| Missing `study_hours_per_week` | 20 | Filled with median |
| Missing `attendance_rate` | 30 | Filled with median |
| Missing `writing_score` | 15 | Filled with median |

After cleaning: **0 missing values**, **1,000 rows**, and one engineered column,
`average_score` (mean of the three subject scores).

## 4. Summary Statistics

| Metric | Math | Reading | Writing | Average |
|---|---|---|---|---|
| Mean | ~73.0 | ~72.0 | ~66.1 | ~70.4 |
| Std Dev | ~14 | ~14.6 | ~14.6 | ~13 |
| Min | ~24 | 33 | 24 | — |
| Max | 100 | 100 | 100 | — |

Scores are roughly normally distributed with a mild left skew (a longer tail of
lower-scoring students than higher-scoring ones).

## 5. Key Insights

### 5.1 Test Preparation Course Matters Most
Students who completed the test prep course averaged **76.2**, vs **67.2** for those who
didn't — a ~9 point gap. This was the strongest, cleanest relationship found in the dataset.

### 5.2 Parental Education Has a Steady Gradient
Average score rises fairly consistently with parental education level, from ~66.2
(some high school) up to ~76.9 (master's degree) — roughly a 10-point spread end-to-end.

### 5.3 Lunch Type Shows a Meaningful Gap
Students on the standard lunch plan outscore those on free/reduced lunch. This mirrors a
well-documented pattern in the real-world version of this dataset and likely reflects
broader socio-economic circumstances rather than lunch itself.

### 5.4 Gender: Negligible Difference
Female and male students had nearly identical average scores (70.42 vs 70.32) — no
meaningful gap in this dataset.

### 5.5 Study Hours & Attendance: Weak Correlation
- Study hours vs average score correlation: **r ≈ 0.11**
- Attendance vs average score correlation: **r ≈ 0.08**

Both are positive but weak — logging more study hours didn't reliably predict a higher
score, suggesting that *how* students study (quality, consistency, focus) likely matters
more than raw hours logged, though that isn't directly measurable from this data.

### 5.6 Strong Cross-Subject Correlation
Math, reading, and writing scores correlate with each other at roughly **r ≈ 0.6–0.7**,
indicating that a student's overall academic strength tends to show up consistently
across subjects, rather than being isolated to one.

## 6. Visualizations

All charts are available in `/visualizations`:

1. `01_score_distributions.png` — histogram + KDE for each subject score
2. `02_gender_vs_score.png` — boxplot of average score by gender
3. `03_testprep_vs_score.png` — boxplot of average score by test prep completion
4. `04_parentedu_vs_score.png` — barplot of average score by parental education
5. `05_correlation_heatmap.png` — correlation matrix of numeric features
6. `06_studyhours_vs_score.png` — scatter of study hours vs average score
7. `07_lunch_vs_score.png` — violin plot of average score by lunch type

## 7. Conclusion

The most actionable finding is the strong association between test preparation course
completion and score improvement. Socio-economic proxies (lunch type, parental education)
also show meaningful relationships with performance, while gender shows essentially none.
Study hours and attendance, somewhat surprisingly, show only weak correlation with
outcomes in this dataset — worth digging into further with additional behavioral data
(e.g. study method, sleep, tutoring) in a follow-up analysis.

## 8. Limitations

- Dataset is synthetically generated (see `data/generate_dataset.py`) to mirror realistic
  patterns from the well-known "Students Performance in Exams" dataset structure, since the
  project needed to be fully self-contained and reproducible.
- Correlation does not imply causation — e.g., the lunch-type effect is very likely a proxy
  for broader socio-economic factors, not a direct causal link.
- Self-reported study hours may not reflect actual effective study time.
