import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

# Create demo users
users = [
    {'username': 'admin', 'password': 'admin123', 'is_staff': True, 'is_superuser': True},
    {'username': 'john_sales', 'password': 'john123', 'is_staff': False, 'is_superuser': False},
    {'username': 'sarah_analytics', 'password': 'sarah456', 'is_staff': False, 'is_superuser': False},
    {'username': 'mike_reporting', 'password': 'mike789', 'is_staff': False, 'is_superuser': False},
]

print("Setting up demo users...")
for user_data in users:
    username = user_data['username']
    password = user_data['password']
    is_staff = user_data.get('is_staff', False)
    is_superuser = user_data.get('is_superuser', False)
    
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'is_staff': is_staff,
            'is_superuser': is_superuser,
            'email': f'{username}@example.com'
        }
    )
    
    user.set_password(password)
    user.is_staff = is_staff
    user.is_superuser = is_superuser
    user.save()
    
    status = "✓ Created" if created else "✓ Updated"
    print(f"{status}: {username} / {password} (Admin: {is_staff})")

print("\n✅ All demo users are ready!")
