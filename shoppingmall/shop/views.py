from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth  
from django.template import loader
from .models import Profile,Otb,Detail,CartItem,BuyInfo,QnA
from django.db.models import Q
from django.contrib import messages
from .forms import QnAForm


# Create your views here.



# 메인페이지
def index(request):
    outwear =  get_object_or_404(Otb, pk=1)
    top  =  get_object_or_404(Otb, pk=2)
    pants =  get_object_or_404(Otb, pk=3)
    skirt =  get_object_or_404(Otb, pk=4)
    context={
        'outwear':outwear,
        'top':top,
        'pants':pants,
        'skirt':skirt
    }     
    return render(request,"shop/index.html",context)



# OUTWEAR/TOP/BOTTOM 페이지
def otb(request, id):
    if id is not None:
        item = get_object_or_404(Otb, pk=id)
        return render(request,'shop/otb.html', { 'item':item } )
    return redirect("index")



# 디테일 페이지
def detail(request, num1, num2):
    item = Detail.objects.filter(num1=num1).get(num2=num2)
    return render(request,"shop/detail.html",{'item':item})



# 서치페이지
def search(request):
    return render(request,"shop/search.html")

def searchResult(request):
    products = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        products = Detail.objects.all().filter(name__contains=query)

    return render(request, 'shop/search.html', {'query':query, 'products':products})


# 장바구니 & 구매
def cart(request):
    # 로그인 되었을때
    if request.user.is_authenticated: 
        profile = Profile.objects.get(user=request.user)

        if 'cart' == request.GET.get('cartIn'): # cart 클릭
            try:
                item = Detail.objects.filter(num1=request.GET.get('item_num1')).get(num2=request.GET.get('item_num2'))
                cartItem_ex = CartItem.objects.filter(Q(user=request.user)&Q(name=item.name)).get(size=request.GET.get('item_size'))
                if cartItem_ex:
                    cartItem_ex.count += int(request.GET.get('item_count'))
                    cartItem_ex.save()

            except:
                cartItem_new = CartItem()
                cartItem_new.num1 = item.num1
                cartItem_new.num2 = item.num2
                cartItem_new.name = item.name
                cartItem_new.price = item.price
                cartItem_new.size = request.GET.get('item_size')
                cartItem_new.count = request.GET.get('item_count')
                cartItem_new.total_price = int(item.price)*int(request.GET.get('item_count'))
                cartItem_new.user = request.user
                cartItem_new.save()

            total_price_sum = 0
            cartItems = CartItem.objects.filter(user=request.user)
            for cartItem in cartItems:
                total_price_sum += cartItem.total_price
            context={
                'cartItems':cartItems,
                'total_price_sum' : total_price_sum,
                'user': request.user,
                'address': profile.address
            }
            return render(request,"shop/cart.html", context)

        elif 'buy' == request.GET.get('buy'): 
            item = Detail.objects.filter(num1=request.GET.get('item_num1')).get(num2=request.GET.get('item_num2'))
            total_price = int(item.price) * int(request.GET.get('item_count'))
            context={
                'num1' : item.num1,
                'num2' : item.num2,
                'name' : item.name,
                'price' : item.price,
                'size' : request.GET.get('item_size'),
                'count' : request.GET.get('item_count'),
                'total_price' : total_price,
                'user' : request.user,
                'address' : profile.address
            }            
            return render(request,"shop/buy.html",context)

        else: # navbar의 CART 클릭
            total_price_sum = 0
            cartItems = CartItem.objects.filter(user=request.user)
            for cartItem in cartItems:
                total_price_sum += cartItem.total_price
            context = {
                'cartItems':cartItems,
                'total_price_sum' : total_price_sum,
                'user': request.user,
                'address': profile.address
            }
            return render(request,"shop/cart.html",context)


    #로그인 안되었을때
    elif not request.user.is_authenticated:
        return redirect("login")


#장바구니 상품 삭제
def cartDelete(request,name,size):
    item = CartItem.objects.filter(Q(user=request.user)&Q(name=name)).get(size=size)
    item.delete()
    return redirect("cart")


