from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .forms import CreateUserForm, DepositForm, TransferForm, WithdrawalForm
from .models import Transfer, UserAccount 


# Create your views here.

"""
    Terminology dictionary?

    1. The | {'form': form} | allows the form to be rendered into the html templates.
    2. | UserAccount.objects.get(user=request.user) | this allows us to get the object(s) created in the UserAccount model.
    3. | form = Form(request.POST) | this means you're making use of the form and then you can render the form in the html template.
    4. return render(request, 'signup.html', {'form': form}) -- "signup.html" here is the name of the html template we're rendering to.
"""


def homepage(request):
    return render(request, 'layout.html')

# Authenticate Login Request
def loginUser(request):
    
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
                
		if user is not None:
			login(request, user)
			return redirect('dashboard')
                
		else:
			messages.error(request, ("Invalid Username or Password"))	
			return redirect('login')	
                
	else:
		return render(request, 'login.html')

    
# Authenticate Logout Request
def logoutUser(request):

    username = request.user.get_username()
    logout(request)
    messages.success(request, (f"Goodbye, {username}."))
    return redirect('login')

# Register User
def signup(request):

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = UserAccount.objects.create(user=user) # Generates an Account Number for each user after a successful registration.
            username = request.user.get_username()
            login(request, user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('login')
        
    else:
        # Displays a blank form if the user's request is a GET request.
        form = CreateUserForm()

    return render(request, 'signup.html', {'form': form})



""""
    Main Fuctions of the App. 
        When a user is not authenticated, they can't access these pages.  
        Hence, they'll be redirected to the login page - [@login_required]
"""    


@login_required(login_url='login')
def dashboard(request):

    user_account = UserAccount.objects.get(user=request.user) # Let's you access the fields in UserAccount in dashboard template.
    return render(request, 'dashboard.html', {'user_account': user_account})



@login_required(login_url='login')
def deposit(request):
        
    if request.method == 'POST':
        form = DepositForm(request.POST) 
        if form.is_valid(): 
            deposit = form.save(commit=False) # If the form is valid, save the form     

            # Saves and displays the details of the user in the database associating each deposit with the right user.
            deposit.user = request.user
            deposit.user_id = request.user.id
            deposit.first_name = request.user.first_name
            deposit.last_name = request.user.last_name
            deposit.username = request.user.username
            deposit.save()

            # Get amount and add to existing amount of the user
            amount = float(request.POST.get('amount'))
            user_account = UserAccount.objects.get(user=request.user)
            user_account.account_balance = float(user_account.account_balance) + amount
            user_account.save()

            # Message Success for successful deposit
            messages.success(request, f'Your deposit of ₦{amount} was successful!')
        return redirect('dashboard')
    else:
        # Displays a blank form if the user's request is a GET request.
        form = DepositForm()
    
    return render(request, 'deposit.html', {'form': form})



@login_required(login_url='login')
def transfer(request):

    if request.method == 'POST':

        form = TransferForm(request.POST)

        if form.is_valid():
            receiver_account = form.cleaned_data['receiver_account']
            receiver_account = UserAccount.objects.filter(account_number=receiver_account).first()
            amount = float(request.POST.get('amount'))
            
            sender_account = UserAccount.objects.get(user=request.user)

            # Check if sender and receiver's accounts are the same/
            if sender_account == receiver_account:
                messages.success(request, "Beneficiary account must be different from yours.")
                return render(request, 'transfer.html', {'form': form})

            # Checks if the sender has enough balance to make a transfer.
            if float(sender_account.account_balance) < amount:

                messages.error(request, 'Insufficient balance. Make a deposit')
                return redirect('dashboard')
            
            # Sends the money to the receiver's account.
            if receiver_account:

                sender_account = UserAccount.objects.get(user=request.user)
                sender_account.account_balance = float(sender_account.account_balance)
                receiver_account.account_balance = float(receiver_account.account_balance)

                if sender_account.account_balance >= amount:
                    sender_account.account_balance -= amount
                    sender_account.save()

                    receiver_account.account_balance += amount
                    receiver_account.save()
                
                # Saves the transaction into the database.
                transfer = Transfer.objects.create(sender_account=sender_account, 
                                                   receiver_account=receiver_account, 
                                                   amount=amount, user=request.user, 
                                                   sender_username = request.user.username)
                transfer.save()

                messages.success(request, f'Your Transfer of ₦{amount} was successful.')
                
                
                return redirect('dashboard')
            
            # Checks if receiver's account exists
            try:
                receiver_account = UserAccount.objects.get(account_number=receiver_account)
            except UserAccount.DoesNotExist:
                messages.error(request, 'Account Does Not Exist!')
                return redirect('transfer')
        
    else:
        # Displays a blank form if the user's request is a GET request.
        form = TransferForm()

    return render(request, 'transfer.html', {'form': form})



@login_required(login_url='login')
def withdraw(request):

    if request.method == 'POST':
        form = WithdrawalForm(request.POST)
        if form.is_valid():
            withdraw = form.save(commit=False)

            # Saves and displays the details of the user in the database associating each withdrawal with the right user.
            withdraw.user = request.user
            withdraw.user_id = request.user.id
            withdraw.first_name = request.user.first_name
            withdraw.last_name = request.user.last_name
            withdraw.username = request.user.username
            withdraw.save()

            user_account = UserAccount
            user_account = UserAccount.objects.get(user=request.user) 
            amount = float(request.POST.get('amount'))
            if amount <= float(user_account.account_balance):
                
                user_account.account_balance = float(user_account.account_balance)
                user_account.account_balance -= amount
                user_account.save()
                messages.success(request, f'Withdrawal of ₦{amount} was successful!')

            elif amount > float(user_account.account_balance):
                messages.error(request, f'Withdrawal cannot be more than your account balance')
                messages.success(request, f'Withdrawal of {amount} was not successful!')
                
        return redirect('dashboard')
    else:
        # Displays a blank form if the user's request is a GET request.
        form = WithdrawalForm()

    return render(request, 'withdraw.html',{"form": form})