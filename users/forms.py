from django import forms
import re 
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.models import Group, Permission
from events.forms import StyledFormMixin

from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm
from users.models import CustomUser
from django.contrib.auth import get_user_model
User = get_user_model()

class StyledFormMixin2:
    default_classes = (
        "border-2 border-gray-300 "
        "bg-slate-700 "
        "p-1 w-full rounded-lg shadow-sm "
        "focus:border-rose-500 focus:ring-rose-500"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == "name":
                classes = self.default_classes
                field.widget.attrs["class"] = classes
                field.widget.attrs["placeholder"] = f"Enter {field.label.lower()}"
           



class StyledFormMixin3:
    """
    Mixin to apply consistent styling to Django form fields.
    Compatible with Form and ModelForm.
    """

    base_classes = (
        "w-full p-3 rounded-lg border border-gray-300 "
        "focus:outline-none focus:ring-2 focus:ring-rose-500 "
        "focus:border-rose-500"
    )

    select_classes = (
        "w-full p-3 rounded-lg border border-gray-300 "
        "bg-white focus:outline-none focus:ring-2 "
        "focus:ring-rose-500 focus:border-rose-500"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            widget = field.widget

            if isinstance(widget, forms.Select):
                widget.attrs.setdefault("class", self.select_classes)
            elif isinstance(
                widget,
                (
                    forms.TextInput,
                    forms.EmailInput,
                    forms.PasswordInput,
                    forms.NumberInput,
                    forms.DateInput,
                ),
            ):
                widget.attrs.setdefault("class", self.base_classes)

class StyledFormMixin4:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": (
                    "w-full px-3 py-2 rounded-md "
                    "border border-gray-300 text-black bg-slate-500"
                )
            })



class StyledFormMixin5:
    """Mixing to apply style"""
    def __init__(self,*arg,**kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()
    default_classes = "border-2 border-gray-300 p-1 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name,field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} bg-gray-200 ",
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows':5
                }) 
            elif isinstance(field.widget,forms.SelectDateWidget):
                # print("I am called!")
                field.widget.attrs.update({
                    'class': "border-2 border-gray-300 p-1 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500",
                }) 
            elif isinstance(field.widget,forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': " p-1 rounded-lg "
                })

class StyledFormMixin6:
    default_classes = (
        "border-2 border-gray-300 p-1 w-full rounded-lg shadow-sm "
        "focus:border-rose-500 focus:ring-rose-500"
    )

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            classes = self.default_classes
      
            if field_name == "username":
                classes += " bg-rose-200"
            
            label = field.label if field.label else field_name.replace('_', ' ')
            field.widget.attrs['placeholder'] = f"Enter {label.lower()}"
            field.widget.attrs["class"] = classes


class CustomRegistraionForm(StyledFormMixin,forms.ModelForm):
   password1 = forms.CharField(widget=forms.PasswordInput)
   confirm_password = forms.CharField(widget=forms.PasswordInput)
   
   class Meta:
      model = User
      fields = ['username','first_name','last_name', 'password1','confirm_password','email']

   def clean_email(self):
      email = self.cleaned_data.get('email')
      email_exists = User.objects.filter(email = email).exists()

      if email_exists:
         raise forms.ValidationError('email already exist!')
      
      return email

   def clean_password1(self):
      password1 = self.cleaned_data.get('password1')
      errors = []

      if len(password1)<8:
         errors.append('Password must be 8 characters long.')

      if not re.search(r'[A-Z]',password1):
         errors.append('Password must include at least one uppercase letter.')
      if not re.search(r'[a-z]',password1):
         errors.append('Password must include at least one lowercase letter.')
      if not re.search(r'[0-9]',password1):
         errors.append('Password must include at least one number.')
      if not re.search(r'[@#$%^&+=]',password1):
         errors.append('Password must include at least one special character.')
         
      if errors:
         raise forms.ValidationError(errors)
      
      return password1
   
   def clean(self):   #non-field error
      cleaned_data = super().clean()
      password1 = cleaned_data.get('password1')
      confirm_password = cleaned_data.get('confirm_password')

      if password1 != confirm_password:
         raise forms.ValidationError('password did not match!')
      
      return cleaned_data
   
   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.help_text = None

   


class LoginForm(AuthenticationForm, StyledFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        self.apply_styled_widgets()  


class AssignRoleForm(StyledFormMixin4,forms.Form):
   role = forms.ModelChoiceField(
      queryset = Group.objects.all(),
      empty_label = "Select a Role"
   )

class CreateGroupForm(StyledFormMixin2, forms.ModelForm):
   permissions = forms.ModelMultipleChoiceField(
      queryset = Permission.objects.all(),
      widget = forms.CheckboxSelectMultiple,
      required = False,
      label="Assign Permission"
   )
   class Meta:
      model = Group
      fields = ['name', 'permissions']
  

class EditProfileForm(StyledFormMixin5, forms.ModelForm):
   class Meta:
      model = CustomUser
      fields = ['email','first_name', 'last_name','bio','profile_image','phone_no']
    


#password change forms

class CustomPasswordChangeForm(StyledFormMixin6,PasswordChangeForm):
   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   # AuthenticationForm init FIRST
        self.apply_styled_widgets()  

class CustomPasswordResetForm(StyledFormMixin6,PasswordResetForm):
   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   # AuthenticationForm init FIRST
        self.apply_styled_widgets()
        
class CustomPasswordResetConfirmForm(StyledFormMixin6,SetPasswordForm):
   def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   # AuthenticationForm init FIRST
        self.apply_styled_widgets()  

