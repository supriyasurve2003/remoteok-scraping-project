"""
RemoteOK Data Cleaning Script
VS Code Compatible
"""

import pandas as pd
import numpy as np

def clean_remoteok_data(input_file="final.csv", output_file="remoteok_jobs_cleaned.csv"):
    """
    Clean RemoteOK job data following Evoastra rules.
    """
    print("=== Starting Data Cleaning ===")
    
    # 1. Load data
    try:
        df = pd.read_csv(input_file)
        print(f"✓ Loaded: {df.shape[0]} rows")
    except FileNotFoundError:
        print(f"✗ Error: File '{input_file}' not found")
        print(f"  Place '{input_file}' in same folder as this script")
        return
    
    # 2. Handle missing values
    critical_cols = ['Job Title', 'Company', 'Skills']
    df_cleaned = df.dropna(subset=critical_cols).copy()
    df_cleaned[['Location', 'Job Type']] = df_cleaned[['Location', 'Job Type']].fillna('not_specified')
    
    # 3. Remove duplicates
    df_cleaned = df_cleaned.drop_duplicates(subset=['Job Title', 'Company', 'Job URL'])
    
    # 4. Clean text
    text_cols = ['Job Title', 'Company', 'Location', 'Job Type']
    for col in text_cols:
        df_cleaned[col] = df_cleaned[col].astype(str).str.lower().str.strip()
    
    # 5. Remove emojis
    df_cleaned['Location'] = df_cleaned['Location'].str.encode('ascii', 'ignore').str.decode('ascii').str.strip()
    
    # 6. Clean skills
    def clean_skills(skills):
        if isinstance(skills, str):
            skills = skills.lower().strip()
            skill_list = [skill.strip() for skill in skills.split(',')]
            skill_list = [s for s in skill_list if s]
            unique_skills = list(dict.fromkeys(skill_list))
            return ', '.join(unique_skills)
        return skills
    
    df_cleaned['Skills'] = df_cleaned['Skills'].apply(clean_skills)
    
    # 7. Fix dates
    df_cleaned['Date Posted'] = df_cleaned['Date Posted'].astype(str).str[:10]
    
    # 8. Save cleaned data
    df_cleaned.to_csv(output_file, index=False)
    
    # 9. Print summary
    print("✓ Cleaning Summary:")
    print(f"  Original: {df.shape[0]} rows")
    print(f"  Cleaned:  {df_cleaned.shape[0]} rows")
    print(f"  Removed:  {df.shape[0] - df_cleaned.shape[0]} rows")
    print(f"✓ Saved as: '{output_file}'")
    print("=== Cleaning Complete ===")
    
    return df_cleaned

if __name__ == "__main__":
    clean_remoteok_data()