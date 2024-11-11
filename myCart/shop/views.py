from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Orders,Orderupdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from paytm import checksum
# Create your views here.


def index(request):
    # products= Product.objects.all()
    # n= len(products)
    # nSlides= n//4 + ceil((n/4) + (n//4))
   #params={'no_of_slides':nSlides, 'range':range(1,nSlides), 'product': products}
    # allprods=[[products,range(1,nSlides),nSlides],
    #           [products,range(1,nSlides),nSlides]]
    allprods=[]
    catprods=Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n=len(prod)
        nSlides=n // 4 + ceil((n/4)-(n//4))
        allprods.append([prod,range(1, nSlides), nSlides])
    params={'allprods':allprods}  
    return render(request,"shop/index.html", params)


def about(request):
    return render(request,'shop/about.html')


def contact(request):
    thank=False
    if request.method == "POST":
        print(request)
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        print(name, email, phone, desc)
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank=True
    return render(request, 'shop/contact.html',{'thank':thank})


def tracker(request):
    if request.method == "POST":
        OrderId= request.POST.get('OrderId', '')
        email = request.POST.get('email', '')
        
        order=Orders.objects.filter(order_id=OrderId,email=email)
        if len(order)>0:
                update=Orderupdate.objects.filter(order_id=OrderId)
                updates=[]
                for item in update:
                    updates.append({'text':item.update_desc,})
                response=json.dumps([updates,order[0].items_json],default=str)
                return HttpResponse(response)
        else:
                pass    
    return render(request,'shop/tracker.html')

# def tracker(request):
#     if request.method == "POST":
#         OrderId = request.POST.get('OrderId', '')
#         email = request.POST.get('email', '')
        
#         order = Orders.objects.filter(order_id=OrderId, email=email)
#         if len(order) > 0:
#             update = Orderupdate.objects.filter(order_id=OrderId)
#             updates = []
#             for item in update:
#                 updates.append({
#                     'text': item.update_desc,
#                     'time': item.update_time.strftime('%Y-%m-%d %H:%M:%S')  # Convert datetime to string
#                 })
#             response = json.dumps(updates)
#             return HttpResponse(response, content_type="application/json")
#         else:
#             # You might want to handle the case when no orders are found
#             return HttpResponse(json.dumps({'error': 'No order found'}), content_type="application/json")
    
#     return render(request, 'shop/tracker.html')



def search(request):
     return render(request,'shop/search.html')


def productview(request, myid):
    product=Product.objects.filter(id=myid)
    print(product)
    return render(request, "shop/prodview.html", {'product':product[0]})


# def checkout(request):
#     if request.method == "POST":
#         print(request)
#         items_json=request.POST.get('itemsJson', '')
#         name = request.POST.get('name', '')
#         amount= request.POST.get('amount', '')
#         email = request.POST.get('email', '')
#         address= request.POST.get('address1', '') + " " + request.POST.get('address2', '')
#         city= request.POST.get('city', '')
#         state= request.POST.get('state', '')
#         zip_code= request.POST.get('zip_code', '')
#         phone= request.POST.get('phone', '')
#         order = Orders(items_json=items_json, name=name, email=email, address=address, city=city, state= state , zip_code=zip_code, phone=phone,amount=amount)
#         order.save()
#         update=Orderupdate(order_id=order.order_id,update_desc="The order has been placed")
#         update.save()
#         thank=True
#         id=order.order_id
#        # return render(request, 'shop/checkout.html', {'thank':thank, 'id':id})
#         #request to paytm to reecive money
#     param_dict={

#             'MID': '',
#             'ORDER_ID': 'order.order_id',
#             'TXN_AMOUNT': '1',
#             'CUST_ID': 'email',
#             'INDUSTRY_TYPE_ID': 'Retail',
#             'WEBSITE': 'WEBSTAGING',
#             'CHANNEL_ID': 'WEB',
#             'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

#     }
#     return  render(request, 'shop/paytm.html', {'param_dict': param_dict})
        

#  return render(request,'shop/checkout.html')
def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = Orderupdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        # Request paytm to transfer the amount to your account after payment by user
        param_dict = {

                'MID': 'Your-Merchant-Id-Here',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

        }
       # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})

    return render(request, 'shop/checkout.html')


@csrf_exempt
def handlerequest(request):
    return HttpResponse('done')
    pass
