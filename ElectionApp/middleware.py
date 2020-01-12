from django.http import HttpResponseForbidden 
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse, Http404
from poll.models import SiteConfigs

class CheckUserSiteMiddleware(MiddlewareMixin):

    def process_request(self, request):
        election_status = SiteConfigs.objects.get(key="status").value

        if (election_status == "False" and not
            request.path.startswith('/admin/')):
            raise Http404

        if (request.path.startswith('/admin/') and
                request.user.is_authenticated and not
                request.user.is_admin):
            raise Http404

        if (request.path.startswith('/vote/') and
                request.user.is_authenticated and not
                request.user.is_student):
            raise Http404

        if (request.path.startswith('/authoriser/') and
                request.user.is_authenticated and not
                request.user.is_staff):
            raise Http404

