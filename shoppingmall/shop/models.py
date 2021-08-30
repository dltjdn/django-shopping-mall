from django.db import models
from django.contrib.auth.models import User
# Create your models here.


#회원가입
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=50)


# OUTWEAR,TOP,BOTTOM (4가지)
class Otb(models.Model):
    photo1 = models.ImageField(blank=True)
    name1 = models.CharField(max_length=20)
    photo2 = models.ImageField(blank=True)
    name2 = models.CharField(max_length=20)
    photo3 = models.ImageField(blank=True)
    name3 = models.CharField(max_length=20)
    photo4 = models.ImageField(blank=True)
    name4 = models.CharField(max_length=20)
    photo5 = models.ImageField(blank=True)
    name5 = models.CharField(max_length=20)
    photo6 = models.ImageField(blank=True)
    name6 = models.CharField(max_length=20)



#디테일페이지
class Detail(models.Model):
    num1 = models.IntegerField()
    num2 = models.IntegerField()

    photo1 = models.ImageField(blank=True)
    photo2 = models.ImageField(blank=True)
    photo3 = models.ImageField(blank=True)
    photo4 = models.ImageField(blank=True)
    
    name = models.CharField(max_length=20)
    price = models.CharField(max_length=20)
    
    info_1 = models.CharField(max_length=30)
    info_2 = models.CharField(max_length=30)
    info_3 = models.CharField(max_length=30)

    def __str__ (self): 
        return self.name

#카트아이템
class CartItem(models.Model):
    num1 = models.IntegerField()
    num2 = models.IntegerField()
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    size = models.CharField(max_length=10)
    count = models.IntegerField()
    total_price = models.IntegerField()

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name


# 구매정보
class BuyInfo(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    size = models.CharField(max_length=10)
    count = models.IntegerField()
    total_price = models.IntegerField()
   
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    customerName = models.CharField(max_length=20)
    customerTel = models.IntegerField()


# Q&A글
class QnA(models.Model):
    title = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    content = models.TextField()
    image = models.ImageField(upload_to="",blank=True)
    password = models.CharField(max_length=20, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title






