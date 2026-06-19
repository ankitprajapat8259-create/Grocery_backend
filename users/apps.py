from django.apps import AppConfig
import os

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        # Create superuser automatically when app starts
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Only create superuser if environment variables are set
        admin_email = os.environ.get('ADMIN_EMAIL')
        admin_password = os.environ.get('ADMIN_PASSWORD')
        admin_first_name = os.environ.get('ADMIN_FIRST_NAME', 'Admin')
        admin_last_name = os.environ.get('ADMIN_LAST_NAME', 'User')
        
        if admin_email and admin_password:
            if not User.objects.filter(email=admin_email).exists():
                User.objects.create_superuser(
                    email=admin_email,
                    password=admin_password,
                    first_name=admin_first_name,
                    last_name=admin_last_name
                )
                print(f"Superuser '{admin_email}' created successfully!")
