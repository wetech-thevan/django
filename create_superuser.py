#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User

username = 'admin'
password = 'E3b1d13n'
email = 'admin@example.com'

# Tạo hoặc cập nhật superuser
if User.objects.filter(username=username).exists():
    # Nếu tồn tại, cập nhật password
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print(f"✓ Superuser '{username}' password được cập nhật thành công")
else:
    # Nếu chưa tồn tại, tạo mới
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"✓ Superuser '{username}' được tạo thành công")

