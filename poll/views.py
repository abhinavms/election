from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from users.models import User
from .models import UserCandidateGet
from poll.models import SiteConfigs


def vote(request):
    if request.user.is_authenticated:
        username = request.user
        try:
            user = User.objects.get(username=username)
            if user.is_student == request.session['student'] == True and (user.is_active and user.profile.allow and not user.profile.status):
                context = { }
                try:
                    context["data"] = UserCandidateGet(user)
                except:
                    pass
                print(context)
                try:
                    return render(request, 'vote.html', context)
                except:
                    print('error')
                    return render(request, 'vote_copy.html')                    
            else:
                request.session.flush()
                return redirect("/")
        except:
            request.session.flush()
            return redirect("/")

    else:
        return redirect("/")
    
def switch_election_status(request):
    if request.user.is_authenticated:
        username = request.user
        try:
            user = User.objects.get(username=username)
            if user.is_admin == True and user.is_active:
                election_status = SiteConfigs.objects.get(key="status")
                if (election_status.value == "True"):
                    election_status.value = "False"
                    election_status.save()
                else:
                    election_status.value = "True"
                    election_status.save()
            else:
                request.session.flush()
                return redirect("/")
        except:
            request.session.flush()
            return redirect("/")
    else:
        request.session.flush()
        return redirect("/")
    return HttpResponseRedirect('/admin')