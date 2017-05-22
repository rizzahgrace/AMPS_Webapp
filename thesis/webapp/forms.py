from .models import RawData_Weather
from django import forms
from django.contrib.auth.models import User


class UploadCSVFile(forms.Form):
    csvfile = forms.FileField()
    owner = forms.ModelChoiceField(
        label="Owner",
        queryset=User.objects.order_by('username'),
        required=True,
        empty_label='Choose an owner'
    )

class recordWeather(forms.ModelForm):
    winddir = forms.FloatField(label="Wind Direction", required=True,)
    windspeedmph = forms.FloatField(label="Wind Speed (mph)", required=True,)
    windspdmph_avg2m = forms.FloatField(label="Wind Speed (mph) Average", required=True,)
    rainin = forms.FloatField(label="Rain", required=True,)
    dailyrainin = forms.FloatField(label="Total Rain", required=True,)
    humidity = forms.FloatField(label="Humidity", required=True,)
    tempf = forms.FloatField(label="Temperature", required=True,)
    pressure = forms.FloatField(label="Pressure", required=True,)

    class Meta:
        model = RawData_Weather
        fields = ['winddir', 'windspeedmph', 'windspdmph_avg2m', 'rainin', 'dailyrainin', 'humidity', 'tempf', 'pressure']


class recordPower(forms.Form):
    grid = forms.FloatField(label="Grid", required=True,)
    load = forms.FloatField(label="Load", required=True,)
    batt_curr = forms.FloatField(label="Battery Current", required=True,)
    batt_pow = forms.FloatField(label="Battery Power", required=True,)
    SP_curr = forms.FloatField(label="Solar Panel Current", required=True,)
    SP_volt = forms.FloatField(label="Solar Panel Voltage", required=True,)


class recordUser(forms.Form):
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=("Username"), error_messages={ 'invalid': ("This value must contain only letters, numbers and underscores.") })
    first_name = forms.CharField(label = "First Name")
    last_name = forms.CharField(label = "Last Name")
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=("Password (again)"))
 
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(("The username already exists. Please try another one."))
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(("The two password fields did not match."))
        return self.cleaned_data
