from django.contrib.auth.forms import UserCreationForm
from .constant import ACCOUNT_TYPE, GENDER_TYPE
from django import forms
from django.contrib.auth.models import User
from .models import UserAccount, UserAddress
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserAddress, UserAccount

class UserRegistrationForm(UserCreationForm):
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    street = forms.CharField()
    city = forms.CharField()
    postal_code = forms.IntegerField()
    country = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'account_type', 'gender', 'street', 'city', 'postal_code', 'country', 'birth_date']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            account_type = self.cleaned_data.get('account_type')
            birth_date = self.cleaned_data.get('birth_date')
            gender = self.cleaned_data.get('gender')
            street = self.cleaned_data.get('street')
            city = self.cleaned_data.get('city')
            postal_code = self.cleaned_data.get('postal_code')
            country = self.cleaned_data.get('country')

            UserAddress.objects.create(user=user, street=street, postal_code=postal_code, city=city, country=country)
            UserAccount.objects.create(user=user, account_type=account_type, birth_date=birth_date, gender=gender, account_no=4800000 + user.id)

        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200'
                    'text-gray-700 border border-gray-200 rounded'
                    'py-3 px-4 leading-tight focus-outline-none'
                    'focus:bg-white focus:border-gray-500'
                )
            })



class UserUpdateForm(forms.ModelForm):
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    birth_date = forms.DateField()
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street = forms.CharField() 
    city = forms.CharField()
    postal_code = forms.IntegerField()
    country = forms.CharField()
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class' : (
                    'appearance-none block w-full bg-gray-200'
                    'text-gray-700 border border-gray-200 rounded'
                    'py-3 px-4 leading-tight focus-outline-none'
                    'focus:bg-white focus:border-gray-500' 
                )
            })
            # jodi user er account thake 
        if self.instance:
            try:
                user_account = self.instance.account
                user_address = self.instance.address
            except UserAccount.DoesNotExist:
                user_account = None
                user_address = None
                
            if user_account:
                self.fields['account_type'].initial = user_account.account_type
                self.fields['gender'].initial = user_account.gender
                self.fields['birth_date'].initial = user_account.birth_date
                self.fields['street'].initial = user_address.street
                self.fields['city'].initial = user_address.city
                self.fields['postal_code'].initial = user_address.postal_code
                self.fields['country'].initial = user_address.country
        
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            
            user_account, created = UserAccount.objects.get_or_create(user=user)
            user_address, created = UserAddress.objects.get_or_create(user = user)
            #account thakle user_account a dibe naile created kore dibe get_or_create function
            user_account.account_type = self.cleaned_data['account_type']
            user_account.gender = self.cleaned_data['gender']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.save()
            
            user_address.street = self.cleaned_data['street']
            user_address.city = self.cleaned_data['city']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.country = self.cleaned_data['country']
        
        return user