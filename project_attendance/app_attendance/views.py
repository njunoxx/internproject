from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CustomUser, Attendance
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, date
from django.contrib.auth.decorators import login_required


# Create your views here.

# Index page
@login_required(login_url='login')
def index(request):
    user = request.user
    context = {"data":user}
    return render(request, 'display/index.html', context)

# To create Normal User
@login_required(login_url='login')
def create_normal_user(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Get the form data from the request POST data
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        gender = request.POST.get('gender')

        # Create a new normal user using UserManager's create_user method
        CustomUser.objects.create_user(
            username=username,
            password=password,
            email=email,
            address=address,
            contact=contact,
            gender=gender
        )

        # Return a success response
        messages.success(request, 'Normal user created successfully!')
        return redirect('index')
    else:
        # Render the form template
        return render(request, 'authentication/registerform.html')
    
# To create Super User
def create_admin_user(request):
    # Check if the request method is POST
    if not request.user.is_superuser:
        messages.warning(request,"Forbidden Request")
        return redirect('index')
    else:
        if request.method == 'POST':
            # Get the form data from the request POST data
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            address = request.POST.get('address')
            contact = request.POST.get('contact')
            gender = request.POST.get('gender')

            # Create a new admin user using UserManager's create_superuser method
            CustomUser.objects.create_superuser(
                username=username,
                password=password,
                email=email,
                address=address,
                contact=contact,
                gender=gender
            )

            # Return a success response
            return HttpResponse('Admin user created successfully!')
        else:
            # Render the form template
            return render(request, 'authentication/adminregisterform.html')
    

# Login for both Normal and Super User
def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Logged In Successfully!")
                return redirect('index')
            else:
                messages.error(request, "Invalid Username or Password!!!")
                return redirect('login')
    return render(request, 'authentication/loginform.html')

# Logout for all Users
@login_required(login_url='login')
def user_logout(request):
    user=request
    logout(user)
    messages.success(request, "Logged Out")
    return redirect('login')

# To Add Attendance of the Users
@login_required(login_url='login')
def add_attendance(request):
    attendance = CustomUser.objects.filter(username=request.user)
    context = {"data" : attendance}
    if request.method == 'POST':
        username = request.POST.get('username') 
        attendance_date = request.POST.get('date')
        time_in1 = request.POST.get('start_in')
        time_out1 = request.POST.get('start_out')
        time_in2 = datetime.strptime(time_in1, '%H:%M')
        time_out2 = datetime.strptime(time_out1, '%H:%M')
        try:
            # Checking if User Enters Present dates Only
            if attendance_date < str(date.today()) and attendance_date > str(date.today()):
                messages.error(request, "Error!!! You have entered PAST or FUTURE date!")
                return redirect('attendance-add')
            
            # Checking the entered time from user is in between 09:00 to 17:00
            elif time_in1 < "09:00" or time_in1 > "09:00" and time_out1 < "17:00" or time_out1 > "17:00":
                messages.warning(request, "Warning!! You have entered invalid check in and check out time!")
                return redirect('attendance-add')
            else:
                user = CustomUser.objects.get(id=request.POST.get('username'))
                att = Attendance()
                att.username = user
                att.date = attendance_date
                time_in = time_in2
                time_out = time_out2
                hours_worked = time_out - time_in
                att.hours_worked = hours_worked
                att.time_in = time_in2
                att.time_out = time_out2
                att.status = True if request.POST.get('status')=="status" else False
                # Checking if the specific user has performed their attendance for specific date
                status = Attendance.objects.filter(status=True,
                                                        username=request.POST.get('username'),
                                                        date=request.POST.get('date'))
                if status.exists():
                    messages.error(request, "You have already recorded your attendance today!!")
                    return redirect('attendance-add')
                else:
                    att.save()
                    messages.success(request, "Success!!! Attendance added successfully.")
                    return redirect('index')
        except:
            messages.error(request, "Something went wrong!")
            return redirect('attendance-add')    
    return render(request, 'display/attendance.html', context)


# To View the Attendance Information of the users
@login_required(login_url='login')
def attendance_view(request):
    if not request.user.is_superuser:
        att = Attendance.objects.filter(username=request.user)
        context = {"data" : att}
        return render(request, 'display/attendanceview.html', context)
    else:
        att = Attendance.objects.all()
        context = {"data" : att}
        return render(request, 'display/attendanceview.html', context)
    

# To Edit Attendance    
@login_required(login_url='login')    
def edit_attendance(request,id):
    att = Attendance.objects.get(id=id)
    context = {"data":att}
    if not request.user.is_superuser:
        messages.warning(request, "Forbiddend Access!")
        return redirect('attendance-view')
    else:
        if request.method == 'POST':
            att.date = request.POST.get('date')
            time_in1 = request.POST.get('time_in')
            time_out1 = request.POST.get('time_out')
            time_in = datetime.strptime(time_in1, '%H:%M')
            time_out = datetime.strptime(time_out1, '%H:%M')
            hours_worked = time_out - time_in
            att.time_in = time_in1
            att.time_out = time_out1
            att.hours_worked = hours_worked
            att.save()
            messages.success(request, "Attendance data has been Edited successfully")
            return redirect('attendance-view')
    return render(request, 'display/attendanceedit.html', context)

# To delete attendance of the users
@login_required(login_url='login')
def delete_attendance(request, id):
    att = Attendance.objects.get(id=id)
    if not request.user.is_superuser:
        messages.warning(request, 'Forbidden Access!!')
        return redirect('attendance-view')
    else:
        att.delete()
        messages.success(request, "Deleted SuccessFully!")
        return redirect('attendance-view')

# To view User Profile
@login_required(login_url='login')    
def user_profile(request):
    user = CustomUser.objects.all()
    if not request.user.is_superuser:
        messages.warning(request, "Forbidden Access!")
        return redirect('index')
    else:
        context = {"data" : user}
        return render(request, 'display/profile.html', context)
    
# To Edit the User Profile Information
@login_required(login_url='login')    
def user_edit(request, id):
    if not request.user.is_superuser:
        messages.warning(request, "Forbidden Access")
        return redirect('index')
    else:
        user = CustomUser.objects.get(id=id)
        context = {"data":user}
        if request.method == 'POST':
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.contact = request.POST.get('contact')
            user.address = request.POST.get('address')
            user.gender = request.POST.get('gender')
            user.save()
            messages.success(request, "User Profile Edited Successfully")
            return redirect('user-profile')
        return render(request, 'display/useredit.html', context)
    

# To delete User 
login_required(login_url='login')
def user_delete(request, id):
    if not request.user.is_superuser:
        messages.warning(request, "Forbidden access!")
        return redirect('index')
    else:
        user = CustomUser.objects.get(id=id)
        user.delete()
        messages.success(request, "User deleted successfully")
        return redirect('user-profile')

        