from django import forms
from django.forms import ModelForm
from shop.models import QnA
from django.utils.translation import gettext_lazy as _

class QnAForm(ModelForm):
    class Meta:
        model = QnA
        fields = ['title','name', 'content','image', 'password']
        labels={
            'title' : _('제목'),
            'name' : _('작성자'),
            'content' : _('내용'),
            'image':_('첨부파일'),
            'password':_('비밀번호'),
        }
        CHOICES = (
        
                ('배송문의', '배송문의'),
                ('상품문의', '상품문의'),
                ('교환/반품문의', '교환/반품문의'),
                ('기타문의', '기타문의'),
                )
        
    
        widgets = {
            'title': forms.Select(choices=CHOICES,attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs = { 'class': 'form-control'}),
            'content': forms.Textarea(attrs = {'class': 'form-control','rows':20,'cols':80}),
            'password':forms.PasswordInput()

        }