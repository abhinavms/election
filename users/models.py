from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)
from django.utils.crypto import get_random_string

class UserManager(BaseUserManager):
    def create_user(self, username, password = None, email = None, full_name = None, is_active = True, is_student = False, is_staff = False, is_admin = False):
        if not username:
            raise ValueError("Users must have an username")
        
        if not password:
            if is_student:
                password = get_random_string(length = 32)
            else:
                raise ValueError("Users must have a password")

        user_obj = self.model(
            username = username
        )
        user_obj.set_password(password)
        user_obj.email = email
        user_obj.full_name = full_name
        user_obj.active = is_active
        user_obj.student = is_student
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_studentuser(self, username, password = None, full_name = None):
        user = self.create_user(
            username,
            password = password, 
            full_name = full_name,
            is_student = True 
        )
        return user
    
    def create_staffuser(self, username, password = None, email = None, full_name = None):
        user = self.create_user(
            username,
            password = password,
            full_name = full_name, 
            is_staff = True
        )
        return user        

    def create_superuser(self, username, password = None, email = None, full_name = None):
        user = self.create_user(
            username,
            password = password, 
            full_name = full_name,
            is_admin = True,
            is_staff = True
        )
        return user        
        
class User(AbstractBaseUser):

    username    = models.CharField(max_length = 255, unique = True)
    email       = models.EmailField(max_length = 255, unique = True, blank = True, null = True)
    full_name   = models.CharField(max_length = 255, blank = True, null = True)
    active      = models.BooleanField(default = True) # Can Login
    student     = models.BooleanField(default = False) # Student User | Non Superuser
    staff       = models.BooleanField(default = False) # Staff User   | Non Superuser
    admin       = models.BooleanField(default = False) # Superuser
    timestamp   = models.DateField(auto_now_add = True)

    USERNAME_FIELD = 'username' # Username
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.username

    def get_short_name(self):
        if self.full_name:
            return self.full_name
        return self.username
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

    def get_email(self):
        return self.email
    
    def set_student(self):
        self.student = True

    @property
    def is_student(self):
        return self.student

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin

class Profile(models.Model):
    SEX_CHOICES     = [('M', 'Male'), ('F', 'Female')]
    YEAR_CHOICES    = [(1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year')]
    DEPT_CHOICES    = [('R', 'Computer Science'), ('T', 'Electronics And Communication'), ('M', 'Mechanical'), ('A', 'Mechanical Automobile'), ('P', 'Mechanical Production'), ('B', 'Bio Technology')]
    DEG_CHOICES     = [('B', 'BTech'), ('M', 'MTech')]

    user            = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    department      = models.CharField(choices=DEPT_CHOICES, max_length=50)
    year            = models.IntegerField(choices=YEAR_CHOICES)
    sex             = models.CharField(choices = SEX_CHOICES, max_length=10)
    degree          = models.CharField(choices = DEG_CHOICES, max_length=25)
    allow           = models.BooleanField(default=False)
    status          = models.BooleanField(default=False)
    submission_time = models.DateTimeField(null=True, blank=True)
    user_approved   = models.CharField(max_length=100, blank=True)

class UserProxy(User):
    class Meta:
        proxy = True
        verbose_name = 'Student'