
# ECE143_Project

UCSD is a BIG school with 106 departments and 2452 total classes. Class selection can be difficult and overwhelming, especially for freshman and transfer students. This project aims to build a course recommendation system for UCSD students from CAPE (cape.ucsd.edu), which is a dataset that collects evaluation from students until Spring 2023.

This project takes inspiration from https://github.com/andportnoy/smartercapes.com

## Table of contents
- [Data_Collection](#Data_collection)
- [Data_processing](#Data_processing)
- [Requirements](#Requirements)

## Data_collection
**![Raw Data](https://lh7-us.googleusercontent.com/FO48FO54fkFQFCokSU4OCsrPLDhMAv8h_Aajleb9M6niLAi0GXjBDc3We3HT59Yai4prKd5iQFjBSJ2jKHAJnCGzpxys6zTVNnF2o3zxXTuzAAGgmblmLZ_m1w05FgRkTeJETUxKxP-z-9lgXfoAzxbHAQ=s2048)**
`scrape.py` is used to scrape data from CAPE. The figure above shows the sample raw data from `data.csv`.

## Data_processing

-   Scrape course evaluations from CAPE
    
-   Clean data
    

-   Remove null values
    
-   Remove outdated evaluations
    

-   Survey user for course preferences
    

-   Use to calculate recommendation
    
-   Reasoning explained later
    

-   Give recommendations and visualizations


## Course Data analysis



## Course Recommendation System 
We give 5 weights for the recommendation system.


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
