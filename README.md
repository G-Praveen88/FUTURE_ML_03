# FUTURE_ML_03 — Resume Screening System

Part of the **Future Interns Machine Learning Internship** (Task 3).

## Objective
Build a system that automatically screens and ranks job candidates for a
**Data Analyst** role based on their resume data — matching required
skills, experience, certifications, and prior company exposure — to help
recruiters shortlist top candidates faster.

## Approach
1. **Synthetic resume dataset** generated for 120 candidates (name,
   experience, degree, skills, certifications, previous companies).
2. **Skill matching**: each candidate's skill list is compared against 8
   weighted required skills for the role (Python, SQL, Excel, Power BI,
   Statistics, Machine Learning, Tableau, Communication) — core technical
   skills are weighted higher than soft/reporting skills.
3. **Composite scoring**: a final 0–100 score is computed as a weighted
   blend of skill match (55%), experience (25%), certifications (10%),
   and previous company exposure (10%).
4. **Tiering**: candidates are bucketed into Strong Fit (≥75), Moderate
   Fit (55–74), and Weak Fit (<55).
5. **Outputs**: a ranked shortlist CSV, a top-15 ranking bar chart, a
   skill-gap heatmap for the top 20 candidates, and a recruiter-facing
   text summary.

## Results (this run)
- **120** candidates screened for the Data Analyst role
- **37** Strong Fit / **40** Moderate Fit / **43** Weak Fit
- Top candidate: **Karan Patel** — score 95.0, 100% skill match, 8.7 yrs experience
- Most common skill gaps across the pool: Tableau, Power BI, Machine Learning, Python, Excel

## Files
| File | Description |
|---|---|
| `resume_screening.py` | Main script: scoring, ranking, charts, summary |
| `generate_data.py` | Generates the synthetic candidate dataset |
| `data/resumes_raw.csv` | Raw candidate resume data (120 records) |
| `candidate_ranking.csv` | Full ranked shortlist with scores and tiers |
| `candidate_ranking.png` | Bar chart — top 15 candidates by score |
| `skill_gap_heatmap.png` | Heatmap — skill coverage for top 20 candidates |
| `recruiter_summary.txt` | Plain-text recruiter summary and recommendation |

## How to Run
```bash
pip install pandas numpy matplotlib seaborn
python generate_data.py       # creates data/resumes_raw.csv
python resume_screening.py    # runs screening, saves all outputs
```

## Tech Stack
Python, pandas, NumPy, matplotlib, seaborn

---
*Future Interns — Machine Learning Track*
