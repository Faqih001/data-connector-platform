import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'is_staff': True,
        'is_superuser': True,
        'email': 'admin@example.com'
    }
)

admin_user.set_password('admin123')
admin_user.save()

print(f"Admin user: {admin_user.username}")
print(f"Password: admin123")
print(f"Is superuser: {admin_user.is_superuser}")
print("\nAdmin credentials have been set!")

