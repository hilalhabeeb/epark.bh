from django import forms
from .models import ParkingSession




class ParkingSessionForm(forms.ModelForm):
    class Meta:
        model = ParkingSession
        fields = ['vehicle_number', 'parking_location']
