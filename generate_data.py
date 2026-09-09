"""
Generates synthetic resume/candidate data for the Resume Screening System.
Creates data/resumes_raw.csv with candidate details, skills, and experience
for a Data Analyst job opening.
"""

import pandas as pd
import numpy as np
import random
import os

np.random.seed(42)
random.seed(42)

os.makedirs("data", exist_ok=True)

# Job requirement for Data Analyst role
REQUIRED_SKILLS = ["Python", "SQL", "Excel", "Power BI", "Statistics",
                    "Machine Learning", "Tableau", "Communication"]

ALL_SKILLS = REQUIRED_SKILLS + ["Java", "C++", "AWS", "Docker", "R",
                                 "Data Visualization", "Deep Learning",
                                 "Project Management", "Leadership"]

FIRST_NAMES = ["Aarav", "Priya", "Rohan", "Ananya", "Vikram", "Sneha", "Karan",
               "Divya", "Arjun", "Meera", "Nikhil", "Pooja", "Rahul", "Kavya",
               "Sanjay", "Ritu", "Amit", "Neha", "Vivek", "Isha", "Manish",
               "Shreya", "Aditya", "Tanya", "Rajesh", "Simran", "Varun", "Anjali",
               "Deepak", "Swati", "Suresh", "Priyanka", "Gaurav", "Nisha",
               "Ashok", "Kritika", "Manoj", "Ritika", "Sunil", "Payal"]

LAST_NAMES = ["Sharma", "Verma", "Patel", "Gupta", "Kumar", "Singh", "Rao",
              "Reddy", "Nair", "Iyer", "Menon", "Das", "Joshi", "Malhotra",
              "Chopra", "Kapoor", "Mehta", "Agarwal", "Bhatt", "Desai"]

DEGREES = ["B.Tech Computer Science", "B.Tech IT", "MCA", "M.Sc Statistics",
           "B.Sc Mathematics", "MBA Analytics", "B.Com", "M.Tech Data Science",
           "B.E Electronics", "M.Sc Computer Science"]

def generate_candidate(candidate_id):
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
    experience_years = round(np.random.uniform(0, 10), 1)

    # Candidates with more experience tend to have more skills (realistic correlation)
    base_skill_count = min(len(ALL_SKILLS), int(3 + experience_years * 1.1 + np.random.randint(-2, 3)))
    base_skill_count = max(2, base_skill_count)

    # Bias skill selection toward required skills so scoring is meaningful
    n_required = min(len(REQUIRED_SKILLS), np.random.randint(0, len(REQUIRED_SKILLS) + 1))
    candidate_required = random.sample(REQUIRED_SKILLS, n_required)
    remaining_slots = max(0, base_skill_count - n_required)
    other_pool = [s for s in ALL_SKILLS if s not in candidate_required]
    candidate_other = random.sample(other_pool, min(remaining_slots, len(other_pool)))

    skills = candidate_required + candidate_other
    random.shuffle(skills)

    degree = random.choice(DEGREES)
    certifications = np.random.randint(0, 5)

    return {
        "candidate_id": f"C{candidate_id:04d}",
        "name": name,
        "email": f"{name.lower().replace(' ', '.')}{candidate_id}@email.com",
        "experience_years": experience_years,
        "degree": degree,
        "skills": ", ".join(skills),
        "certifications": certifications,
        "previous_companies": np.random.randint(0, 5),
    }

def main():
    n_candidates = 120
    candidates = [generate_candidate(i) for i in range(1, n_candidates + 1)]
    df = pd.DataFrame(candidates)
    df.to_csv("data/resumes_raw.csv", index=False)
    print(f"Generated {len(df)} candidate records -> data/resumes_raw.csv")
    print(f"\nSample record:\n{df.iloc[0]}")

if __name__ == "__main__":
    main()
