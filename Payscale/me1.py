import requests 
from bs4 import BeautifulSoup 
  
def news(): 
    # the target we want to open     
    url='https://www.payscale.com/research/US/Employer=Capgemini/Reviews'    
    #open with GET method 
    resp=requests.get(url) 
      
    #http_respone 200 means OK status 
    if resp.status_code==200: 
        print("Successfully opened the web page") 
        print("The news are as follow :-\n") 
      
        # we need a parser,Python built-in HTML parser is enough . 
        soup=BeautifulSoup(resp.text,'html.parser')     
        
 
        # l is the list which contains all the text i.e news  
        l=soup.find("div",{"class":"ugc-list"}) 
        #print(l.prettify())      
        countReviews = str(l).count('class="review"')
        print(countReviews)
        
        for i in l.findAll("div",{"class":"review"}): 
             #print(i.prettify())
             #print(i)
             print("--------------------")
             ReviewDate=i.find("div",{"class":"review__date"})
             Reviewer  =i.find("div",{"class":"review__reviewer"})          
             ReviewPro =i.find("div",{"class":"review__pros"}) 
             ReviewCon =i.find("div",{"class":"review__cons"})
             if ReviewDate is not None:
                 print(ReviewDate.text)
             if Reviewer is not None:
                 print(Reviewer.text)
             if ReviewPro is not None:
                 print(ReviewPro.text)
             if ReviewCon is not None:
                 print(ReviewCon.text)
        #now we want to print only the text part of the anchor. 
        #find all the elements of a, i.e anchor 
    else: 
        print("Error") 
          
news()