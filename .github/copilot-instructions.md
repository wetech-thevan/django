Project snapshot

- Simple Django app (single project `mysite`) with one app: `tasks`.
- DB: default SQLite (see `mysite/settings.py`). Deployment notes for Railway are present but DB env vars for Postgres are commented out.

Quick purpose for agents

- Help maintain and extend a small task-management Django app. Focus areas: small model changes, CBV views in `tasks/views.py`, forms in `tasks/forms.py`, templates in `templates/` and simple auth/permission logic.

Important files (start here)

- `manage.py` — standard Django entrypoint (runserver, migrate, check, test).
- `mysite/settings.py` — DB, static files, INSTALLED_APPS, middleware (note: Whitenoise is present but commented out).
- `tasks/models.py` — `Task` model: Vietnamese field names (e.g. `ten_cong_viec`, `nguoi_nhan`, `thoi_gian_tra`, `da_nhan`, `hoan_thanh`).
- `tasks/views.py` — Class-based views (ListView/CreateView/UpdateView/DeleteView) and custom `AdminRequiredMixin`. `TaskToggleStatusView` updates boolean fields via POST and enforces business rules.
- `tasks/forms.py` — `TaskForm` uses HTML5 `datetime-local` with input format `%Y-%m-%dT%H:%M`. `AdminUserCreationForm` and `AdminUserChangeForm` map an `is_admin` checkbox to `is_staff`.
- `templates/` — Project-level templates directory set in `TEMPLATES['DIRS']`. App templates live under `templates/tasks/`.

Developer workflows & commands (Windows PowerShell)

1) Create venv, install deps:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) DB + dev server:

```powershell
python manage.py migrate
python manage.py createsuperuser    # optional for admin flows
python manage.py runserver 0.0.0.0:8000
```

3) Quick checks/tests:

```powershell
python manage.py check
python manage.py test
```

Project-specific conventions and gotchas

- Vietnamese identifiers: many model fields, template context keys and messages use Vietnamese names. When changing templates or view context names, preserve these exact keys (e.g. `ten_cong_viec`, `nguoi_nhan`).
- Date/time input: `TaskForm.thoi_gian_tra` expects HTML `datetime-local` format. If you change the widget, update `input_formats=['%Y-%m-%dT%H:%M']` accordingly.
- Admin flag mapping: user-facing forms use `is_admin` but the DB flag is `User.is_staff`. Keep that mapping in `AdminUserCreationForm.save()` and `AdminUserChangeForm.save()`.
- Permission flow: `AdminRequiredMixin` in `tasks/views.py` checks `user.is_staff` and redirects to `'dashboard'` on failure. Don't remove this without adjusting calls in templates.
- Status toggles: `TaskToggleStatusView` enforces that `hoan_thanh` cannot be True unless `da_nhan` is True. Preserve this business rule when changing toggle logic or templates that POST to `task_toggle_status`.
- Static files: `STATICFILES_DIRS` and `STATIC_ROOT` are configured in `mysite/settings.py`. Whitenoise middleware is present but commented out — enable only for production deployments and run `collectstatic` if doing so.

Integration points & deploy notes

- Railway: `README.md` includes a Railway badge and `mysite/settings.py` contains commented environment-based Postgres config. If deploying to Railway, uncomment and use environment variables instead of the local SQLite.
- Whitenoise: middleware commented out — used for serving static files in simplified deploys. If enabling, add it near the top of `MIDDLEWARE`.

Agent rules when editing code

- Do not change DB schemas without adding migrations (`python manage.py makemigrations` + `migrate`).
- Preserve literal context keys and form field names used in templates unless you update the templates accordingly.
- When modifying views that affect permissions, update tests (none exist currently) or manually verify with a superuser + regular user.

If you make edits, run these checks before committing:

- `python manage.py check`
- `python manage.py makemigrations --dry-run` (if models changed)
- `python manage.py migrate` (if migrations were created)
- `python manage.py runserver` and manually smoke-test dashboard and account pages

Where to look for examples

- `tasks/views.py` — examples of CBV patterns, custom mixin, messages usage and redirect behavior.
- `tasks/forms.py` — form customization and widget examples.
- `tasks/models.py` — model naming, Meta ordering and __str__.

If anything is unclear or you want the instructions translated into Vietnamese (or expanded with automated tests and CI steps), tell me which parts to expand. 
