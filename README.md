


# ECE143_Project

UCSD is a BIG school with 106 departments and 2452 total classes. Class selection can be difficult and overwhelming, especially for freshman and transfer students. This project aims to build a course recommendation system for UCSD students from CAPE (cape.ucsd.edu), which is a dataset that collects evaluation from students until Spring 2023.

This project takes inspiration from https://github.com/andportnoy/smartercapes.com

## Structure
- [scrape.py](#Data_Collection)
- [clean_data.py](#Data_Processing)
- [recommendation.ipynb](#Course_Recommendation_System)
- [visualization.ipynb](#Visualization)
- [requirements.txt](#Requirements)
- data.csv
- data_clean.csv
- README.md


## Data_Collection
**![Raw Data](https://lh7-us.googleusercontent.com/FO48FO54fkFQFCokSU4OCsrPLDhMAv8h_Aajleb9M6niLAi0GXjBDc3We3HT59Yai4prKd5iQFjBSJ2jKHAJnCGzpxys6zTVNnF2o3zxXTuzAAGgmblmLZ_m1w05FgRkTeJETUxKxP-z-9lgXfoAzxbHAQ=s2048)**
The figure above shows the sample raw data from the capes website. `scrape.py` is used to scrape data from CAPE and export as `data.csv`.

## Data_Processing
`data_clean.py` imports `data.csv` and filters it. After removing null values / outdated evaluations and reselecting the columns, we export a cleaned data set as `data_clean.csv`. Below is the sample data.

| instr | term | enroll | evals | rmd_class | rmd_instr | time | Course_ID | Course_Name | expected_grade | expected_gpa | actual_grade | actual_gpa |
| ---------|--------- |--------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- | --------- | 
|Butler, Elizabeth Annette | WI23 | 65 | 46 | 93.5 | 93.3 | 4.15 | AAS 11 | Intro Black Diasporic Studies (A) | A- | 3.84 | A- | 3.71


## Course_Recommendation_System 
`Recommendation.ipynb` imports `data_clean.py`. It takes user input and creates a recommendation score. It also presents the user with useful graphs what explain its decision making.

$Score = [w_1,w_2,w_3,w_4,w_5]*[ActualGPA,InverseTimeSpent,ActualGPA - ExpectedGPA,RMDClass,RMDInstr]^T$

Bar charts of these factors are plotted respectively.

## Visualization
`visualization.ipynb` imports `data_clean.py`. It takes the user input and visualizes it in various graphs for the presentation. Visualization is split between `visualization.ipynb` and  `Recommendation.ipynb`

- Comparison of average gpa / time spent outside of class by quarter
- Expected and actual gpa in different quarters
- Average gpa received / time spent for upper division ECE courses by EE major depth
- Correlation: 
-- Time Spent vs Course Recommendation %
-- Time Spent vs Instructor Recommendation %
-- Actual GPA vs Course Recommendation %
-- Actual GPA vs Instructor Recommendation %

## Requirements

The `requirements.txt` file should list all Python libraries that your notebooks depend on.
```
matplotlib==3.5.3
scipy==1.7.3
numpy==1.22.3
pandas==1.4.4
statsmodels==0.14.0
natsort==7.1.1
selenium==3.141.0
```
