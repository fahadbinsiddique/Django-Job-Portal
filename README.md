# 💼 Job Portal — Django Web Application

A full-featured **Job Portal Web Application** built with Django, supporting two distinct user roles: **Recruiters** and **Job Seekers**. Recruiters can post and manage job listings, while seekers can browse, search, filter, and apply for jobs by uploading their resume.

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [User Roles](#user-roles)
- [Database Models](#database-models)
- [URL Routes](#url-routes)
- [Forms](#forms)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [Media Files](#media-files)
- [Known Issues & Notes](#known-issues--notes)
- [Future Improvements](#future-improvements)

---

## ✨ Features

### General
- Custom user model extending Django's `AbstractUser` with role-based registration (`Seeker` or `Recruiter`)
- Secure login, logout, and registration system
- Role-aware views and redirects based on user type

### For Job Seekers
- Browse all available job listings
- Search jobs by title or description (keyword search)
- Filter jobs by category
- View detailed job information (description, salary, deadline, vacancy, required skills)
- Apply for a job by uploading a resume (PDF/file)
- View a personal list of all submitted applications

### For Recruiters
- Set up a company profile with logo, address, phone, and email
- Post new job listings with title, vacancy, category, description, required skills, salary, and deadline
- View and manage only their own posted jobs
- Edit or delete their own job posts
- View a list of all candidates who applied for a specific job posting

---

## 🛠 Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Backend     | Python 3, Django 6.0.4            |
| Database    | SQLite3 (default)                 |
| Frontend    | Django Templates, Bootstrap       |
| Auth        | Custom AbstractUser model         |
| Image/File  | Pillow 12.2.0                     |
| Search      | Django ORM with `Q` objects       |

---

## 📁 Project Structure

```
Job_Portal/
│
├── Job_Portal/                    # Project configuration
│   ├── settings.py                # Project settings (AUTH_USER_MODEL, MEDIA, etc.)
│   ├── urls.py                    # Root URL configuration
│   ├── asgi.py
│   └── wsgi.py
│
├── Job_Portal_App/                # Main application
│   ├── migrations/                # Database migrations
│   ├── templates/
│   │   ├── master/
│   │   │   ├── base.html          # Base layout template
│   │   │   ├── base-form.html     # Reusable form template
│   │   │   └── nav.html           # Navigation bar
│   │   ├── home.html              # Landing/home page
│   │   ├── register.html          # Registration page
│   │   ├── login.html             # Login page
│   │   ├── profile.html           # User profile view
│   │   ├── job-list.html          # Job listings with search & filter
│   │   ├── job-details.html       # Single job detail page
│   │   ├── job_applied.html       # Seeker's applied jobs list
│   │   └── candidate_list.html    # Recruiter's applicant list
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                   # All Django forms
│   ├── models.py                  # Database models
│   ├── urls.py                    # App-level URL patterns
│   └── views.py                   # All view logic
│
├── recruiter_logos/               # Uploaded recruiter/company logos
├── seeker_photos/                 # Uploaded seeker profile pictures
├── resumes/                       # Uploaded applicant resumes
├── db.sqlite3                     # SQLite database file
├── manage.py
└── requirements.txt
```

---

## 👤 User Roles

The application uses a **custom user model** (`UserInfoModel`) with a `user_types` field that determines access and behavior throughout the app.

| Role        | Capabilities                                                                 |
|-------------|------------------------------------------------------------------------------|
| **Recruiter** | Post jobs, edit/delete own jobs, view applicants for their job posts       |
| **Seeker**    | Browse all jobs, search & filter, apply with resume, view applied jobs     |

Role is selected during registration and cannot be changed afterwards.

---

## 🗄 Database Models

### `UserInfoModel` — Custom User (extends `AbstractUser`)
| Field          | Type      | Description                          |
|----------------|-----------|--------------------------------------|
| `display_name` | CharField | Publicly shown name                  |
| `user_types`   | CharField | `Seeker` or `Recruiter`              |

### `RecruiterProfileModel`
| Field          | Type          | Description                         |
|----------------|---------------|-------------------------------------|
| `recruiter`    | OneToOneField | Linked to `UserInfoModel`           |
| `company_name` | CharField     | Name of the company                 |
| `email`        | EmailField    | Company contact email               |
| `address`      | TextField     | Company address                     |
| `phone`        | CharField     | Contact phone number                |
| `logo`         | ImageField    | Company logo (uploaded to `recruiter_logos/`) |

### `JobSeekerProfileModel`
| Field             | Type          | Description                          |
|-------------------|---------------|--------------------------------------|
| `seeker`          | OneToOneField | Linked to `UserInfoModel`            |
| `profile_picture` | ImageField    | Photo (uploaded to `seeker_photos/`) |
| `address`         | TextField     | Seeker's address                     |
| `phone`           | CharField     | Contact phone number                 |

### `CategoryModel`
| Field  | Type      | Description              |
|--------|-----------|--------------------------|
| `name` | CharField | Job category name        |

### `JobPostModel`
| Field             | Type          | Description                                  |
|-------------------|---------------|----------------------------------------------|
| `title`           | CharField     | Job title                                    |
| `vacancy`         | PositiveIntegerField | Number of open positions               |
| `category`        | ForeignKey    | Linked to `CategoryModel`                    |
| `job_description` | TextField     | Full job description                         |
| `skills_set`      | TextField     | Required skills                              |
| `salary`          | DecimalField  | Offered salary                               |
| `deadline`        | DateField     | Application deadline                         |
| `created_at`      | DateTimeField | Auto-set on creation                         |
| `posted_by`       | ForeignKey    | Linked to `RecruiterProfileModel`            |

### `ApplyJobModel`
| Field        | Type          | Description                                    |
|--------------|---------------|------------------------------------------------|
| `applied_by` | ForeignKey    | Linked to `JobSeekerProfileModel`              |
| `applied_job`| ForeignKey    | Linked to `JobPostModel`                       |
| `resume`     | FileField     | Uploaded resume file (stored in `resumes/`)    |
| `applied_at` | DateTimeField | Auto-set on application submission             |

---

## 🔗 URL Routes

| URL                            | View              | Name              | Access        | Description                        |
|--------------------------------|-------------------|-------------------|---------------|------------------------------------|
| `/`                            | `home_page`       | `home_page`       | Public        | Landing/home page                  |
| `/register/`                   | `register_page`   | `register_page`   | Public        | User registration                  |
| `/login/`                      | `login_page`      | `login_page`      | Public        | User login                         |
| `/logout/`                     | `logout_page`     | `logout_page`     | Auth required | Logout current user                |
| `/profile/`                    | `profile_page`    | `profile_page`    | Auth required | View user profile                  |
| `/profile-update/`             | `profile_update`  | `profile_update`  | Auth required | Update recruiter or seeker profile |
| `/job-list/`                   | `job_list`        | `job_list`        | Public        | Browse, search, and filter jobs    |
| `/job-details/<j_id>/`         | `job_details`     | `job_details`     | Public        | View a single job's full details   |
| `/job-post/`                   | `job_post`        | `job_post`        | Auth required | Post a new job (Recruiter only)    |
| `/job-edit/<j_id>/`            | `job_edit`        | `job_edit`        | Auth required | Edit a job post (Recruiter only)   |
| `/job-delete/<j_id>/`          | `job_delete`      | `job_delete`      | Auth required | Delete a job post (Recruiter only) |
| `/job-apply/<j_id>/`           | `job_apply`       | `job_apply`       | Auth required | Apply for a job (Seeker only)      |
| `/applied-job/`                | `job_applied`     | `job_applied`     | Auth required | View applied jobs (Seeker only)    |
| `/candidate-list/<j_id>/`      | `candidate_list`  | `candidate_list`  | Auth required | View applicants (Recruiter only)   |

---

## 📝 Forms

| Form               | Model                    | Purpose                                   |
|--------------------|--------------------------|-------------------------------------------|
| `RegisterForm`     | `UserInfoModel`          | New user sign-up with role selection      |
| `LoginForm`        | `UserInfoModel`          | User login via Django's AuthenticationForm|
| `RecProfileForm`   | `RecruiterProfileModel`  | Update recruiter/company profile          |
| `SeekerProfileForm`| `JobSeekerProfileModel`  | Update seeker profile & photo             |
| `JobPostForm`      | `JobPostModel`           | Create or edit a job listing              |
| `JobApplyForm`     | `ApplyJobModel`          | Submit job application with resume        |

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10+
- pip

### Steps

**1. Extract the project:**
```bash
unzip Job_Portal.zip
cd Job_Portal
```

**2. Create and activate a virtual environment:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Apply database migrations:**
```bash
python manage.py migrate
```

**5. Create a superuser (for Django Admin):**
```bash
python manage.py createsuperuser
```

**6. Run the development server:**
```bash
python manage.py runserver
```

**7. Open in your browser:**
```
http://127.0.0.1:8000/
```

---

## 📖 Usage Guide

### As a Job Seeker
1. Go to `/register/` and sign up, selecting **Seeker** as your user type.
2. After login, go to `/profile-update/` to upload your photo and fill in your address and phone.
3. Browse available jobs at `/job-list/`.
4. Use the **search bar** to search by keyword or the **category filter** to narrow down results.
5. Click on any job to view its details at `/job-details/<id>/`.
6. Click **Apply** and upload your resume.
7. View all your submitted applications at `/applied-job/`.

### As a Recruiter
1. Go to `/register/` and sign up, selecting **Recruiter** as your user type.
2. After login, go to `/profile-update/` to set up your company name, logo, email, address, and phone.
3. Post a new job at `/job-post/`, filling in the title, category, description, required skills, salary, vacancy, and deadline.
4. View and manage your job posts from `/job-list/` (only your own posts are shown).
5. Use the **Edit** or **Delete** buttons to manage individual postings.
6. Click **View Candidates** on any post to see all applicants and their resumes at `/candidate-list/<id>/`.

---

## 🖼 Media Files

The project stores user-uploaded files locally in the following folders:

| Folder              | Contents                             |
|---------------------|--------------------------------------|
| `recruiter_logos/`  | Company logos uploaded by recruiters |
| `seeker_photos/`    | Profile pictures uploaded by seekers |
| `resumes/`          | Resume files uploaded by applicants  |

Make sure `MEDIA_URL` and `MEDIA_ROOT` are properly configured in `settings.py` and that media files are served correctly in development via `urls.py`.



## 🚀 Future Improvements

- [ ] Add role-based access control decorators (`@recruiter_required`, `@seeker_required`)
- [ ] Prevent duplicate job applications
- [ ] Add application status tracking (Pending / Reviewed / Accepted / Rejected)
- [ ] Add email notifications on application submission
- [ ] Add pagination to the job listing page
- [ ] Implement a bookmark / save job feature for seekers
- [ ] Add an admin dashboard with analytics (total jobs, applications, users)
- [ ] Add REST API support using Django REST Framework
- [ ] Write unit and integration tests
- [ ] Add Docker support for easier deployment
- [ ] Move to PostgreSQL for production-grade database

---

## 👤 Author

> This project was built as a Django learning project covering custom user models, role-based logic, file uploads, relational models, and search/filter functionality.

---

## 📄 License

This project is open-source and free to use for educational purposes.
