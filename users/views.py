from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from .models import User

from .forms import LoginForm

def login_page(request):
    if request.user.is_authenticated:
        username = request.user
        try:
            user = User.objects.get(username=username)
            if user.is_student == request.session['student'] == True:
                return redirect("vote")
            elif user.is_staff == request.session['staff'] == True:
                return redirect("authoriser")
            else:
                request.session.flush()
                return redirect("/")
        except:
            request.session.flush()
            return redirect("/")

    else:
        form = LoginForm(request.POST or None)
        context = {
            "form": form
        }
        student_path = 'vote'
        staff_path = 'authoriser'

        if form.is_valid():
            username  = form.cleaned_data.get("username")
            password  = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_student:
                    if is_safe_url(student_path, request.get_host()):
                        request.session['student'] = True
                        request.session['staff'] = False
                        return redirect(student_path)
                    else:
                        return redirect("/")
                elif user.is_staff:
                    if is_safe_url(staff_path, request.get_host()):
                        request.session['student'] = False
                        request.session['staff'] = True
                        return redirect(staff_path)
                    else:
                        return redirect("/")
            else:
                # Return an 'invalid login' error message.
                print("Error")
        return render(request, "index.html", context)