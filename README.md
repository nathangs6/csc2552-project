# csc2552-project
Code and data for my CSC2552 project.

## Results Replication
To replicate results, please do the following:
1. Clone repo to your local system
2. Download article data to data/input/ using this link https://drive.google.com/file/d/1CnM6j8fNgN_hNAprMxO5kT4nkB_MZ35m/view?usp=sharing
3. Setup python virtual environment
    * Run `python -m venv env`
    * Run `source env/bin/activate`
    * Run `python -m pip install -r requirements.txt`
4. Setup R virtual environment
    * Go into `r/`
    * Run `R`
    * Run `renv::restore()`
    * Install `wordcloud` package by running `renv::install("wordcloud")`
5. Run `getUnions.py`
6. Run `cleanData.py`
7. Run `eliminatedDataCheck.r`
8. Run `prevalenceAnalysis.r`

Results will be in the `r/output/` folder.

## Content Analysis
Originally, I was going to do a rhetoric analyis between the left-leaning and right-leaning publishers. However, not enough data could be found to make this a substantial analysis. The code to generate the model used for such analysis is found in `r/contentAnalysis.r`

## Data Scrapers
To account for not enough data for the content analysis, I attempted to scrape some websites for data. I succeeded in some of the data scraping, but many of the websites either blocked data scrapers or had way too many articles in a given year for a reasonable download time. In the end, I didn't get enough articles to do a content analysis with. Some of the scrapers I wrote can be found in the `scrapers/` folder.
