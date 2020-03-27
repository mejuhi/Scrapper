# Installation
First, make sure that you're using Python 3.

1. Clone or download this repository.
2. Run `pip install -r requirements.txt` inside this repo. Consider doing this inside of a Python virtual environment.

# Working
Scrapper was last tested on 27th march 2020, Any changes to the site will hamper its working

# Disclaimer
This scraper is provided as a public service because Indeed doesn't have an API for reviews. Indeed TOS prohibit scraping and I make no representation that your account won't be banned if you use this program. Furthermore, should I be contacted by Indeed with a request to remove this repo, I will do so immediately.

# Usage
```
usage: main.py [-h] [-url URL] [-outputcsv FILE.CSV] [--pagelimit NUMBER]

optional arguments:
  -h, --help                                  show this help message and exit
  --url URL                                   URL of the company's Indeed landing page. (Eg/Defaul:'https://www.indeed.co.in/cmp/Capgemini/reviews' )
  --pagelimit NUMBER                          Limit on number of pages to be scrapped.  (Eg: 2)
  --outputcsv FILENAME.csv                    Name of the csv file for final output     (Eg: whatJuhi.csv)  
  --single    NUMBER                          No use yet 
```

### Example 1
Suppose you want to get the reviews from first 3 page of Capgemini from indeed

`python main.py --pagelimit 3 --single 0 --url https://www.indeed.co.in/cmp/Capgemini/reviews --outputcsv whatJuhi.csv`

