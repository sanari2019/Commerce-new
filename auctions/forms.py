from random import choices
from django import forms
from .models import *
from django.forms import ModelForm


class CreateForm(forms.ModelForm):
    # category = forms.CharField()
    # image = forms.ImageField()
    # title = forms.CharField()
    # price = forms.IntegerField()
    # description = forms.CharField (widget=forms.Textarea)
    # creation_date = forms.DateTimeField()

    class Meta:
        model = Auction
        fields = ['category','image','title', 'price','is_active','description']

        widgets = {
            'category': forms.Select(attrs={'class':'form-control'}),
            
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'price' : forms.NumberInput(attrs={'class':'form-control'}),
            'description' : forms.Textarea(attrs={'class':'form-control'}),
            
        }
            
            # 'creation_date' : forms.DateTimeField(auto_now_add=True),
        

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['category'].queryset = Category.objects.none()


        # def save(self, commit=True):
        # booking = super(BookingForm, self).save(commit=False)
        # if commit:
        #     booking.save()
        #     self.save_m2m()
        #     for location in booking.place.all():
        #         location.inuse = True
        #         location.save()

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_price']

        widgets = {
            'bid_price': forms.NumberInput(attrs={'class':'bid_input'}),
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

        widgets = {
            'comment': forms.Textarea(attrs={'class':'form-control'}),
        }



       
        
        

        

        