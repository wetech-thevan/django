#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User

# Tạo superuser nếu chưa tồn tại
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='E3b1d13n'
    )
    print("✓ Superuser 'admin' được tạo thành công với password 'E3b1d13n'")
else:
    print("✓ Superuser 'admin' đã tồn tại")
