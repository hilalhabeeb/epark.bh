from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def home(request):
    return render(request, 'parking/home.html')

def register(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            if User.objects.filter(username=email).exists():
                messages.error(request, 'Email is already taken')
                return redirect('home')
            else:
                user = User.objects.create_user(username=email, password=password, first_name=full_name)
                user.save()
                messages.success(request, 'Account created successfully')
                return redirect('home')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('home')
    else:
        return redirect('home')
    
    
from django.contrib.auth import authenticate, login as auth_login


def login(request):
    """
    Handles user login. Displays a login form and processes form submissions.
    """
    if request.method == 'POST':
        username = request.POST.get('logemail')
        password = request.POST.get('logpassword')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('user_home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'parking/login.html')

@login_required
def user_home(request):

    return render(request, 'parking/userhome.html')

@login_required
def user_logout(request):

    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from .forms import ParkingSessionForm
from .models import ParkingSession

from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
import pytz
from .forms import ParkingSessionForm

def create_parking_session(request):
    # Define Bahrain timezone
    bahrain_tz = pytz.timezone('Asia/Bahrain')

    if request.method == 'POST':
        form = ParkingSessionForm(request.POST)
        if form.is_valid():
            parking_session = form.save(commit=False)
            parking_session.user = request.user
            
            # Get the selected duration
            duration = request.POST.get('duration')

            # Get the current time in Bahrain timezone
            now = timezone.now().astimezone(bahrain_tz)


            # Set start time
            parking_session.start_time = now

            # Determine the end time and amount based on duration
            if duration == '60':  # 1 hour
                parking_session.amount = 0.200
                parking_session.end_time = now + timedelta(hours=1)
            else:  # Default to 30 minutes
                parking_session.amount = 0.100
                parking_session.end_time = now + timedelta(minutes=30)
            
            parking_session.save()
            return redirect('payment_page', session_id=parking_session.id)
    else:
        form = ParkingSessionForm()
    
    # Get the current time in Bahrain timezone
    now = timezone.now().astimezone(bahrain_tz)
    end_time = now + timedelta(minutes=30)  # Default to half-hour from now

    return render(request, 'parking/create_parking_session.html', {
        'form': form,
        'now': now,
        'end_time': end_time,
    })