# 구매하기
def payCart(request):
    cartItems = CartItem.objects.filter(user=request.user)
    for cartItem in cartItems:
        buyInfo = BuyInfo()
        buyInfo.name = cartItem.name
        buyInfo.price = cartItem.price
        buyInfo.size = cartItem.size
        buyInfo.count = cartItem.count
        buyInfo.total_price = cartItem.total_price
        buyInfo.user = request.user
        buyInfo.customerName = request.POST.get('customerName')
        buyInfo.customerTel = request.POST.get('customerTel')
        buyInfo.save()
   
    cartItems.delete()
    messages.success(request,"구매가 완료되었습니다")
    return redirect("index")

def payBuy(request):
    buyInfo = BuyInfo()
    buyInfo.name = request.POST.get('name')
    buyInfo.price = request.POST.get('price')
    buyInfo.size = request.POST.get('size')
    buyInfo.count = request.POST.get('count')
    buyInfo.total_price = request.POST.get('total_price')
    buyInfo.user = request.user
    buyInfo.customerName = request.POST.get('customerName')
    buyInfo.customerTel = request.POST.get('customerTel')
    buyInfo.save()

    messages.success(request,"구매가 완료되었습니다")
    return redirect("index")




# 회원가입,로그인
def login_view(request):
    if request.method == "POST":
        username = request.POST['id']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request,user)
        return redirect("index")
    
    else:
        return render(request,"shop/login.html")

    

def logout_view(request):
    auth.logout(request)
    
    return redirect("index")


def signup_view(request):
    if request.method == "POST":
        signup_id = request.POST.get('signup_id')
        try:
            _id = User.objects.get(username=signup_id)
        except:
            _id = None
        
        if _id is None:
            user = User.objects.create_user(
                username = request.POST['signup_id'],
                password = request.POST['signup_password'],
                email = request.POST['signup_email']
            )

            address = request.POST['signup_address']
            profile = Profile(user=user, address=address)
            profile.save()
            auth.login(request, user)
            return redirect("index")

        else:
            messages.error(request,'이미 존재하는 아이디입니다') 
            return render(request,"shop/login.html")


# Q&A 게시판
def qnaList(request):
    context = {
        'qnas': QnA.objects.all().order_by('-created_at')
    }
    return render(request,'shop/qnaMain.html',context)


def qnaCreate(request):   
    if request.user.is_authenticated: 
        if request.method == 'POST':
            item = QnA(
                title = request.POST['title'],
                name = request.POST['name'],
                content=request.POST['content'],
                image=request.FILES['image'],
                password= request.POST['password']
            )
            item.save()
            return redirect("qnaList")
        
        form = QnAForm()
        return render(request,'shop/qnaCreate.html',{'form':form})
    
    elif not request.user.is_authenticated:
        return redirect("login")


def qnaSearch(request):
    products = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        products = QnA.objects.all().filter(name__contains=query)

    return render(request, 'shop/qnaMain.html', {'query':query, 'qnas':products})


def qnaPwConfirm(request,qnaId):
    return render(request,'shop/pwConfirm.html',{'qnaId':qnaId})


def qnaDetail(request):
    if 'id' in request.GET:
        item = get_object_or_404(QnA, pk=request.GET.get('id'))
        if item.password == request.POST.get('pw'):   
            return render(request,'shop/qnaDetail.html',{'item':item})

    return redirect("qnaList")


def qnaDelete(request):
    qna = get_object_or_404(QnA, pk=request.GET.get('id'))
    qna.delete()
    return redirect("qnaList")


def qnaUpdate(request):
    if request.method == "POST" and 'id' in request.POST:
        item = get_object_or_404(QnA,pk=request.POST.get('id'))
        form = QnAForm(request.POST,instance=item)
        if form.is_valid():
            form.save()

    elif request.method == "GET":
        item = get_object_or_404(QnA,pk=request.GET.get('id'))
        form = QnAForm(instance=item)
        return render(request,'shop/qnaUpdate.html',{'form':form})
    
    return redirect("qnaList")


      


  
    
