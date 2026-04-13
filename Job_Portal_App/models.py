from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfoModel(AbstractUser):
    USER_TYPES = [
        ("Seeker", "Seeker"),
        ("Recruiter", "Recruiter"),
    ]
    display_name = models.CharField(
        max_length=255,
        null=True,
    )
    user_types = models.CharField(
        choices=USER_TYPES,
        max_length=25,
        null=True,
    )

    def __str__(self):
        return f"{self.username} - {self.user_types}"


class RecruiterProfileModel(models.Model):
    recruiter = models.OneToOneField(
        UserInfoModel,
        on_delete=models.CASCADE,
        related_name="recruiter_profile",
        null=True,
    )
    company_name = models.CharField(
        max_length=225,
        null=True,
    )
    email = models.EmailField(
        null=True,
    )
    address = models.TextField(
        null=True,
    )
    phone = models.CharField(
        max_length=20,
        null=True,
    )
    logo = models.ImageField(
        upload_to="recruiter_logos/",
        null=True,
    )

    def __str__(self):
        return f"{self.company_name} - {self.recruiter.username}"


class JobSeekerProfileModel(models.Model):
    seeker = models.OneToOneField(
        UserInfoModel,
        on_delete=models.CASCADE,
        related_name="seeker_profile",
        null=True,
    )
    profile_picture = models.ImageField(
        upload_to="seeker_photos/",
        null=True,
    )
    address = models.TextField(
        null=True,
    )
    phone = models.CharField(
        max_length=20,
        null=True,
    )

    def __str__(self):
        return f"{self.seeker.username}"


class JobPostModel(models.Model):
    CATEGORY_CHOICES = [
        ("Developer", "Developer"),
        ("Banking", "Banking"),
        ("HR", "HR"),
        ("Education", "Education"),
    ]
    title = models.CharField(max_length=255, null=True)
    vacancy = models.PositiveIntegerField(null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20, null=True)
    job_description = models.TextField(null=True)
    skills_set = models.TextField(null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    deadline = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    posted_by = models.ForeignKey(
        RecruiterProfileModel,
        on_delete=models.CASCADE,
        related_name="job_posts",
        null=True,
    )

    def __str__(self):
        return f"{self.title}  -  { self.posted_by }"


class ApplyJobModel(models.Model):
    applied_by = models.ForeignKey(
        JobSeekerProfileModel,
        on_delete=models.CASCADE,
        related_name="my_applications",
        null=True,
    )
    applied_job = models.ForeignKey(
        JobPostModel,
        on_delete=models.CASCADE,
        related_name="applicants",
        null=True,
    )
    resume = models.FileField(upload_to="resumes/", null=True)
    applied_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.applied_by.seeker.display_name} applied for {self.applied_job.title}"
