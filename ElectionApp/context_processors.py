from poll.models import SiteConfigs

def election_status(request):
    election_status = SiteConfigs.objects.get(key="status").value
    return {
        'election_status': election_status
    }