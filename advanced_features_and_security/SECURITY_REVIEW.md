# Security Review – HTTPS & Redirects

## What we implemented
- **SECURE_SSL_REDIRECT = True**: All HTTP requests are 301-redirected to HTTPS.
- **HSTS**: `SECURE_HSTS_SECONDS=31536000`, `SECURE_HSTS_INCLUDE_SUBDOMAINS=True`, `SECURE_HSTS_PRELOAD=True` to force browsers to use HTTPS for one year and qualify for HSTS preload (only after full HTTPS readiness).
- **Secure cookies**: `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True` prevent cookie leakage over HTTP.
- **Headers**: `X_FRAME_OPTIONS="DENY"`, `SECURE_CONTENT_TYPE_NOSNIFF=True`, `SECURE_BROWSER_XSS_FILTER=True` mitigate clickjacking, MIME sniffing, and some XSS risks.
- **Proxy awareness**: `SECURE_PROXY_SSL_HEADER=("HTTP_X_FORWARDED_PROTO","https")` so Django trusts HTTPS when behind a reverse proxy.

## How this secures the app
- **Confidentiality & Integrity**: HTTPS encrypts traffic; cookies won’t traverse plaintext channels.
- **Downgrade prevention**: HSTS stops browsers from attempting HTTP even if an attacker tries to force it.
- **UI redress/XSS hardening**: Headers block framing, sniffing, and hint old browsers to enable XSS filters.

## Operational notes
- Only enable `SECURE_HSTS_PRELOAD=True` when every subdomain serves HTTPS.
- Maintain TLS renewals with Certbot’s timer (`systemctl status certbot.timer`).
- Monitor redirects and ensure health checks are compatible (use `SECURE_REDIRECT_EXEMPT` if needed).
- Keep `DEBUG=False` and set correct `ALLOWED_HOSTS` + `CSRF_TRUSTED_ORIGINS`.

## Potential improvements
- Add a **Content Security Policy (CSP)** (via django-csp or custom middleware).
- Use **Expect-CT**/**Expect-CT reports** (legacy) or rely on Certificate Transparency by CAs.
- Implement **Subresource Integrity (SRI)** for any third-party assets.
- Automate security scanning (e.g., `bandit`, `pip-audit`) in CI.
