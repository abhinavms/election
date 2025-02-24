from django.db import models

class Position(models.Model):
    SEX_CHOICES     = [('All', 'All'), ('M', 'Male'), ('F', 'Female')]
    YEAR_CHOICES    = [(0, 'All'), (1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year')]
    DEPT_CHOICES    = [('All', 'All'), ('R', 'Computer Science'), ('T', 'Electronics And Communication'), ('M', 'Mechanical'), ('A', 'Mechanical Automobile'), ('P', 'Mechanical Production'), ('B', 'Bio Technology')]
    DEG_CHOICES     = [('All', 'All'), ('B', 'B-Tech'), ('M', 'M-Tech')]

    position    = models.CharField(max_length = 100)
    department  = models.CharField(choices=DEPT_CHOICES, default = 'All', max_length = 5)
    year        = models.IntegerField(choices = YEAR_CHOICES, default = 0)
    sex         = models.CharField(choices = SEX_CHOICES, default = 'All' ,max_length = 5)
    degree      = models.CharField(choices = DEG_CHOICES, default = 'All' , max_length = 5)

    def __str__(self):
        return str(self.position)


class Candidate(models.Model):
    admission_no = models.IntegerField()
    image        = models.ImageField(upload_to = 'Candidates', blank = True)
    name         = models.CharField(max_length = 100)
    post         = models.ForeignKey(Position, on_delete = models.CASCADE)

    def __str__(self):
        return str(self.post)

class Vote(models.Model):
    candidate_id = models.OneToOneField(Candidate, on_delete = models.CASCADE)
    vote         = models.IntegerField(default = 0)

def UserCandidateGet(User):
    context = {}
    position_list = Position.objects.all()
    candidate_list = Candidate.objects.all()
    for post in position_list:
        applicable_posts = {}
        applicable_candidates = {}
        flag = True      
        if (post.department != "All" and post.department != User.profile.department):
            flag = False
        if (post.year != 0 and post.year != User.profile.year):
            flag = False
        if (post.sex != 'All' and post.sex != User.profile.sex):
            flag = False
        if (post.degree != 'All' and post.degree != User.profile.degree):
            flag = False
        if (flag):
            applicable_posts["title"] = post.position
            for candidates in candidate_list:
                if (candidates.post_id == post.id):
                    applicable_candidates[candidates.id] = candidates.name
            applicable_posts["candidates"] = applicable_candidates
            context[post.id] = applicable_posts
    return context
    
def AllCandidateGet():
    context = {}
    
    candidate_list = Candidate.objects.all()

    for candidates in candidate_list:
        cand = {}
        cand['admission_no'] = candidates.admission_no
        cand['name'] = candidates.name
        cand['position'] = str(candidates.post)
        cand['vote'] = Logs.objects.get(candidate_id=candidates.id).log
        context[candidates.id] = cand
    return context

def AllPostsGet():
    context = {}
    position_list = Position.objects.all()
    candidate_list = Candidate.objects.all()
    for post in position_list:
        applicable_posts = {}
        for candidates in candidate_list:
            applicable_candidates = {}
            if (candidates.post_id == post.id):
                applicable_candidates['admission_no'] = candidates.admission_no
                applicable_candidates['name'] = candidates.name
                applicable_candidates['vote'] = Logs.objects.get(candidate_id=candidates.id).log
                applicable_posts[candidates.id] = applicable_candidates
        context[post.position] = applicable_posts
    return context

class SiteConfigs(models.Model):
    key = models.CharField(primary_key=True, max_length = 100)
    value = models.CharField(max_length = 100)

    def __str__(self):
        return str(self.key)

# insert into "public"."poll_siteconfigs" ("key","value") values ('status', 'True');



class Logs(models.Model):
    candidate_id = models.ForeignKey(Candidate,on_delete=models.CASCADE)
    log = models.IntegerField(default=1)

    