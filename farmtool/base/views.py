from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone 
from django.http import HttpResponse
from .forms import LoginForm
from .forms import SignupForm
from .models import FarmTool,ToolTransaction,MaintenanceSchedule



def home(request):
    return render (request, 'homepage.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                
                return redirect('home')  # Redirect to homepage after login
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'user_login.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            login(request, user)  # Automatically log in the user after signup
            return redirect('profile')  # Redirect to the profile page
    else:
        form = SignupForm()
    return render(request, 'signup.html',{'form': form})

def homepage1(request):
    
    return render(request, 'homepage1.html')

def tool_list(request):
    tools = FarmTool.objects.all()
    return render(request, 'tool_list.html', {'tools': tools})

@login_required
def profile_page(request):
    return render(request, 'profile.html')

def error(request):
    return render(request,'error.html')

    
def add_tool(request):
     if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        FarmTool.objects.create(name=name, description=description, available=True)
        return redirect('tool_list')
     return render(request,'add_tool.html')


def tool_detail(request, tool_id):
    tool = get_object_or_404(FarmTool, id=tool_id)
    return render(request, 'tool_details.html', {'tool': tool})


def check_out_tool(request, tool_id):
    tool = get_object_or_404(FarmTool, id=tool_id)
    
    if tool.available:  # Only allow checkout if tool is available
        transaction = ToolTransaction.objects.create(
            user=request.user,
            tool=tool,
            check_out_date=timezone.now(),
            status='Checked Out'
        )
        tool.available = False  # Mark tool as unavailable
        tool.save()
        return redirect('tool_list')  # Redirect to tool list after checkout
    else:
        return render(request, 'error.html', {'message': 'Tool is currently not available'})


def check_in_tool(request, transaction_id):
    transaction = get_object_or_404(ToolTransaction, id=transaction_id, user=request.user)

    if transaction.status == 'Checked Out':  # Ensure it's checked out before checking in
        transaction.check_in_date = timezone.now()
        transaction.status = 'Checked In'
        transaction.save()

        # Mark tool as available again
        transaction.tool.available = True
        transaction.tool.save()

        return redirect('tool_list')  # Redirect to tool list after check-in
    else:
        return render(request, 'error.html', {'message': 'Tool is already checked in'})
    

def maintenance_list(request):
    schedules = MaintenanceSchedule.objects.all().order_by('scheduled_date')
    return render(request, 'maintenance_list.html', {'schedules': schedules})

@login_required
def maintain(request, tool_id):
    tool = get_object_or_404(FarmTool, id=tool_id)
    
    if request.method == 'POST':
        scheduled_date = request.POST['scheduled_date']
        notes = request.POST.get('notes', '')
        MaintenanceSchedule.objects.create(tool=tool, scheduled_date=scheduled_date, notes=notes)
        return redirect('maintenance_list')
    
    return render(request, 'maintain.html', {'tool': tool})


def mark_completed(request, maintenance_id):
    maintenance = get_object_or_404(MaintenanceSchedule, id=maintenance_id)
    maintenance.status = 'Completed'
    maintenance.save()
    return redirect('maintenance_list')

def reminders(request):
    today = timezone.now().date()
    upcoming = MaintenanceSchedule.objects.filter(scheduled_date__gte=today).order_by('scheduled_date')
    return render(request, 'reminders.html', {'upcoming': upcoming})
    


   


    




