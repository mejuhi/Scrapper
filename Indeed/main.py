import requests 
import pandas as pd
from bs4 import BeautifulSoup 
import argparse
import logging
import time
import logging.config

# required arg
DEFAULT_URL = 'https://www.indeed.co.in/cmp/Capgemini/reviews'
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
    conUrl = args.url + "?start="	
    c = -20
    for i in range(0,(int(args.pagelimit))):
        c = c + 20 
        otherUrl =  conUrl + str(c)
        time.sleep(10)
        #open with GET method 
        resp=requests.get(otherUrl) 
          
        #http_respone 200 means OK status 
        if resp.status_code==200: 
            print("Successfully opened following web page: ")
            print(otherUrl)
            #print("The news are as follow :-\n")          
            # we need a parser,Python built-in HTML parser is enough . 
            soup=BeautifulSoup(resp.text,'html.parser')     
            # l is the list which contains all the text i.e news  
            l=soup.find("div",{"class":"cmp-ReviewsList"}) 
            #print(l)      
            countReviews = str(l).count('class="cmp-Review"')
            print('Total no of reviews in url "'+ otherUrl  +'" is '  + str(countReviews))        
            df = pd.DataFrame(columns=['ReviewText','ReviewTitle','ReviewRating','random'])        
            for i in l.findAll("div",{"class":"cmp-Review"}): 
                ##print(i.prettify())
                ReviewText=i.find("div",{"class":"cmp-Review-text"})
                ReviewTitle=i.find("div",{"class":"cmp-Review-title"})          
                ReviewRating=i.find("div",{"class":"cmp-ReviewRating-text"}) 
                random=i.find("span",{"class":"cmp-ReviewAuthor"}) 
                #print(random.text)
                #for k in i.findAll("a",{"class":"cmp-ReviewAuthor-link"}):
                  #print(k.text)
                  ##print(k.prettify())
                #print(ReviewTitle.text)
                #print(ReviewRating.text)			
                #print(ReviewText.text)
                df = df.append({'ReviewText':ReviewText.text,'ReviewTitle':ReviewTitle.text,'ReviewRating':ReviewRating.text,'random':random.text}, ignore_index=True)
            #print(df)
            df.to_csv("step1.csv", mode='a', header=False)
        else: 
            print("Error")
    print("End of code, Goodbye!")			

def processcsv():
    col_Names=['ReviewText','ReviewTitle','ReviewRating','OtherRandom']
    my_CSV_File= pd.read_csv("step1.csv",names=col_Names)
    print(my_CSV_File)
    my_CSV_File.to_csv("step2.csv", mode='w', header=True)	
    data = pd.read_csv("step2.csv")
    EmpData = data["OtherRandom"]
    Role_list=[]
    Date_list=[]
    loc_list =[]
    Status_list =[]
    for emp in EmpData:
        me = emp.split("(")
        Role_list.append(me[0])
        date = emp.split('-')[-1]
        Date_list.append(date)
        loc = emp.split('-')[-2]
        loc_list.append(loc)
        if "Current Employee" in emp:
            Status_list.append("Current Employee")
        elif "Former Employee" in emp:
            Status_list.append("Former Employee")
        else:
            Status_list.append("NA")
    data['Role'] = Role_list
    data['Date'] = Date_list
    data['location'] = loc_list
    data['EmployeeStatus'] = Status_list
    final_data = data.copy(deep=True)
    final_data.drop(["OtherRandom", "Unnamed: 0"], axis = 1, inplace = True) 
    final_data.to_csv(args.outputcsv, mode='w', header=True)



def main():
    logger.info(f'Scraping up to {args.pagelimit} review pages.')
    scrapereview()
    processcsv()
    end = time.time()
    logger.info("Successfully completed the task")

if __name__ == '__main__':
    main()