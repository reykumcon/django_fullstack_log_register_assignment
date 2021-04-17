from django.db import models
import bcrypt
import re

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name should be at least 2 characters long'
        
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name should be at least 2 characters long'

        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters long'
        
        if postData['password'] != postData['confirm_pw']:
            errors['mismatch'] = 'Passwords do not match'

        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['email']) == 0:
            errors['email'] = 'Please enter an email address'
        elif not email_regex.match(postData['email']):
            errors['email'] = 'Please enter a valid email address'

        unique_user = User.objects.filter(email=postData['email'])
        
        if len(unique_user) > 0:
            errors['duplicate'] = 'Email address already in use. Please enter another one'
        
        return errors

    def login_validator(self, postData):
        errors = {}

        user = User.objects.filter(email=postData['email'])

        if len(user) != 1:
            errors['user'] = 'User has not been registered'
        if len(postData['email']) == 0:
            errors['email'] = 'Please enter a valid email address'
        if len(postData['password']) < 8:
            errors['password'] = 'Please enter a valid password'
        elif bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()) != True:
            errors['mismatch'] = 'Email address and Password do not match. Please try again'

        return errors        

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)

    objects = UserManager()
