import streamlit as st
import sqlite3
import pandas as pd
import math

st.set_page_config(layout="wide")

# ---------- LOAD DATA ----------
conn = sqlite3.connect("jobs.db", check_same_thread=False)
df = pd.read_sql("SELECT * FROM jobs", conn)

# ---------- HARD SAFETY ----------
REQUIRED_COLS = ["job_type", "skills", "start_date", "source"]

for col in REQUIRED_COLS:
    if col not in df.columns:
        df[col] = ""

df = df.fillna("")

st.title("🚀 Job Intelligence Platform")

# ---------- METRICS ----------
c1, c2, c3 = st.columns(3)
c1.metric("Total Jobs", len(df))
c2.metric("Companies", df["company"].nunique())
c3.metric("Sources", df["source"].nunique())

# ---------- SIDEBAR ----------
st.sidebar.header("🔍 Search & Filters")

search = st.sidebar.text_input(
    "What job are you looking for?",
    placeholder="frontend developer, HR intern, marketing"
)

job_type_selected = st.sidebar.multiselect(
    "Job Type",
    ["Internship", "Full Time", "Part Time"]
)

all_skills = sorted(set(",".join(df["skills"]).split(",")))
all_skills = [s.strip() for s in all_skills if s.strip()]

skills_selected = st.sidebar.multiselect("Skills", all_skills)

source_selected = st.sidebar.multiselect(
    "Source",
    sorted(df["source"].unique())
)

# ---------- FILTER LOGIC ----------
filtered = df.copy()

if search:
    s = search.lower()
    filtered = filtered[
        filtered["title"].str.lower().str.contains(s)
        | filtered["company"].str.lower().str.contains(s)
        | filtered["skills"].str.lower().str.contains(s)
    ]

if job_type_selected:
    filtered = filtered[
        filtered["job_type"].str.strip().isin(job_type_selected)
    ]

if skills_selected:
    pattern = "|".join(skills_selected)
    filtered = filtered[
        filtered["skills"].str.contains(pattern, case=False)
    ]

if source_selected:
    filtered = filtered[
        filtered["source"].isin(source_selected)
    ]

# ---------- PAGINATION ----------
PAGE_SIZE = 20
total_rows = len(filtered)

if total_rows == 0:
    st.warning("No jobs found. Try changing filters.")
else:
    total_pages = math.ceil(total_rows / PAGE_SIZE)

    page = st.number_input(
        "Page",
        min_value=1,
        max_value=total_pages,
        step=1
    )

    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    paginated_df = filtered.iloc[start:end].copy()

    # Make clickable Apply column
    paginated_df["Apply"] = paginated_df["link"].apply(
        lambda x: f'<a href="{x}" target="_blank">Apply</a>'
    )

    display_df = paginated_df[
        ["title", "company", "job_type", "source", "Apply"]
    ]

    st.subheader(f"Showing {total_rows} total jobs")

    st.write(
        display_df.to_html(escape=False, index=False),
        unsafe_allow_html=True
    )

# ---------- DOWNLOAD ----------
st.download_button(
    "⬇ Download Filtered Results",
    filtered.to_csv(index=False),
    "filtered_jobs.csv"
)
