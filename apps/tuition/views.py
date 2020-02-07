from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):
    if "userid" in request.session:
        print("in employee")
        user = User.objects.get(id=request.session["userid"])
        context = {
            "first_name": user.first_name,
        }
        return render(request, "tuition/index.html", context)
    elif "employerid" in request.session:
        print("in employer")
        # print(request.session["employerid"])
        employer = Employer.objects.get(id=request.session["employerid"])
        context = {
            "company_name": employer.company_name,
        }
        return render(request, "tuition/index2.html", context)
    else:
        return redirect("/login_page")

def application(request):
    if "userid" in request.session:
        cur_user = User.objects.get(id=request.session["userid"])
        print("in application")
        applications = Application.objects.filter(user=cur_user)
        # print(applications.values())
        for application in applications:
            application.total_cost = application.cost + application.other_fees
            application.save()
        context = {
            "applications": applications,
        }
        return render(request, "tuition/application.html", context)
    return redirect("/logout")

def employee_application(request):
    if "employerid" in request.session:
        cur_employer = Employer.objects.get(id=request.session["employerid"])
        employees = User.objects.filter(employer=cur_employer)
        all_applications = []
        for employee in employees:
            all_applications += Application.objects.filter(user=employee)
        # print(all_applications[0].__dict__)
        context = {
            "all_applications": all_applications,
        }
        return render(request, "tuition/employee_application.html", context)
    return redirect("/logout")


def view_application(request, application_id):
    if "userid" in request.session:
        cur_app = Application.objects.get(id=application_id)
        context = {
            "cur_app": cur_app,
        }
        return render(request, "tuition/view_application.html", context)
    return redirect("/logout")


def review_application(request, application_id):
    if "employerid" in request.session:
        if request.method == "POST":
            cur_app = Application.objects.get(id=application_id)
            if request.POST["choice"] == "Reject":
                cur_app.is_rejected = True
                cur_app.is_pending = False
                cur_app.amount_awarded = 0
            elif  request.POST["choice"] == "Approve":
                cur_app.is_approved = True
                cur_app.is_pending = False
                cur_app.amount_awarded = request.POST["amount_rewarded"]
            elif  request.POST["choice"] == "Require Additional Info":
                cur_app.add_info_required = True
                cur_app.is_pending = True
            cur_app.feedback = request.POST["feedback"]
            cur_app.save()
        else:
            cur_app = Application.objects.get(id=application_id)
            context = {
                "cur_app": cur_app,
            }
            return render(request, "tuition/review_application.html", context)
        return redirect("/employee_application")
    return redirect("/logout")

def account(request):
    cur_user = User.objects.get(id=request.session["userid"])
    cur_user.birthday = cur_user.birthday.strftime('%Y-%m-%d')
    employer = cur_user.employer.__dict__
    context = {
        "cur_user": cur_user,
    }
    return render(request, "tuition/account.html", context)

def edit_account(request):
    if request.method == "POST":
        cur_user = User.objects.get(id=request.session["userid"])
        cur_user.email = request.POST["email"]
        cur_user.password = request.POST["password"]
        cur_user.birth_day = request.POST["birth_day"]
        cur_user.address = request.POST["address"]
        cur_user.save()
        return redirect("/account")
    return redirect("/account")

def employer_account(request):
    cur_employer = Employer.objects.get(id=request.session["employerid"])
    # print(cur_employer.__dict__)
    # print(cur_employer.employees.values())
    print("in employer acc")
    context = {
        "cur_employer": cur_employer,
        "employees": cur_employer.employees.all().values()
    }
    print(context["employees"])
    return render(request, "tuition/employer_account.html", context)

def edit_employer_account(request):
    if request.method == "POST":
        cur_employer = Employer.objects.get(id=request.session["employerid"])
        cur_employer.email = request.POST["email"]
        cur_employer.address = request.POST["address"]
        cur_employer.save()
        return redirect("/employer_account")
    return redirect("/employer_account")

def new_application(request):
    if request.method == "POST":
        errors = Application.objects.basic_validator(request.POST)
        # see if the email provided exists in the database
        if len(errors) > 0:
                # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                    # Adding errors into messages
                messages.error(request, value, extra_tags=key)
            # redirect the user back to the form to fix the errors
            print(errors)
            return redirect("/application")
        else:
            if len(request.FILES) != 0:
                file=request.FILES["application_file"]
            else:
                file = None
            cur_user = User.objects.get(id=request.session["userid"])
            Application.objects.create(institution=request.POST["institution"], start_date=request.POST["start_date"], end_date=request.POST["end_date"], course_name=request.POST["course_name"], add_info=request.POST["add_info"], other_fees=request.POST["other_fees"], cost=request.POST["cost"], application_file=file, user=cur_user)
            return redirect("/application")
    else:
        return redirect("/application")

def delete_application(request, application_id):
    dele = Application.objects.get(id=application_id)
    dele.delete()
    return redirect("/application")

def edit_application(request, application_id):
    if request.method == "POST":
        cur_app = Application.objects.get(id=application_id)
        cur_app.institution=request.POST["institution"]
        cur_app.start_date=request.POST["start_date"]
        cur_app.end_date=request.POST["end_date"]
        cur_app.course_name=request.POST["course_name"]
        cur_app.add_info=request.POST["add_info"]
        cur_app.cost=request.POST["cost"]
        cur_app.other_fees=request.POST["other_fees"]
        cur_app.file=request.POST["file"]
        cur_app.save()
        return redirect("/application")
    else:
        cur_app = Application.objects.get(id=application_id)
        cur_app.start_date = cur_app.start_date.strftime('%Y-%m-%d')
        cur_app.end_date = cur_app.end_date.strftime('%Y-%m-%d')
        context = {
            "application_id": application_id,
            "cur_app": cur_app
        }
        return render(request, "tuition/edit.html", context)

def revise_application(request, application_id):
    if "userid" in request.session:
        if request.method == "POST":
            cur_app = Application.objects.get(id=application_id)
            cur_app.add_info = request.POST["add_info"]
            cur_app.application_file = request.FILES["application_file"]
            cur_app.save()
        else:
            cur_app = Application.objects.get(id=application_id)
            context = {
                "cur_app": cur_app,
            }
            return render(request, "tuition/revise_application.html", context)
        return redirect("/application")
    return redirect("/logout")

def contact(request):
    return render(request, "tuition/contact_us.html")

def submit_request(request):
    return render(request, "tuition/submit_request.html")