from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User_Info_Model(AbstractUser):
    USER_TYPES = [
        ("Seeker", "Seeker"),
        ("Recruiter", "Recruiter"),
    ]
    Display_Name = models.CharField(max_length=255, null=True)
    User_Types = models.CharField(choices=USER_TYPES, max_length=25, null=True)

    def __str__(self):
        return f"{self.username} - {self.User_Types}"


class Recruiter_Profile_Model(models.Model):
    Recruiter = models.OneToOneField(
        User_Info_Model,
        on_delete=models.CASCADE,
        related_name="Recruiter_Profile",
        null=True,
    )
    Company_Name = models.CharField(
        max_length=225,
        null=True,
    )
    Email = models.EmailField(
        null=True,
    )
    Address = models.TextField(null=True)
    Phone = models.CharField(max_length=20, null=True)
    Logo = models.ImageField(upload_to="media/", null=True)


class Job_Seeker_Profile_Model(models.Model):
    Seeker = models.OneToOneField(
        User_Info_Model,
        on_delete=models.CASCADE,
        related_name="Seeker_Profile",
        null=True,
    )
    Profile_Picture = models.ImageField(upload_to="media/", null=True)
    Address = models.TextField(null=True)
    Phone = models.CharField(max_length=20, null=True)


class Job_Post_Model(models.Model):
    CATEGORY = [
        ("Developer", "Developer"),
        ("Banking", "Banking"),
        ("HR", "HR"),
        ("Education", "Education"),
    ]
    Title = models.CharField(max_length=255, null=True)
    Vacancy = models.PositiveIntegerField(null=True)
    Category = models.CharField(choices=CATEGORY, max_length=20, null=True)
    Job_Description = models.TextField(null=True)
    Skills_Set = models.TextField(null=True)
    Salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    Deadline = models.DateField(null=True)
    Create_At = models.DateField(auto_now_add=True, null=True)
    Posted_By = models.ForeignKey(
        Recruiter_Profile_Model, on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return f"{self.Title} - {self.Posted_By.Company_Name}"


class Apply_Job_Model(models.Model):
    Applied_By = models.ForeignKey(
        Job_Seeker_Profile_Model, on_delete=models.CASCADE, null=True
    )
    Applied_Job = models.ForeignKey(
        Job_Post_Model,
        on_delete=models.CASCADE,
        null=True,
        related_name="Seeker_Applied_Job",
    )
    Resume = models.FileField(upload_to="media/", null=True)
    Applied_At = models.DateField(null=True, auto_now_add=True)

    def __str__(self):
        return f"{self.Applied_By.Seeker.Display_Name}"
