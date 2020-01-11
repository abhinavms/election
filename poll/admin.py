from django.contrib import admin

# from .models import Student
from .models import Candidate
from .models import Position

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ['position', 'department', 'year', 'sex', 'degree']

class CandidateAdmin(admin.ModelAdmin):
    model = Candidate
    list_display = ['admission_no', 'name', 'get_post']

    def get_post(self, obj):
        return obj.post
    get_post.admin_order_field  = 'Post'
    get_post.short_description = 'Position'

    list_filter = ['post__position']

admin.site.register(Candidate, CandidateAdmin)
