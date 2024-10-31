# Deploying a Django Application on AWS with Gunicorn and Nginx

Deploying a Django application to AWS is a powerful way to make your project scalable and secure. This guide will walk you through deploying a Django application on an AWS EC2 instance using Docker, Nginx, Gunicorn, and system services for smooth deployment and management.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Step 1: Set Up Your AWS Environment](#step-1-set-up-your-aws-environment)
- [Step 2: Change the Django Application](#step-2-change-the-django-application)
  - [Check STATIC_URL and STATIC_ROOT](#check-static_url-and-static_root)
  - [Middleware Configuration](#middleware-configuration)
  - [Static Files Storage Configuration](#static-files-storage-configuration)
  - [Serving Static Files through URL Patterns](#serving-static-files-through-url-patterns)
  - [Example Configuration](#example-configuration)
  - [Ensure Static Files are Collected](#ensure-static-files-are-collected)
- [Step 3: Create a Directory and Download Your Application on AWS](#step-3-create-a-directory-and-download-your-application-on-aws)
- [Step 4: Set Up the Django Project](#step-4-set-up-the-django-project)
  - [Create a Virtual Environment](#create-a-virtual-environment)
  - [Activate the Virtual Environment](#activate-the-virtual-environment)
  - [Install Required Libraries](#install-required-libraries)
- [Step 5: Configure Gunicorn](#step-5-configure-gunicorn)
- [Step 6: Configure Nginx](#step-6-configure-nginx)
- [Step 7: Start and Enable Services](#step-7-start-and-enable-services)
- [Conclusion](#conclusion)

## Prerequisites
- An AWS EC2 instance (Ubuntu)
- Basic knowledge of Django
- Basic knowledge of Nginx and Gunicorn

## Step 1: Set Up Your AWS Environment
1. Log in to your AWS EC2 instance using SSH.
2. Update the package manager:
   ```bash
   sudo apt update
3. Install Nginx
   ```bash
   sudo apt install -y nginx

## Step 1: Set Up Your AWS Environment
- Check STATIC_URL and STATIC_ROOT
  - Verify that you have correctly set STATIC_URL and STATIC_ROOT in your Django settings:
    ``` bash
    # settings.py
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Ensure this matches your collectstatic output

- Middleware Configuration
  - Add WhiteNoise to your middleware list in settings.py:
    ``` bash
    MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Enhances security
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serves static files
    ...
    ]

- Static Files Storage Configuration
  - Enable caching of static files by setting STATICFILES_STORAGE in settings.py:
    ``` bash
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

- Serving Static Files through URL Patterns
  - Ensure your Django application serves the static files through your URL patterns:
    ``` bash
    from django.conf import settings
    from django.conf.urls.static import static
    
    urlpatterns = [
        # Your URL patterns here
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

- Example Configuration
  - Here’s a typical settings.py configuration for using WhiteNoise:
    ``` bash
    import os

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        ...
    ]
    
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


- Ensure Static Files are Collected
  - Make sure your static files are properly collected:
    ``` bash
    python manage.py collectstatic


