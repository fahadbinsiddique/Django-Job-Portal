from django.contrib import admin
from Job_Portal_App.models import *

# Register your models here.
admin.site.register(
    [
        UserInfoModel,
        RecruiterProfileModel,
        JobSeekerProfileModel,
        JobPostModel,
        ApplyJobModel,
    ]
)
