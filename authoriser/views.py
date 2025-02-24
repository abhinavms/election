from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from users.models import User, Profile
from django.utils.crypto import get_random_string
from .form import AuthForm
from django.contrib.auth import logout

def authoriser(request):
    if request.user.is_authenticated:
        username = request.user
        try:
            user = User.objects.get(username=username)
            if user.is_staff == request.session['staff'] == True:
                form = AuthForm(request.POST or None)
                context = {
                    "form": form,
                    "show_password" : False
                }
                if form.is_valid():
                    student_no  = form.cleaned_data.get("student_no")
                    try:
                        student = User.objects.get(username=student_no)
                        student_profile = Profile.objects.get(user = student)
                    except:
                        return render(request, 'authoriser.html', context)
                    
                    if(student.is_student and student.is_active and not student.profile.status):
                        password = get_random_string(length=4, allowed_chars='ABCDEFGHIJKLMNPQRSTUVWXYZ123456789')
                        context['show_password'] = True
                        context['password'] = password
                        student.set_password(password)
                        student_profile.allow = True
                        student_profile.user_approved = user.full_name
                        print ("Here")
                        student_profile.save()
                        student.save()
                        return render(request, 'authoriser.html', context)
                    return render(request, 'authoriser.html', context)
                else:
                    pass
                return render(request, 'authoriser.html', context)
            else:
                logout(request)
                return redirect("/")
        except:
            request.session.flush()
            return redirect("/")
    else:
        request.session.flush()
        return redirect("/")