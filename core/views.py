
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import CustomUser
from store.models import *
from store.views import *
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.conf import settings 
from django.core.mail import send_mail
# from .tasks import send_otp_email
from django.core.exceptions import ObjectDoesNotExist
import sweetify
import random
from .emails import *


class CreateUser(View):
    """
    View for rendering and processing the registration form.

    This view renders the registration form in 'register.html' and handles user registration form submission.

    Attributes:
        None

    Methods:
        get(request): Handles GET requests to render the registration form.
        post(request): Handles POST requests to process user registration.
    """
    def get(self, request):
        # Render the registration form page
        return render(request, 'register.html')

    def post(self, request):
        # Handle user registration form submission
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Username length validation
        if len(username) < 3:
            messages.warning(request, "Username must be at least 3 characters long.")
            return redirect('register')
        
        # Password validation checks
        try:
            validate_password(password, user=None)
        except ValidationError as e:
            # Display validation error messages and redirect to registration form
            messages.warning(request, e)
            return redirect('register')
        
        # Check if the passwords match
        if password != confirm_password:
            # Display a warning and redirect to registration form
            messages.warning(request, "Passwords do not match")
            return redirect('register')

        # Check if the email is already registered
        if CustomUser.objects.filter(email=email).exists():
            # Display a warning and redirect to registration form
            messages.warning(request, "Email already registered, please use a different email")
            return redirect('register')
        otp = str(random.randint(100000, 999999))
        account_verification_email(email,otp)
        request.session['signup_data'] = {'username':username,'email': email,'password': password, 'otp': otp}

        # Create a new user account and display a success message
        # CustomUser.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "OTP send to your mail.")
        return redirect('verify_otp')

class VerifyOTP(View):

  def get(self, request):
  
    if request.session.get('signup_data'):
      return render(request, 'verify_otp.html')
    return redirect('register')

  def post(self, request):
    reciveotp = request.POST.get('otp1') + request.POST.get('otp2') + request.POST.get('otp3') + request.POST.get('otp4') + request.POST.get('otp5') + request.POST.get('otp6')
    signup_data =  request.session.get('signup_data',{})
    if not signup_data:
        messages.error(request, 'OTP expired or invalid')
        return redirect('signin')
    otp = signup_data.get('otp')
    username = signup_data.get('username')
    email = signup_data.get('email')
    password = signup_data.get('password')
    print(reciveotp, otp)
    if reciveotp != otp:
        messages.error(request, 'OTP mismatch')
        return redirect('verify_otp')
    user = CustomUser.objects.create_user(username=username, email=email, password=password)
    user.save()
    messages.success(request, 'Registration successful. You can now sign in.')
    del request.session['signup_data']
    return redirect('signin')

class ResendOTP(View):
  def get(self, request):
    signup_data = request.session.get('signup_data',{})
    if signup_data:
      email = signup_data.get('email')
      username = signup_data.get('username')
      otp = str(random.randint(100000, 999999))
      account_verification_email(email, otp)
      signup_data['otp'] = otp
      return redirect('verify_otp')
    return redirect('register')
            
class SignIn(View):
    """
    View for rendering and processing the sign-in form.

    This view renders the sign-in form in 'signin.html' and handles user sign-in form submission.

    Attributes:
        None

    Methods:
        get(request): Handles GET requests to render the sign-in form.
        post(request): Handles POST requests to process user sign-in.
    """
    def get(self, request):
        # Render the sign-in form page
        return render(request, 'signin.html')

    def post(self, request):
        # Handle user sign-in form submission
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the user exists and is blocked
        try:
            user = CustomUser.objects.get(email=email)
            if user.is_blocked:
                messages.warning(request, 'You are banned')
                return redirect('signin')
        except ObjectDoesNotExist:
            pass

        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                # If authentication is successful and the user is active, log them in and redirect to the home page
                login(request, user)
                return redirect('home')
            else:
                # If the user is inactive, display a warning and redirect to the sign-in form
                messages.warning(request, 'User is inactive')
                return redirect('signin')
        else:
            # If authentication fails, display a warning and redirect to the sign-in form
            messages.warning(request, 'Invalid email or password')
            return redirect('signin')

class SignOut(View):
    """
    View for handling user sign-out.

    This view handles user sign-out by logging the user out and redirecting to the home page.

    Attributes:
        None

    Methods:
        get(request): Handles GET requests to perform user sign-out.
    """
    def get(self, request):
        # Log the user out and redirect to the home page
        logout(request)
        return redirect('home')

    
class UserProfileView(LoginRequiredMixin, View):


  def get(self, request):
    return render(request, 'user_profile.html')
  
class UserManageAddress(View):

  def get(self, request):
    addresses = request.user.user_addresses.all()
    return render(request, 'manage_address.html', {'addresses':addresses})
  
class UserAddAddress(View):


  def post(self, request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    gender = request.POST.get('gender')
    mobile = request.POST.get('mobile')
    email = request.POST.get('email')
    address = request.POST.get('address')
    address_type = request.POST.get('address_type')
    place = request.POST.get('place')
    landmark = request.POST.get('landmark')
    pincode = request.POST.get('pincode')
    post = request.POST.get('post')
    district = request.POST.get('district')
    state = request.POST.get('state')
    UserAddress.objects.create(
            user=request.user,
            address_type=address_type,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            mobile=mobile,
            email=email,
            address=address,
            place=place,
            landmark=landmark,
            pincode=pincode,
            post=post,
            district=district,
            state=state
        )
    messages.success(request, 'Address added successfully')
    return redirect(request.META.get('HTTP_REFERER'))

class UserUpdateAddress(View):
    
  def post(self, request, pk):
    user_address = UserAddress.objects.get(id=pk)
    user_address.address_type = request.POST.get('address_type')
    user_address.name = request.POST.get('name')
    user_address.gender = request.POST.get('gender')
    user_address.mobile = request.POST.get('mobile')
    user_address.address = request.POST.get('address')
    user_address.place = request.POST.get('place')
    user_address.pincode = request.POST.get('pincode')
    user_address.landmark = request.POST.get('landmark')
    user_address.save()
    messages.success(request, 'Address Updated')
    return redirect('manage_address')
  
class UserDeleteAddress(View):

  def get(self, request, pk):
    useraddress = UserAddress.objects.get(id=pk)
    useraddress.delete()
    messages.error(request, 'Address deleted')
    return redirect('manage_address')