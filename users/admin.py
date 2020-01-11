from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .forms import UserAdminChangeForm, UserAdminCreationForm, StudentAdminForm
from .models import Profile
from .models import UserProxy

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # Hide Student in UserAdmin
    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if not request.user.is_student:
            return qs.filter(student=False)
        return qs

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'active', 'admin', 'staff')
    list_filter = ('admin', 'staff', 'active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('full_name', 'email')}),
        ('Permissions', {'fields': ('admin', 'staff' , 'active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )
    search_fields = ('username', 'email', 'full_name')
    ordering = ('username',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)

# Registering Student
class StudentInlines(admin.StackedInline):
    model = Profile
    fields = [ 'department' , 
                    'year', 'sex', 'degree', 
             ]

class StudentAdmin(admin.ModelAdmin):
    inlines = [StudentInlines]

    # readonly_fields = [("UserProxy__Profile__submission_time")]
    form = StudentAdminForm

    def queryset(self, request):
        qs = super(StudentAdmin, self).queryset(request)
        return qs

    # Hide everyine execept student in StudentAdmin
    def get_queryset(self, request):
        qs = super(StudentAdmin, self).get_queryset(request)
        if not request.user.is_student:
            return qs.filter(student=True)
        return qs

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'active', 'profile_department' , 
                    'profile_year', 'profile_sex', 'profile_degree', 
                    'profile_allow', 'profile_status', 'profile_submission_time', 
                    'profile_user_approved')
    list_filter = ('active',)
    fieldsets = (
        (None, {'fields': ('username', )}),
        ('Personal info', {'fields': ('full_name', 'email', 'student')}),
        
    )
    search_fields = ('username', 'full_name')
    ordering = ('username',)
    filter_horizontal = ()

    def profile_department(self, x):
        return x.profile.department
    profile_department.short_description = 'Department'

    def profile_year(self, x):
        return x.profile.year
    profile_year.short_description = 'Year'

    def profile_sex(self, x):
        if(x.profile.sex == 'M'):
            return 'Male'
        elif(x.profile.sex == 'F'):
            return 'Female'
        else:
            return x.profile.degree
    profile_sex.short_description = 'Sex'

    def profile_degree(self, x):
        if(x.profile.degree == 'B'):
            return 'BTech'
        elif(x.profile.degree == 'M'):
            return 'MTech'
        else:
            return x.profile.degree
    profile_degree.short_description = 'Degree'

    def profile_allow(self, x):
        return x.profile.allow
    profile_allow.boolean = True
    profile_allow.short_description = 'Allow'

    def profile_status(self, x):
        return x.profile.status
    profile_status.boolean = True
    profile_status.short_description = 'Status'

    def profile_submission_time(self, x):
        return x.profile.submission_time
    profile_submission_time.short_description = 'Submission Time'

    def profile_user_approved(self, x):
        return x.profile.user_approved
    profile_user_approved.short_description = 'User Approved'


  
admin.site.register(UserProxy, StudentAdmin)

# Remove Group Model from admin
admin.site.unregister(Group)