# Security Enhancements in Django App

## Settings
- `DEBUG = False` → prevent debug info leaks.
- `SECURE_BROWSER_XSS_FILTER`, `SECURE_CONTENT_TYPE_NOSNIFF`, `X_FRAME_OPTIONS = "DENY"` → protect against XSS, clickjacking.
- `CSRF_COOKIE_SECURE = True` and `SESSION_COOKIE_SECURE = True` → enforce HTTPS-only cookies.

## Templates
- `{% csrf_token %}` added to all forms to prevent CSRF.

## Views
- Use Django ORM (`Book.objects.filter`) instead of raw SQL → prevents SQL injection.
- Validate input using Django forms.

## CSP
- Custom middleware sets `Content-Security-Policy` header → mitigates XSS by whitelisting allowed content sources.
