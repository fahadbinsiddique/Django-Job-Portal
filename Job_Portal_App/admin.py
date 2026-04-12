from django.contrib import admin
from Job_Portal_App.models import *

# Register your models here.
admin.site.register(
    [
        User_Info_Model,
        Recruiter_Profile_Model,
        Job_Seeker_Profile_Model,
        Job_Post_Model,
        Apply_Job_Model,
    ]
)
