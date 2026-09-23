"""
Resume Screening System
------------------------
Ranks candidates for a Data Analyst role using a weighted scoring model
based on required-skill match, years of experience, certifications, and
past company exposure. Produces a ranked shortlist, a skill-gap heatmap,
and a recruiter-facing summary.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import webbrowser
import os

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 100

# ---------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------
df = pd.read_csv("data/resumes_raw.csv")
print(f"Loaded {len(df)} candidate resumes.")

REQUIRED_SKILLS = ["Python", "SQL", "Excel", "Power BI", "Statistics",
                    "Machine Learning", "Tableau", "Communication"]

# Weight: core technical skills matter more than soft/reporting skills
SKILL_WEIGHTS = {
    "Python": 1.5,
    "SQL": 1.5,
    "Machine Learning": 1.3,
    "Statistics": 1.2,
    "Power BI": 1.0,
    "Tableau": 1.0,
    "Excel": 0.8,
    "Communication": 0.7,
}

# ---------------------------------------------------------------
# 2. Feature engineering
# ---------------------------------------------------------------
def parse_skills(skill_str):
    return set(s.strip() for s in skill_str.split(","))

df["skill_set"] = df["skills"].apply(parse_skills)

def skill_match_score(skill_set):
    matched = [s for s in REQUIRED_SKILLS if s in skill_set]
    weighted = sum(SKILL_WEIGHTS[s] for s in matched)
    max_weighted = sum(SKILL_WEIGHTS.values())
    return weighted / max_weighted, matched

scores_and_matches = df["skill_set"].apply(skill_match_score)
df["skill_match_pct"] = scores_and_matches.apply(lambda x: round(x[0] * 100, 1))
df["matched_skills"] = scores_and_matches.apply(lambda x: ", ".join(x[1]))
df["missing_skills"] = df["skill_set"].apply(
    lambda s: ", ".join([r for r in REQUIRED_SKILLS if r not in s])
)

# Normalize experience and certifications to 0-100 scale
df["experience_score"] = np.clip(df["experience_years"] / 8 * 100, 0, 100)
df["certification_score"] = np.clip(df["certifications"] / 4 * 100, 0, 100)
df["company_exposure_score"] = np.clip(df["previous_companies"] / 4 * 100, 0, 100)

# ---------------------------------------------------------------
# 3. Composite ranking score
# ---------------------------------------------------------------
WEIGHTS = {
    "skill_match_pct": 0.55,
    "experience_score": 0.25,
    "certification_score": 0.10,
    "company_exposure_score": 0.10,
}

df["final_score"] = sum(df[col] * w for col, w in WEIGHTS.items())
df["final_score"] = df["final_score"].round(1)

df_ranked = df.sort_values("final_score", ascending=False).reset_index(drop=True)
df_ranked["rank"] = df_ranked.index + 1

# Shortlist tier
def tier(score):
    if score >= 75:
        return "Strong Fit"
    elif score >= 55:
        return "Moderate Fit"
    else:
        return "Weak Fit"

df_ranked["fit_tier"] = df_ranked["final_score"].apply(tier)

# ---------------------------------------------------------------
# 4. Save ranked candidate list
# ---------------------------------------------------------------
output_cols = ["rank", "candidate_id", "name", "experience_years", "degree",
               "skill_match_pct", "matched_skills", "missing_skills",
               "certifications", "previous_companies", "final_score", "fit_tier"]

df_ranked[output_cols].to_csv("candidate_ranking.csv", index=False)
print("Saved ranked shortlist -> candidate_ranking.csv")

top10 = df_ranked.head(10)
print(f"\nTop 10 candidates:\n{top10[['rank', 'name', 'final_score', 'fit_tier']].to_string(index=False)}")

# ---------------------------------------------------------------
# 5. Visualization 1: Top-15 candidate ranking bar chart
# ---------------------------------------------------------------
top15 = df_ranked.head(15)
fig, ax = plt.subplots(figsize=(11, 7))
colors = ["#2ca02c" if t == "Strong Fit" else "#ff7f0e" if t == "Moderate Fit" else "#d62728"
          for t in top15["fit_tier"]]
bars = ax.barh(top15["name"][::-1], top15["final_score"][::-1], color=colors[::-1])
ax.set_xlabel("Final Score (0-100)")
ax.set_title("Top 15 Candidates - Resume Screening Ranking", fontsize=13, fontweight="bold")
ax.set_xlim(0, 100)
for bar, score in zip(bars, top15["final_score"][::-1]):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
            f"{score:.1f}", va="center", fontsize=9)
plt.tight_layout()
plt.savefig("candidate_ranking.png", dpi=100, bbox_inches="tight")
plt.close()
print("Saved chart -> candidate_ranking.png")
webbrowser.open_new_tab(
    "file://" + os.path.abspath("candidate_ranking.png")
)

# ---------------------------------------------------------------
# 6. Visualization 2: Skill gap heatmap (top 20 candidates)
# ---------------------------------------------------------------
top20 = df_ranked.head(20)
heatmap_data = pd.DataFrame(
    [[1 if skill in cand_skills else 0 for skill in REQUIRED_SKILLS]
     for cand_skills in top20["matched_skills"].apply(lambda s: set(s.split(", ")) if s else set())],
    index=top20["name"],
    columns=REQUIRED_SKILLS,
)

fig, ax = plt.subplots(figsize=(9, 9))
sns.heatmap(heatmap_data, cmap="YlGnBu", cbar=False, linewidths=0.5,
            linecolor="white", ax=ax, annot=heatmap_data.values, fmt="d")
ax.set_title("Skill Coverage Heatmap - Top 20 Candidates\n(1 = has skill, 0 = missing)",
              fontsize=12, fontweight="bold")
ax.set_xlabel("Required Skills")
ax.set_ylabel("Candidate")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("skill_gap_heatmap.png", dpi=100, bbox_inches="tight")
plt.close()
print("Saved chart -> skill_gap_heatmap.png")
webbrowser.open_new_tab(
    "file://" + os.path.abspath("skill_gap_heatmap.png")
)

# ---------------------------------------------------------------
# 7. Recruiter summary
# ---------------------------------------------------------------
strong_count = (df_ranked["fit_tier"] == "Strong Fit").sum()
moderate_count = (df_ranked["fit_tier"] == "Moderate Fit").sum()
weak_count = (df_ranked["fit_tier"] == "Weak Fit").sum()

most_common_missing = pd.Series(
    ", ".join(df_ranked["missing_skills"].dropna()).split(", ")
).value_counts()
most_common_missing = most_common_missing[most_common_missing.index != ""]

summary_lines = [
    "RESUME SCREENING SYSTEM - RECRUITER SUMMARY",
    "=" * 50,
    f"Role: Data Analyst",
    f"Total candidates screened: {len(df_ranked)}",
    "",
    "FIT DISTRIBUTION",
    "-" * 50,
    f"Strong Fit (score >= 75):   {strong_count} candidates",
    f"Moderate Fit (score 55-74): {moderate_count} candidates",
    f"Weak Fit (score < 55):      {weak_count} candidates",
    "",
    "TOP 10 RANKED CANDIDATES",
    "-" * 50,
]

for _, row in df_ranked.head(10).iterrows():
    summary_lines.append(
        f"{row['rank']:>2}. {row['name']:<20} | Score: {row['final_score']:>5.1f} | "
        f"{row['fit_tier']:<13} | Exp: {row['experience_years']} yrs | "
        f"Matched: {row['skill_match_pct']}%"
    )

summary_lines += [
    "",
    "MOST COMMON SKILL GAPS (across all candidates)",
    "-" * 50,
]
for skill, count in most_common_missing.head(5).items():
    summary_lines.append(f"  {skill}: missing in {count} candidates")

summary_lines += [
    "",
    "SCREENING SUMMARY",
    "-" * 50,
    f"{strong_count} candidates are classified as 'Strong Fit' based on the scoring criteria.",
    f"{moderate_count} candidates are classified as 'Moderate Fit'.",
    "Final interview and hiring decisions should be made by the recruiter.",
]

with open("recruiter_summary.txt", "w") as f:
    f.write("\n".join(summary_lines))

print("\nSaved -> recruiter_summary.txt")
print("\n" + "\n".join(summary_lines))
