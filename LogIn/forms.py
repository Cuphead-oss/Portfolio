from django import forms
from .validators import password_valid

class Login_Form(forms.Form):

    user_email=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Username or Email"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Password","style": ''' width: 100%;
        padding: 10px 12px;
        border: 1px solid #ccc;
        border-radius: 8px;
        font-size: 14px;
        transition: all 0.3s ease;'''}))
    

class Signup(forms.Form):

    name=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Username"}))

    email = forms.EmailField()

    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Password","style": ''' width: 100%;
        padding: 10px 12px;
        border: 1px solid #ccc;
        border-radius: 8px;
        font-size: 14px;
        transition: all 0.3s ease;'''}),validators=[password_valid])
    
    rePassword=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"Re enter Password","style": ''' width: 100%;
        padding: 10px 12px;
        border: 1px solid #ccc;
        border-radius: 8px;
        font-size: 14px;
        transition: all 0.3s ease;'''}))
    
    def clean(self):
        clean=super().clean()
        p1=clean.get('password')
        p2=clean.get('rePassword')

        if p1 and p2 and not p1==p2:
            self.add_error('rePassword','Password did not matched')
        
        return clean

class Code(forms.Form):
    code=forms.CharField(max_length=10,widget=forms.TextInput(attrs={'id':'Code'}))