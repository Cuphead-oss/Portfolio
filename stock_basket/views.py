from django.shortcuts import render

# Create your views here.
def Main(req):
    pram={}
    
    Name=req.session.get("Name",None)
    pram['flag']=Name
    pram['Name']=Name
    return render(req,"stock_basket/main.html",pram)