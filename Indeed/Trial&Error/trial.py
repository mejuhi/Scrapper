import requests 
from bs4 import BeautifulSoup 
  
def news(): 
    # the target we want to open     
    url='https://www.indeed.co.in/cmp/Capgemini/reviews'
      
    #open with GET method 
    resp=requests.get(url) 
      
    #http_respone 200 means OK status 
    if resp.status_code==200: 
        print("Successfully opened the web page") 
        print("The news are as follow :-\n") 
      
        # we need a parser,Python built-in HTML parser is enough . 
        soup=BeautifulSoup(resp.text,'html.parser')     
        
        #print(soup)
        
        # l is the list which contains all the text i.e news  
        l=soup.find("div",{"class":"cmp-ReviewsList"}) 
      
        #print(l)
        o=l.find("div",{"class":"cmp-Review"})
        u=o.find("div",{"class":"cmp-Review-title"})
        
      
        print(u)
        print("bye----------------------------------------------")
        #now we want to print only the text part of the anchor. 
        #find all the elements of a, i.e anchor 
        for i in l.findAll("cmp-Review"): 
            print(i.text)
            print("+++--------------------------------------------")			
    else: 
        print("Error") 
          
news()