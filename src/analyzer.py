
# =========================
# Imports
# =========================
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from pathlib import Path
from matplotlib import cm

# =========================
# Global Config
# =========================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "outputs"
PLOTS_DIR = OUTPUT_DIR / "plots"

for d in [DATA_DIR, OUTPUT_DIR, PLOTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", context="notebook")

# =========================
# Logging
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("RemoteOK-Visualization")

# =========================
# Load Dataset
# =========================
def load_data():
    try:
        file_path = DATA_DIR / "remoteok_jobs_cleaned.csv"
        df = pd.read_csv(file_path)
        logger.info(f"Dataset loaded successfully | Shape: {df.shape}")
        return df
    except Exception as e:
        logger.error("Failed to load dataset", exc_info=True)
        raise e

# =========================
# Pre-checks
# =========================
def validate_data(df):
    required_cols = ["Job Title", "Skills", "Job Type", "Location", "Date Posted"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["date_posted"] = pd.to_datetime(df["Date Posted"], errors="coerce")
    df["days_since_posted"] = (pd.Timestamp.utcnow() - df["date_posted"]).dt.days

    logger.info("Data validation & minimal preprocessing completed")
    return df

# =====================================================
# IMPORTANT PLOT 1: Top 10 Skills Demand (Pulkit)
# =====================================================
def plot_top_skills(df):
    skills = (
        df["Skills"]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
        .value_counts()
        .head(10)
        .sort_values()
    )

    plt.figure(figsize=(10, 6))
    colors = cm.viridis_r(range(len(skills)))
    ax = skills.plot(kind="barh", color=colors, edgecolor="black")

    plt.title("Top 10 Skills in Demand", fontsize=16, weight="bold", loc="left")
    plt.xlabel("Number of Job Postings")
    plt.ylabel("Skill")

    for i, v in enumerate(skills.values):
        plt.text(v + 2, i, str(v), va="center", fontsize=10)

    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "01_top_skills.png", dpi=300)
    plt.close()
    logger.info("Pulkit | Top Skills plot generated")

# =====================================================
# IMPORTANT PLOT 2: Job Type Distribution (Rishita)
# =====================================================
def plot_job_type_distribution(df):
    job_types = df["Job Type"].fillna("Not Specified").value_counts()

    plt.figure(figsize=(8, 8))
    plt.pie(
        job_types,
        labels=job_types.index,
        autopct="%1.1f%%",
        startangle=90,
        colors=cm.Set3.colors
    )

    plt.title("Job Type Distribution in Remote Jobs", fontsize=16, weight="bold")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "02_job_type_distribution.png", dpi=300)
    plt.close()
    logger.info("Rishita | Job Type Distribution plot generated")

# =====================================================
# IMPORTANT PLOT 3: Top 10 Job Titles (Costas)
# =====================================================
def plot_top_job_titles(df):
    titles = df["Job Title"].value_counts().head(10).sort_values()
    colors = cm.plasma(range(len(titles)))

    plt.figure(figsize=(10, 6))
    ax = titles.plot(kind="barh", color=colors, edgecolor="black")

    plt.title("Top 10 Job Titles by Demand", fontsize=16, weight="bold", loc="left")
    plt.xlabel("Number of Job Postings")
    plt.ylabel("Job Title")

    for i, v in enumerate(titles.values):
        plt.text(v + 1, i, str(v), va="center")

    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "03_top_job_titles.png", dpi=300)
    plt.close()
    logger.info("Costas | Top Job Titles plot generated")

# =====================================================
# IMPORTANT PLOT 4: Skill Frequency Comparison (Pulkit)
# =====================================================
def plot_skill_frequency(df):
    skills = (
        df["Skills"]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
        .value_counts()
        .head(15)
        .sort_values()
    )

    plt.figure(figsize=(10, 6))
    ax = skills.plot(kind="barh", color="#59A14F", edgecolor="black")

    plt.title("Skill Frequency Comparison", fontsize=16, weight="bold", loc="left")
    plt.xlabel("Frequency")
    plt.ylabel("Skill")

    for i, v in enumerate(skills.values):
        plt.text(v + 2, i, str(v), va="center")

    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "04_skill_frequency.png", dpi=300)
    plt.close()
    logger.info("Pulkit | Skill Frequency plot generated")

# =====================================================
# OPTIONAL PLOT 5: Job Posting Freshness (Costas)
# =====================================================
def plot_job_freshness(df):
    cap = df["days_since_posted"].quantile(0.95)
    freshness = df["days_since_posted"].clip(upper=cap)

    plt.figure(figsize=(10, 6))
    ax = sns.histplot(freshness, bins=30, kde=True, color="#4C72B0")

    plt.title("Job Posting Freshness", fontsize=16, weight="bold", loc="left")
    plt.xlabel("Days Since Posted")
    plt.ylabel("Number of Job Postings")

    median = freshness.median()
    plt.axvline(median, color="red", linestyle="--", label=f"Median: {int(median)} days")
    plt.legend()

    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "05_job_freshness.png", dpi=300)
    plt.close()
    logger.info("Costas | Job Freshness plot generated")

# =====================================================
# OPTIONAL PLOT 6: Job Title Demand Concentration (Costas)
# =====================================================
def plot_demand_concentration(df):
    counts = df["Job Title"].value_counts()
    cumulative = counts.cumsum() / counts.sum()

    plt.figure(figsize=(10, 6))
    plt.plot(cumulative.values, linewidth=3, color="#4C72B0")
    plt.axhline(0.8, linestyle="--", color="#E15759", label="80% demand")

    plt.title("Job Title Demand Concentration", fontsize=16, weight="bold", loc="left")
    plt.xlabel("Job Title Rank")
    plt.ylabel("Cumulative Share")
    plt.legend()

    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "06_job_title_concentration.png", dpi=300)
    plt.close()
    logger.info("Costas | Demand Concentration plot generated")

# =========================
# Main Runner
# =========================
def main():
    logger.info("Visualization pipeline started")
    df = load_data()
    df = validate_data(df)

    plot_top_skills(df)
    plot_job_type_distribution(df)
    plot_top_job_titles(df)
    plot_skill_frequency(df)
    plot_job_freshness(df)
    plot_demand_concentration(df)

    logger.info("All visualizations generated successfully")

if __name__ == "__main__":
    main()