from django.contrib import admin
from .models import Profile,Otb,Detail,CartItem,BuyInfo,QnA

# Register your models here.

admin.site.register(Profile)
admin.site.register(Otb)
admin.site.register(Detail)
admin.site.register(CartItem)
admin.site.register(BuyInfo)
admin.site.register(QnA)