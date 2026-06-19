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
        
        if admin_email and admin_password:
            if not User.objects.filter(email=admin_email).exists():
                User.objects.create_superuser(
                    email=admin_email,
                    password=admin_password
                )
                print(f"Superuser '{admin_email}' created successfully!")
