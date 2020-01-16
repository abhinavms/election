from django.shortcuts import render
from users.models import User
from poll.models import AllCandidateGet, AllPostsGet

def viewresults(request):
    context = {}
    user = User.objects.get(username=170163)
    context['candidates'] = AllCandidateGet()
    context['posts'] = AllPostsGet()
    return render(request, 'results.html', context)