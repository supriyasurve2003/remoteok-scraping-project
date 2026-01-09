# Data Scraping file.

import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

driver = None

try:
    options = Options()
    options.add_argument("--headless")   # remove to SEE browser scrolling
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    URL = "https://remoteok.com/remote-jobs"
    driver.get(URL)

    time.sleep(2)  # initial load delay (respect crawl-delay)

    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # respect crawl-delay

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

   
    with open("raw_remoteok.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    jobs_data = []

    for job in soup.find_all("tr", class_="job"):

        #Job Title & URL 
        title_tag = job.find("h2")
        link_tag = job.find("a", class_="preventLink")

        job_title = title_tag.text.strip() if title_tag else None
        job_url = (
            "https://remoteok.com" + link_tag.get("href")
            if link_tag and link_tag.get("href")
            else None
        )

        #Company 
        company_tag = job.find("h3")
        company = company_tag.text.strip() if company_tag else None

        # Skills / Tags 
        skills = []
        tags_td = job.find("td", class_="tags")

        if tags_td:
            for tag_div in tags_td.find_all("div", class_="tag"):
                h3 = tag_div.find("h3")
                if h3:
                    skills.append(h3.text.strip())

        #Location
        location = None

        location_div = job.find("div", class_="location")
        if location_div:
            text = location_div.text.strip()
            if "upgrade" not in text.lower() and "premium" not in text.lower():
                location = text

        if not location:
            expand_row = job.find_next_sibling("tr", class_="expand")
            if expand_row:
                desc = expand_row.find("div", class_="description")
                if desc:
                    loc_header = desc.find("h1", id="location")
                    if loc_header:
                        loc_p = loc_header.find_next_sibling("p")
                        if loc_p:
                            location = loc_p.text.strip()

        if not location:
            location = "Remote"

        #Job Type
        job_type_tag = job.find("span", class_="contract")
        job_type = job_type_tag.text.strip() if job_type_tag else "Not specified"

        #Date Posted
        date_tag = job.find("time")
        date_posted = date_tag.get("datetime") if date_tag else None

        jobs_data.append({
            "Job Title": job_title,
            "Company": company,
            "Skills": ", ".join(skills),
            "Location": location,
            "Job Type": job_type,
            "Date Posted": date_posted,
            "Job URL": job_url
        })

   #Saving csv
    OUTPUT_FILE = "remoteok_raw.csv"

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "Job Title",
                "Company",
                "Skills",
                "Location",
                "Job Type",
                "Date Posted",
                "Job URL"
            ]
        )
        writer.writeheader()
        writer.writerows(jobs_data)

    print(f" Successfully scraped {len(jobs_data)} jobs")
    print(f" CSV saved as: {OUTPUT_FILE}")
    print("Raw HTML saved as: raw_remoteok.html")

except Exception as e:
    print("Scraper failed due to an unexpected error.")
    print(f"Error details: {e}")

finally:
    if driver:
        driver.quit()
        print("Browser closed safely.")
