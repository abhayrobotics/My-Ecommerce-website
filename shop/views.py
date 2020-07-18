from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order123, Orderupdate
from math import ceil
import json
# from django.db import Product
# Create your views here.

# for payment options
from django.views.decorators.csrf import csrf_exempt
from .Paytm import Checksum

MERCHANT_KEY = 'kbzk1DSbJiV_O3p5';


def index(request):
    # product = Product.objects.all()
    # print(product)
    # length of slides
    # n=len(product)
    # nSlides = n//4 +ceil((n/4)-(n//4))
    # # print(nSlides)
    # range1 =range(1,nSlides)
    # trial 1 #lec 33
    # params= {'no _of slides':nSlides,
    #           'range': range(1,nSlides),
    #           'product':products}
    # trial 2 #lec 34:testing two slides
    # allprods=[[product, range1 , nSlides],
    #           [product, range1, nSlides]]

    # trial 3 #lec 35 :category wise
    # blank list allprods having category wise sub list as prod
    allprods = []
    catprods = Product.objects.values('category', 'id')
    # print(catprods)

    cats = {item['category'] for item in catprods}
    # print(cats)

    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        range1 = range(1, nSlides)
        allprods.append([prod, range1, nSlides])

    params = {'allprods': allprods}
    return render(request, 'shop/index.html', params)


def search(request):
    query = request.GET.get('search')
    allprods = []
    catprods = Product.objects.values('category', 'id')
    # print(catprods)

    cats = {item['category'] for item in catprods}
    # print(cats)

    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchmatch(query,item)]

        n = len(prod)
        nSlides = n//4 + ceil((n/4)-(n//4))
        range1 = range(1, nSlides)

        if len(prod)!=0:
            allprods.append([prod, range1, nSlides])
    params= {'allprods': allprods,'msg': ""}

    # if no search found
    if len(allprods) ==0 or len(query) <3:
        params= {'msg': "No Items Found, Please search Relevant keywords"}

    params = {'allprods': allprods}
    return render(request, 'shop/search.html', params)
    
def searchmatch(query,item):
    # if query found return true else false
    # here we convert both the query and result to lower case to find
    # Also only if the whole str matches with the result it shows ...
    # 
    if (query.lower() in item.product_name.lower() ) or (query.lower() in item.desc.lower()) or (query.lower() in item.category.lower() ):
        return True
    else:
        return False


def about(request):
    return render(request, 'shop/about.html')


def contact(request):

    if request.method == "POST":
        print(request)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        purpose = request.POST.get('purpose', '')
        desc = request.POST.get('desc', '')

        # print(name,email,purpose,desc)
        contact1 = Contact (name=name, email=email,purpose=purpose,desc= desc)
        contact1.save()
    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method == "POST":
        # print(request)
        orderid =request.POST.get('orderid','')
        email = request.POST.get('email', '')
        
        try:
            order =Order123.objects.filter(order_id=orderid,email=email)
            if len(order)>0:
    
                update = Orderupdate.objects.filter(order_id=orderid)
                updates= []
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response = json.dumps(updates,default=str)
                    response =json.loads(response)
                print(response)
                print(type(response))
                return render(request, 'shop/tracker.html',{'response':response})
            else:
                
                return HttpResponse("{}")
        except Exception as e:
            return HttpResponse('{}')
    return render(request, 'shop/tracker.html')




def product(request, myid):

    # fetching the product using id
    product = Product.objects.filter(id=myid)

    print(product)

    # we are passing a parameter having details  of product1
    return render(request, 'shop/product.html', {'product': product})


def checkOut(request):
    # if request post the return parameter esle normal html file
    if request.method == "POST":
        print(request)
        items_json = request.POST.get('items_json', '')
        # order_id = request.POST.get('order_id', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address', '')
        addressl2 = request.POST.get('addressl2', '')
        phone = request.POST.get('phone', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zipcode = request.POST.get('zipcode', '')
        # print(name,email,purpose,desc)

        # adding value of  1 object
        order1 = Order123(items_json=items_json ,name=name, email=email,address= address + "  "+ addressl2,phone= phone,city= city, state= state,zipcode= zipcode,amount=amount)
        order1.save()
        # order tracking
        update = Orderupdate(order_id=order1.order_id, update_desc="Your order has been Placed")
        update.save()

        checkout_complete= True
        # return render(request, 'shop/checkout.html',{'checkout_complete':checkout_complete,
        # 'order1':order1})

        # request paytm to accept payment
        params_dict = {
            'MID':'WorldP64425807474247',
            # 'MID':'HoGFqv04611365726244',
            
            'ORDER_ID': str(order1.order_id),
            'TXN_AMOUNT':str(amount),
            'CUST_ID': str(email),

            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
	        'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest',
        }
        params_dict['CHECKSUMHASH'] =Checksum.generate_checksum(params_dict,MERCHANT_KEY)



        return render(request,'shop/paytm.html',{'params_dict':params_dict})

          
    return render(request, 'shop/checkout.html')


def cart(request):
    return HttpResponse("we are at cart")


def feedback(request):
    return HttpResponse("we are at feedback")


@csrf_exempt
def  handlerequest(request):
    # paytm will send  post request here
    
    # return HttpResponse("Done")
    form = request.POST
    response_dict ={}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        if response_dict['RESPCODE'] =='01':
            print("order Successfull")
        else:
            print("order Not Successfull"+ response_dict['RESPMSG'])
    return render(request,'shop/paymentstatus.html',{'response':response_dict})
