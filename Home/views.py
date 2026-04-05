from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
import requests
import bs4
from newsapi import NewsApiClient
import sys
import io
import random
from urllib3 import HTTPResponse
import yfinance as yf
from django.views.generic import TemplateView
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8') 
# Create your views here.
class HomePage(TemplateView):
   template_name="Home/Home.html"

   def get_context_data(self, **kwargs):
      context= super().get_context_data(**kwargs) 
      Flag=False
      print("----------------------------------------->",self.request.user.is_authenticated)
      if self.request.user.is_authenticated:
       Flag=True
   
      lis=['nifty','niftymidcap','niftysmall','banknifty']
    
      dic=  {"Nifty":{"Price":"","per":""},
           "Mid100":{"Price":"","per":""},
           "SmallCap":{"Price":"","per":""},
           "BankNifity":{"Price":"","per":""}}
      n=0
    
      for key in dic:
        r=requests.get(f"https://ticker.finology.in/market/index/nse/{lis[n]}")
        soup=bs4.BeautifulSoup(r.text,'html.parser')
        s2=soup.find("div",id="mainContent_clsprice")
        dic[key]["Price"]=s2.find("span",class_="Number").text.strip()
        dic[key]["per"]=s2.find("div",id="mainContent_pnlPriceChange").text.strip()#,class_="small increment" add if request
        n+=1

 #_____________________________________For NEWSE Section_____________________________________#
                                                                                             
      newsapi = NewsApiClient(api_key='95a2a26cd9fd4216aa2d80e9181bd5e1')                   
      newLis=['nifty','Midcap','smallcap','banknifty']

      newseNum=random.randrange(0,3)
    
    # Query for Nifty news
      all_articles = newsapi.get_everything(q=newLis[newseNum],
                                      language='en',
                                      sort_by='publishedAt',
                                      page_size=12)
     
      NewseLis=[]
      urlLis=[]
      for article in all_articles['articles']:
          NewseLis.append(str(article['title']))
          urlLis.append(article['url'])
    
      zip_=zip(NewseLis,urlLis)
      NewLis=list(zip_)
      context['Flag']=Flag
      context['Index']=dic
      context["Newse"]=NewLis      
 #____________________________________________________________________________________________#
      return context
   
class Search(TemplateView):
 
 template_name="Home/Search.html"
 
 def get_context_data(self, **kwargs):
  context= super().get_context_data(**kwargs)
  if (self.request.method=='GET'):
     flag=self.request.session.get("Name",None)
     search=self.request.GET.get("fname","NONE").upper()
     if search!="NONE":
        if " " in search:      
          # Split and join without spaces
          o = search.split()
          result = "".join(o)
        else:
          result=search
        print("Your Result is ",result)
        r=requests.get(f"https://www.screener.in/company/{result}/")
        #Filtring Data
        soup=bs4.BeautifulSoup(r.text,'html.parser')
        s2=soup.find("div",class_="company-ratios")#,class_="card cardscreen mt-md-3"
        s3=s2.find("ul",id="top-ratios")
        s4=s3.find_all("li",class_="flex flex-space-between")
        length=len(s4)
        Heading=[]
        Value=[]
        
        for i in range(length):
           s5=s4[i].find("span",class_="name")
           Heading.append(s5.text.strip())
           s5=s4[i].find("span",class_="number")
           Value.append(s5.text.strip())
        zip_=zip(Heading,Value)
        final_lis=list(zip_)
        #About section 

        About=soup.find_all('div',class_='sub show-more-box about')
        About=About[0].text
        context["Name"]=result
        context["Value"]=final_lis
        context["About"]=About
        context["Symbol"]=result
        context["flag"]=flag
     else:
        return redirect("Home")
  else:
    return redirect("Home") 
  return context
   
def Histroy_Price(request):
    symbol = request.GET.get("symbol", None)
    if symbol:
        ticker = yf.Ticker(f"{symbol}.NS")
        data = ticker.history(period="1y", interval="1d")
        his = {
            "dates": data.index.strftime('%Y-%m-%d').tolist(),
            "prices": data['Close'].tolist()
        }
        return JsonResponse(his)
    return JsonResponse({"error": "No symbol provided"})

def Logout(request):
    request.session.flush()
    return redirect('Home')