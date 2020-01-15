from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from users.models import User
from .models import UserCandidateGet,Candidate,Logs
from poll.models import SiteConfigs
from django.db.models import Sum
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
                    request.session.flush()
                    return redirect("/")

                try:
                    return render(request, 'vote.html', context)
                except:
                    request.session.flush()
                    return redirect("/")                    
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

                    # Condensing table vlues
                    for candidate in Candidate.objects.all():
                        votecount = Logs.objects.filter(candidate_id=candidate).aggregate(Sum('log'))
                        Logs.objects.filter(candidate_id=candidate).delete()       
                        log = Logs.objects.create(candidate_id=candidate,log=votecount['log__sum'])
                        log.save()

                    election_status.value = "False"
                    election_status.save()
                else:
                    for candidate in Candidate.objects.all():
                        log = Logs.objects.create(candidate_id=candidate,log=0)
                        log.save()
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

    if request.user.is_authenticated:
        username = request.user
        try:
            user = User.objects.get(username=username)
            if user.is_student == request.session['student'] == True and (user.is_active and user.profile.allow and not user.profile.status):
                context = { }
                try:
                    context = UserCandidateGet(user)
                    print(context)
                except:
                    request.session.flush()
                    return redirect("/")
                
                if request.method == "POST":
                    for i in context:
                        candidate_list = []
                        for key, value in (context[i]['candidates']).items():
                            candidate_list.append(key)
                        print("Post : ", i , " | Condidates: ", candidate_list)
                        flag = 0
                        try:
                            cand = int(request.POST[str(i)])
                            print (cand)
                            if (cand == -1):
                                pass
                            else:
                                if (cand in candidate_list):
                                    candidate =  Candidate.objects.get(id=cand)
                                    log = Logs.objects.create(candidate_id=candidate,log=1)
                                    log.save()
                                    print("sucesss")
                                else:
                                    request.session.flush()
                                    return redirect("/")
                        except:
                            flag = 1
                            print("error")
                    print(flag)
                    if (flag == 0):
                        user.profile.status = True
                        user.active = False
                        user.save()
                        request.session.flush()
                        return render(request, 'success.html')
                    else:
                        request.session.flush()
                        return redirect("/")      
                else:
                    request.session.flush()
                    return redirect("/")
            else:
                request.session.flush()
                return redirect("/")
        except:
            request.session.flush()
            return redirect("/")
    else:
        request.session.flush()
        return redirect("/")