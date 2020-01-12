from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from users.views import login_page
from poll.views import vote, switch_election_status,update_vote
from authoriser.views import authoriser

urlpatterns = [
    path(r'', login_page, name='login'),
    path(r'vote/', vote, name='vote'),
    path(r'vote/validate',update_vote,name='update_vote'),
    path(r'authoriser/', authoriser, name='authoriser'),
    path('admin/', admin.site.urls),
    path('admin/statuschange', switch_election_status),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Election Administration'
admin.site.site_title = 'SCTCE Election 2020'