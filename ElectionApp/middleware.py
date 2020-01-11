from django.http import HttpResponseForbidden 
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse, Http404

class CheckUserSiteMiddleware(MiddlewareMixin):

    def process_request(self, request):
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
        
    