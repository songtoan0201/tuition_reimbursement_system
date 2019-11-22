from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
# Create your views here.


def login_page(request):
    return render(request, "login/login.html")

def register_page(request):
    context = {
        "employers": Employer.objects.all().values()
    }
    return render(request, "login/register.html", context)

def employer_registration(request):
    return render(request, "login/employer_register.html")

def employer_register(request):
    if request.method == "POST":

        errors = Employer.objects.basic_validator(request.POST)
        # see if the email provided exists in the database
        all_employers = Employer.objects.all()
        for employer in all_employers:
            if employer.email == request.POST["email"]:
                errors["unique"] = "Email already existed in the database"
        if len(errors) > 0:
                # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                    # Adding errors into messages
                messages.error(request, value, extra_tags=key)
            # redirect the user back to the form to fix the errors
            print(errors)
            return redirect("/employer_registration")
        else:
            print(request.POST)
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            print(pw_hash)
            logged_employer = Employer.objects.create(company_name=request.POST["company_name"], email=request.POST["email"], password=pw_hash, address = request.POST["address"] + ", " + request.POST["country"] + ", " + request.POST["state"] + ", " + request.POST["zip"])
            request.session['employerid'] = logged_employer.id
            request.session['company_name'] = logged_employer.company_name
            return redirect("/success")
    else:
        return redirect("/employer_registration")

def register(request):
    # include some logic to validate user input before adding them to the database!
    if request.method == "POST":

        errors = User.objects.basic_validator(request.POST)
        # see if the email provided exists in the database
        all_users = User.objects.all()
        for user in all_users:
            if user.email == request.POST["email"]:
                errors["unique"] = "Email already existed in the database"
        if len(errors) > 0:
                # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                    # Adding errors into messages
                messages.error(request, value, extra_tags=key)
            # redirect the user back to the form to fix the errors
            print(errors)
            return redirect("/register_page")
        else:
            print(request.POST)
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            print(pw_hash)
            employ = Employer.objects.get(company_name = request.POST["company_name"])
            logged_user = User.objects.create(first_name=request.POST["first_name"], last_name=request.POST["last_name"],
                                              email=request.POST["email"], password=pw_hash, birthday=request.POST["birthday"], phone_no=request.POST["phone_no"], address = request.POST["address"] + ", " + request.POST["country"] + ", " + request.POST["state"] + ", " + request.POST["zip"], employer= employ)
            request.session['userid'] = logged_user.id
            request.session['first_name'] = logged_user.first_name
            return redirect("/success")
    else:
        return redirect("/register_page")


def login(request):
    # see if the email provided exists in the database
    if request.method == "POST":
        # why are we using filter here instead of get?
        employer_exist = Employer.objects.filter(email=request.POST['email'])
        employee_exist = User.objects.filter(email=request.POST['email'])
        if employer_exist :  # note that we take advantage of truthiness here: an empty list will return false
            logged_user = employer_exist[0]
            # assuming we only have one user with this username, the user would be first in the list we get back
            # of course, we should have some logic to prevent duplicates of usernames when we create users
            # use bcrypt's check_password_hash method, passing the hash from our database and the password from the form
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                # if we get True after checking the password, we may put the user id in session
                request.session['employerid'] = logged_user.id
                request.session['company_name'] = logged_user.company_name
                # never render on a post, always redirect!
                return redirect('/success')
            else:
                messages.error(request, "Password is incorrect",
                               extra_tags="wrong_password")
                return redirect("/login_page")
        # if we didn't find anything in the database by searching by username or if the passwords don't match,
        # redirect back to a safe route
        elif employee_exist :  
            logged_user = employee_exist[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
                request.session['first_name'] = logged_user.first_name
                # never render on a post, always redirect!
                return redirect('/success')
            else:
                messages.error(request, "Password is incorrect",
                               extra_tags="wrong_password")
                return redirect("/login_page")
        else:
            messages.error(request, "Email doesn't exist",
                           extra_tags="wrong_email")
            return redirect("/login_page")
    else:
        return redirect("/login_page")


def success(request):
    if "userid" in request.session:
        user = User.objects.get(id=request.session["userid"])
        context = {
            "first_name": user.first_name,
        }
        return render(request, "tuition/index.html", context)
    elif "employerid" in request.session:
        employer = Employer.objects.get(id=request.session["employerid"])
        context = {
            "company_name": employer.company_name,
        }
        return render(request, "tuition/index2.html", context)
    else:
        return redirect("/login_page")


def logout(request):
    request.session.flush()
    request.session.modified = True
    # delete keys without logging out the user
    # for key in list(request.session.keys()):
    #   if not key.startswith("_"): # skip keys set by the django system
    # del request.session[key]
    return redirect("/login_page")
