# Deploying a Django Application on AWS with Gunicorn and Nginx

Deploying a Django application to AWS is a powerful way to make your project scalable and secure. This guide will walk you through deploying a Django application on an AWS EC2 instance using Docker, Nginx, Gunicorn, and system services for smooth deployment and management.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Step 1: Set Up Your AWS Environment](#step-1-set-up-your-aws-environment)
- [Step 2: Change the Django Application](#step-2-change-the-django-application)
  - [Check STATIC_URL and STATIC_ROOT](#Check-STATIC_URL-and-STATIC_ROOT)
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

## Step 2: Change the Django Application
### Check STATIC_URL and STATIC_ROOT
  - Verify that you have correctly set STATIC_URL and STATIC_ROOT in your Django settings:
    ``` bash
    # settings.py
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Ensure this matches your collectstatic output

### Middleware Configuration
  - Add WhiteNoise to your middleware list in settings.py:
    ``` bash
    MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Enhances security
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serves static files
    ...
    ]

### Static Files Storage Configuration
  - Enable caching of static files by setting STATICFILES_STORAGE in settings.py:
    ``` bash
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

### Serving Static Files through URL Patterns
  - Ensure your Django application serves the static files through your URL patterns:
    ``` bash
    from django.conf import settings
    from django.conf.urls.static import static
    
    urlpatterns = [
        # Your URL patterns here
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

### Example Configuration
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


### Ensure Static Files are Collected
  - Make sure your static files are properly collected:
    ``` bash
    python manage.py collectstatic


## Step 3: Create a Directory and Download Your Application on AWS

1. Create a directory for your Django application
   ``` bash
   cd ~
   mkdir app
   cd app

2. Download your application. If it’s hosted on GitHub, clone it directly:
   ``` bash
   git clone https://github.com/sajitheranda/myproject.git

## Step 4: Set Up the Django Project

### Create a Virtual Environment
  - To keep dependencies isolated, create a virtual environment:
    ``` bash
    python3 -m venv env

### Activate the Virtual Environment
  - ``` bash
    source env/bin/activate


### Install Required Libraries
  - Install Libraries from requirements.txt
  - To install project dependencies:
  - ``` bash
    pip install -r requirements.txt

### Install Gunicorn
  - Install Gunicorn:
    ``` bash
    pip install gunicorn
    
### Install WhiteNoise
  - Install WhiteNoise:
    ``` bash
    pip install whitenoise


### Run Django Migrations and Collect Static Files
  - Prepare your database and gather static files:
    ``` bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py collectstatic

  - Deactivate the virtual environment:
    ``` bash
    deactivate

## Step 5: Configure Gunicorn

### Change to the user's home directory:
    cd ~

### Create a Gunicorn socket file:
    sudo vim /etc/systemd/system/gunicorn.socket

  - Add the following configuration:
    ``` bash
    [Unit]
    Description=gunicorn socket
    
    [Socket]
    ListenStream=/run/gunicorn.sock
    
    [Install]
    WantedBy=sockets.target

### Create a Gunicorn service file:
    sudo vim /etc/systemd/system/gunicorn.service

  - Add the following configuration:
    ``` bash
    [Unit]
    Description=gunicorn daemon
    Requires=gunicorn.socket
    After=network.target
    
    [Service]
    User=ubuntu
    Group=www-data
    WorkingDirectory=/home/ubuntu/app
    ExecStart=/home/ubuntu/app/env/bin/gunicorn \
              --access-logfile - \
              --workers 3 \
              --bind unix:/run/gunicorn.sock \
              jhothishyaaidjango.wsgi:application
    
    [Install]
    WantedBy=multi-user.target

## Step 6: Configure Nginx

### Remove Default Configuration
  - Navigate to Nginx’s enabled sites and remove the default file:
    ``` bash
    cd /etc/nginx/sites-enabled
    sudo rm -f default

### Create a New Nginx Server Block
  - Create a new server block:
    ``` bash
    sudo vim /etc/nginx/sites-available/myproject

  - Add the following configuration:
    ``` bash
    server {
    listen 80 default_server;
    server_name _;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /staticfiles/ {
        root /home/ubuntu/app;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
    }

### Enable the Server Block
  - Create a symbolic link to enable the new configuration:
    ``` bash
    sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled/

  - Add www-data to the ubuntu user group to access necessary directories:
    ``` bash
    sudo gpasswd -a www-data ubuntu

## Step 7: Start and Enable Services

### Enable and Start Gunicorn Socket
  - run
    ``` bash
    sudo systemctl start gunicorn.socket
    sudo systemctl enable gunicorn.socket

### Restart Nginx and Gunicorn Services
  - run
    ``` bash
    sudo systemctl restart nginx
    sudo service gunicorn restart
    sudo service nginx restart

Your Django application should now be accessible via your EC2 instance’s public IP address or domain name.

## Conclusion
This setup enables you to run a Django application on AWS using Docker, Gunicorn, and Nginx. This method is robust for production, offering a scalable and reliable solution. With this setup, you can now scale your application and handle requests efficiently.

- Happy coding and deploying!
   

