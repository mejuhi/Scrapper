import requests 
import pandas as pd
from bs4 import BeautifulSoup 
import argparse
import logging
import time
import logging.config

# required arg
DEFAULT_URL = 'https://www.payscale.com/research/US/Employer=Capgemini/Reviews'
DEFAULT_CSV = 'helloJuhi.csv'
parser = argparse.ArgumentParser()
parser.add_argument('--url', required=False, help='URL of the company\'s Indeed landing page.', default=DEFAULT_URL)
parser.add_argument('--pagelimit', required=True, help='limit')
parser.add_argument('--single', required=True, help='want to get of a specific page.')
parser.add_argument('--outputcsv', required=False, help='output csv file.',default=DEFAULT_CSV)
args = parser.parse_args()

# print all the arguments
# print(args.url)
# print(args.pagelimit)
# print(args.single)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(lineno)d\
    :%(filename)s(%(process)d) - %(message)s')
ch.setFormatter(formatter)

def scrapereview(): 
    # the target we want to open
    conUrl = args.url + "/Page-"	
    c = 0
    for i in range(0,(int(args.pagelimit))):
        c = c + 1
        print("i: " + str(i) + "c:" +str(c))
        otherUrl =  conUrl + str(c)
        time.sleep(10)
        #open with GET method 
        resp=requests.get(otherUrl) 
          
        #http_respone 200 means OK status 
        if resp.status_code==200: 
            print("Successfully opened following web page: ")
            print(otherUrl)
            soup=BeautifulSoup(resp.text,'html.parser')     
            l=soup.find("div",{"class":"ugc-list"}) 
            #print(l)      
            countReviews = str(l).count('class="review"')
            print('Total no of reviews in url "'+ otherUrl  +'" is '  + str(countReviews))        
            df = pd.DataFrame(columns=['ReviewDate','Reviewer','ReviewPro','ReviewCon','ReviewDes'])        
            for i in l.findAll("div",{"class":"review"}): 
                #print(i.prettify())
                #print(i)
                ReviewDate=i.find("div",{"class":"review__date"})
                Reviewer  =i.find("div",{"class":"review__reviewer"})          
                ReviewPro =i.find("div",{"class":"review__pros"}) 
                ReviewCon =i.find("div",{"class":"review__cons"})
                ReviewDes =i.find("div",{"class":"review__content review__summary"})				
                if ReviewDate is not None:
                    rd = ReviewDate.text
                else:
                    rd = "NA"
                if Reviewer is not None:
                    rr = Reviewer.text
                else:
                    rr = "NA"					
                if ReviewPro is not None:
                    rp = ReviewPro.text
                else:
                    rp = "Pros: NA"					
                if ReviewCon is not None:
                    rc = ReviewCon.text
                else:
                    rc = "Cons: NA"										
                if ReviewDes is not None:
                    rs = ReviewDes.text
                else:
                    rs = "NA"						
                df = df.append({'ReviewDate':rd,'Reviewer':rr,'ReviewPro':rp,'ReviewCon':rc, 'ReviewDes':rs}, ignore_index=True)
            print(df)
            df.to_csv("step1.csv", mode='a', header=False)
        else: 
            print("Error")
    print("End of code, Goodbye!")			

def processcsv():
    col_Names=['ReviewDate','Reviewer','ReviewPro','ReviewCon','ReviewDes']
    my_CSV_File= pd.read_csv("step1.csv",names=col_Names)
    print(my_CSV_File)
    my_CSV_File.to_csv("step2.csv", mode='w', header=True)	
    datadf = pd.read_csv("step2.csv")

    ReviewerData = datadf["Reviewer"]
    ProData = datadf["ReviewPro"]
    ConData = datadf["ReviewCon"]
    Pro_list=[]
    Con_list=[]
    Role_list=[]
    loc_list =[]

    for pro in ProData:
        onlyPro = pro.split(':')[-1]
        Pro_list.append(onlyPro)
    
    for con in ConData:
        onlyCon = con.split(':')[-1]
        Con_list.append(onlyCon)

    for data in ReviewerData:
        if " in " in data:
            me = data.replace(" in ", " | ")
            loc = me.split('|')[-1]
            loc = loc.replace(":", " ")
            loc_list.append(loc.strip())
            role = me.split('|')[0]
            role = role.replace(":", " ")
            Role_list.append(role.strip())
        else:
            loc_list.append("NA")
            data = data.replace(":", " ")
            Role_list.append(data.strip())

    datadf['Role'] = Role_list
    datadf['location'] = loc_list
    datadf['Pro'] = Pro_list
    datadf['Con'] = Con_list

    final_data = datadf.copy(deep=True)
    final_data.drop(["ReviewPro", "ReviewCon", "Reviewer", "Unnamed: 0"], axis = 1, inplace = True) 
    final_data.to_csv(args.outputcsv, mode='w', header=True)

def main():
    logger.info(f'Scraping up to {args.pagelimit} review pages.')
    scrapereview()
    processcsv()
    end = time.time()
    logger.info("Successfully completed the task")

if __name__ == '__main__':
    main()