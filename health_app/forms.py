from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, MedicalRecord, Appointment

class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('patient', 'Patient'),
        ('health_worker', 'Health Worker'),
    ]

    user_type = forms.ChoiceField(
        label='User Type',
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'password1', 'password2', 'user_type')

    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(attrs={'type': 'email', 'class': 'form-control'}),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'Please enter your password.',
            'invalid': 'Please enter a correct password.',
        },
        label="Password"
    )
    
class MedicalInfoForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ('blood_group', 'age', 'disease', 'height', 'weight', 'genotype')
    
    blood_group = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    age = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    disease = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    height = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    weight = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    genotype = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class MedicalRecordFilterForm(forms.Form):
    condition_choices = [
        ('', 'All'),
        ('Malaria', 'Malaria'),
        ('Typhoid', 'Typhoid'),
    ]
    condition = forms.ChoiceField(choices=condition_choices, required=False, widget=forms.Select(attrs={'class': 'custom-dropdown'})
    )

class DateTimePickerWidget(forms.TextInput):
    input_type = 'datetime-local'

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['health_worker', 'date']

    def __init__(self, user, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['health_worker'].queryset = CustomUser.objects.filter(userprofile__user_type='health_worker')
        self.fields['health_worker'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget = DateTimePickerWidget(attrs={'class': 'form-control'})
    

class AppointmentDecisionForm(forms.Form):
    decision = forms.ChoiceField(
        choices=[('accepted', 'Accept'), ('rejected', 'Reject')],
        widget=forms.RadioSelect,
    )