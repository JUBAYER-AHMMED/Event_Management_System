from django import forms
from events.models import Event,Participant,Category


class StyledFormMixin:
    """Mixing to apply style"""
    # border-2 border-gray-300
    default_classes = "p-1 w-full rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name,field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput)):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} bg-white-200",
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
                   
            elif isinstance(field.widget,forms.RadioSelect):
                field.widget.attrs.update({
                    'class': " p-1 rounded-lg "
                })
                
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'type': 'time'
                })


class StyledFormMixin2:
    """Mixing to apply style"""
    # border-2 border-gray-300
    default_classes = "p-3 w-full rounded-lg shadow-lg focus:border-rose-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name,field in self.fields.items():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput)):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} bg-slate-500/20",
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget,forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} bg-slate-500/20",
                    'placeholder': f"Enter {field.label.lower()}",
                    'rows':5
                }) 
            
            elif isinstance(field.widget, forms.SelectDateWidget):
                    field.widget.attrs.update({
                        'class': ("px-3 py-2  gap-2 rounded-lg bg-slate-800 text-white "
                        "border border-white/20 focus:border-rose-500 "
                        "focus:ring-rose-500")
                    })


                   
            elif isinstance(field.widget,forms.RadioSelect):
                field.widget.attrs.update({
                    'class': " p-1 rounded-lg "
                })
                
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    'class': (
            "p-3 w-full rounded-lg bg-slate-500/20 text-white "
            "border border-white/20 focus:border-rose-500 "
            "focus:ring-rose-500"
        ),
        'type': 'time'
    })
# cng 



class EventModelForm(StyledFormMixin2, forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description','date','time','location','category']
        widgets={
            'date': forms.SelectDateWidget(),
            'category': forms.RadioSelect(),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    '''using mixing widget'''
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()

class CategoryModelForm(StyledFormMixin2, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

    '''using mixing widget'''
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()



class ParticipantModelForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email']

    '''using mixing widget'''
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()

