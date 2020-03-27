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
        
 
        # l is the list which contains all the text i.e news  
        l=soup.find("div",{"class":"cmp-ReviewsList"}) 
        #print(l)      
        countReviews = str(l).count('class="cmp-Review"')
        print(countReviews)

        for i in l.findAll("div",{"class":"cmp-Review"}): 
            #print(i.prettify())
            ReviewText=i.find("div",{"class":"cmp-Review-text"})
            ReviewTitle=i.find("div",{"class":"cmp-Review-title"})          
            ReviewRating=i.find("div",{"class":"cmp-ReviewRating-text"}) 
            random=i.find("span",{"class":"cmp-ReviewAuthor"}) 
            print(random.text)
            for k in i.findAll("a",{"class":"cmp-ReviewAuthor-link"}):
              print(k.text)
              #print(k.prettify())
            print(ReviewTitle.text)
            print(ReviewRating.text)			
            print(ReviewText.text)

            print("+++--------------------------------------------")
        print("bye----------------------------------------------")

        #now we want to print only the text part of the anchor. 
        #find all the elements of a, i.e anchor 
    else: 
        print("Error") 
          
news()