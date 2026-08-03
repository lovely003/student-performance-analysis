# Student Performance — Data Analysis (Task 1)

Exploratory data analysis on a Students Performance dataset (math/reading/writing scores,
plus demographic and behavioral features like test prep, parental education, study hours,
and attendance) using Python, Pandas, NumPy, Matplotlib, and Seaborn.

This was done as **Task 1: Data Analysis Using Python** for Novexa Technologies.

## What's in this repo

```
.
├── data/
│   ├── StudentsPerformance.csv        # raw dataset (1012 rows, with some missing values + duplicates)
│   ├── StudentsPerformance_clean.csv  # cleaned dataset (1000 rows, no missing values)
│   └── generate_dataset.py            # script used to generate the dataset
├── notebook/
│   └── Student_Performance_Analysis.ipynb   # main analysis notebook
├── visualizations/                    # exported PNG charts
├── analysis.py                        # standalone script version of the analysis
├── Data_Analysis_Report.md            # write-up of methodology + findings
├── requirements.txt
└── README.md
```

## Dataset

500+ records with the following columns:

| Column | Description |
|---|---|
| `student_id` | Unique student identifier |
| `gender` | male / female |
| `race/ethnicity` | Group A–E (anonymized categories) |
| `parental_level_of_education` | Highest education level of parent |
| `lunch` | standard / free-reduced |
| `test_preparation_course` | none / completed |
| `study_hours_per_week` | Self-reported weekly study hours |
| `attendance_rate` | % class attendance |
| `math_score`, `reading_score`, `writing_score` | Exam scores (0–100) |

> Note: this dataset is synthetically generated (see `data/generate_dataset.py`) to mirror the
> structure and patterns of the well-known "Students Performance in Exams" dataset, so the
> project is fully reproducible without needing an external download.

## How to run it

```bash
git clone https://github.com/<your-username>/student-performance-analysis.git
cd student-performance-analysis
pip install -r requirements.txt

# regenerate the dataset (optional, one is already included in /data)
python data/generate_dataset.py

# run the full analysis and regenerate charts
python analysis.py

# or open the notebook
jupyter notebook notebook/Student_Performance_Analysis.ipynb
```

## Approach

1. **Load & inspect** — `read_csv`, `.head()`, `.tail()`, `.info()`, `.describe()`
2. **Check data quality** — missing values (`isnull().sum()`) and duplicates (`duplicated().sum()`)
3. **Clean** — dropped 12 duplicate rows, filled numeric missing values with the median and
   categorical missing values with the mode, engineered an `average_score` column
4. **Analyze & visualize**
   - Score distributions (histograms + KDE)
   - Gender vs average score (boxplot)
   - Test preparation course vs average score (boxplot)
   - Parental education level vs average score (barplot)
   - Correlation heatmap across numeric features
   - Study hours vs average score (scatter)
   - Lunch type vs average score (violin plot)

## Key Findings

- Students who **completed the test preparation course** scored ~9 points higher on average
  than those who didn't — the strongest single relationship in the dataset.
- **Parental education level** shows a fairly steady positive relationship with average score.
- **Lunch type** (standard vs free/reduced) shows a meaningful score gap, likely acting as a
  proxy for socio-economic background.
- **Gender** showed almost no difference in average scores.
- **Study hours** and **attendance** had only weak positive correlation with scores — more
  logged hours didn't reliably translate into higher scores.
- Math, reading, and writing scores are strongly correlated with each other — students tend to
  be consistently strong or weak across subjects rather than excelling in just one.

Full write-up with numbers: see [`Data_Analysis_Report.md`](./Data_Analysis_Report.md).

## Tools used

Python · Pandas · NumPy · Matplotlib · Seaborn · Jupyter Notebook

## Author

Submitted as part of the Novexa Technologies Data Analysis internship task.
