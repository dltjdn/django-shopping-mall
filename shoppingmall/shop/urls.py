from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('singup/',views.signup_view, name="signup"),

    path('otb/<int:id>/', views.otb, name="otb"),
    path('detail/<int:num1>/<int:num2>/', views.detail, name="detail"),

    path('search/',views.search, name="search"),
    path('searchResult/',views.searchResult, name="searchResult"),
    
    path('cart/', views.cart, name="cart"),
    path('cartDelete/<str:name>/<str:size>/', views.cartDelete, name="cartDelete"),
    path('payCart/', views.payCart, name="payCart"),
    path('payBuy/', views.payBuy, name="payBuy"),

    path('qnaList/', views.qnaList, name="qnaList"),
    path('qnaCreate/',views.qnaCreate,name="qnaCreate"),
    path('qnaDetail/',views.qnaDetail,name="qnaDetail"),
    path('qnaSearch/',views.qnaSearch,name="qnaSearch"),
    path('qnaPwConfirm/<int:qnaId>',views.qnaPwConfirm,name="qnaPwConfirm"),
    path('qnaUpdate',views.qnaUpdate,name="qnaUpdate"),
    path('qnaDelete',views.qnaDelete,name="qnaDelete"),
    
]

