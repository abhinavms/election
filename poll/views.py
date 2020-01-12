from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from users.models import User
from .models import UserCandidateGet,Candidate,Logs
from poll.models import SiteConfigs
import json

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




def update_vote(request):

    if request.POST:
        intermediate_dict = {}
        for field in request.POST:
            if field != 'csrfmiddlewaretoken':
                intermediate_dict[field] = request.POST.get(field)
        
        user = User.objects.get(username=request.user)
        if user.is_student == request.session['student'] == True and (user.is_active and  user.profile.allow and not user.profile.status):
           context = UserCandidateGet(user)
           if len(context) == len(intermediate_dict):

               for field in intermediate_dict:
                   candidate =  Candidate.objects.get(pk = intermediate_dict[field])
                   log = Logs.objects.create(candidate_id=candidate,log=1)
                   log.save()
               response = {'status':1}
               request.session.flush()

           else:

               response = {'status':0}




    
        return HttpResponse(json.dumps(response),content_type='application/json')
    

    

