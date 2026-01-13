# Remote Job Market Intelligence using Ethical Web Scraping

## Internship Mini Project  
*Organization:* Evoastra Ventures (OPC) Pvt Ltd  
*Project Type:* Data Science Internship Project  
*Difficulty Level:* Beginner-Friendly  
*Target Website:* https://remoteok.com  

---

## Project Overview
This project focuses on analyzing the remote job market by ethically collecting job listings from *Remote OK*.  
The objective is to extract meaningful insights about *job roles, skill demand, job types, and geographic distribution* using real-world job posting data while strictly adhering to legal and ethical web scraping standards.

The project simulates an industry-level data pipeline, covering data collection, cleaning, analysis, visualization, and documentation.

---

## Data Source & Ethical Compliance
- *Website:* Remote OK (https://remoteok.com)
- *Scraping Type:* Educational (Non-commercial)
- *Compliance Measures:*
  - Followed robots.txt
  - Implemented 1-second crawl delay
  - Avoided forbidden endpoints (?action=get_jobs)
  - No aggressive or parallel scraping
  - Raw scraped data not published publicly

---

## Tools & Technologies
- Python 3.8+
- requests
- BeautifulSoup
- pandas
- matplotlib
- seaborn
- Google Colab / VS Code

---

## Project Workflow
1. *Web Scraping*
   - Extracted job title, company, skills, location, job type, date posted, and job URL
   - Used public HTML pages only

2. *Data Cleaning*
   - Removed duplicate records
   - Handled missing values
   - Normalized text fields
   - Cleaned skill tags and location fields

3. *Data Analysis*
   - Skill frequency analysis
   - Job title distribution
   - Company-wise job posting analysis
   - Location-based distribution

4. *Data Visualization*
   - Top demanded skills
   - Most common job roles
   - Job type distribution
   - Skill frequency comparisons

5. *Documentation*
   - Clear folder structure
   - Clean, readable code
   - Professional reporting of insights and limitations

---

## Key Insights
- Technical roles dominate the remote job market
- Python, SQL, AWS, and JavaScript are among the most demanded skills
- Most job postings are fully remote
- Analysis is primarily descriptive due to non-numeric data

---

## Limitations
- Data is limited to Remote OK only
- Dataset contains mostly text-based fields
- No salary or numeric metrics available
- Advanced statistical or ML analysis is not applicable

---

## Team Contribution
- *Web Scraping:* Scraping Team  
- *Data Cleaning:* Data Cleaning Team  
- *Analysis & Visualization:* Analysis Team  
- *Documentation & Coordination:* Documentation Team

---

## Compliance Statement
This project strictly follows ethical web scraping practices and Evoastra internship guidelines.  
No proprietary or restricted data was accessed or redistributed.

---

## Data Limitations and Biases
The dataset was scraped from Remote OK and reflects only job postings available on thatplatform. 
As such, it does not represent the global remote job market. The data is subject to sampling,
time-based, website-specific, and data-quality biases.

---

*Evoastra Ventures (OPC) Pvt Ltd*  
Data Science Internship – Mini Project

---


## 📁 Project Structure

```text
remoteok-scraping-project/
│
├── README.md                  # Project overview & documentation
├── requirements.txt           # Python dependencies
├── .gitignore                 # Excludes raw data & unnecessary files
├── Team_B.ipynb               # Jupyter Notebook (scraping, cleaning, analysis & visuals)
│
├── src/                       # Source code
│   ├── scraper.py             # Ethical web scraping logic
│   ├── data_cleaner.py        # Data cleaning pipeline
│   └── analyzer.py            # Data analysis & visualization
│
├── data/
│   └── cleaned/
│       └── remoteok_jobs_cleaned.csv   # Final cleaned dataset
│
├── visualizations/
│   ├── top_skills.png
│   ├── job_type_distribution.png
│   ├── top_job_titles.png
│   └── skill_frequency_comparison.png
│
└── reports/
    ├── analysis_report.pdf    # Final project report
    └── methodology.md         # Technical methodology

